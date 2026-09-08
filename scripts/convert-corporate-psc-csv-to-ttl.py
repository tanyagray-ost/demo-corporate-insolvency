#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path
from urllib.parse import quote, urlparse


BASE = "https://w3id.org/rdfox-project-x-demo/"
ONTOLOGY = BASE + "ontology/psc#"
RESOURCE = BASE + "resource/"
NATURE_OF_CONTROL = BASE + "vocab/nature-of-control/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a corporate-only Companies House PSC ownership CSV "
            "into Turtle."
        )
    )
    parser.add_argument("input", type=Path, help="Corporate PSC ownership CSV")
    parser.add_argument("output", type=Path, help="Output Turtle file")
    return parser.parse_args()


def turtle_string(value: str) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )
    return f'"{escaped}"'


def company_iri(company_number: str) -> str:
    return f"<{RESOURCE}company/{quote(company_number, safe='')}>"


def event_iri(source_url: str) -> str:
    controlled_company = urlparse(source_url).path.split("/")[2]
    notification_id = urlparse(source_url).path.rstrip("/").split("/")[-1]
    return (
        f"<{RESOURCE}psc-notification/"
        f"{quote(controlled_company, safe='')}/"
        f"{quote(notification_id, safe='')}>"
    )


def nature_iri(value: str) -> str:
    return f"<{NATURE_OF_CONTROL}{quote(value, safe='')}>"


def load_csv(path: Path) -> tuple[dict[str, dict], set[str]]:
    events: dict[str, dict] = {}
    companies: set[str] = set()

    with path.open("r", encoding="utf-8", newline="") as stream:
        for row_number, row in enumerate(csv.DictReader(stream), start=2):
            controlled = row["controlled_company_number"].strip()
            controller = row["controller_company_number"].strip()
            source_url = row["source_url"].strip()
            if not controlled or not controller or not source_url:
                raise ValueError(
                    f"Missing company number or source URL at CSV row {row_number}"
                )

            companies.update((controlled, controller))

            event = events.setdefault(
                source_url,
                {
                    "controlled": controlled,
                    "controller": controller,
                    "notified_on": row["notified_on"].strip(),
                    "ceased_on": row["ceased_on"].strip(),
                    "ceased": row["ceased"].strip().lower(),
                    "source_url": source_url,
                    "reported_controller_name": row[
                        "controller_name"
                    ].strip(),
                    "reported_controller_legal_form": row[
                        "legal_form"
                    ].strip(),
                    "reported_controller_legal_authority": row[
                        "legal_authority"
                    ].strip(),
                    "reported_controller_country_registered": row[
                        "country_registered"
                    ].strip(),
                    "reported_controller_place_registered": row[
                        "place_registered"
                    ].strip(),
                    "source_etag": row["etag"].strip(),
                    "natures": set(),
                },
            )
            identity = (
                event["controlled"],
                event["controller"],
                event["notified_on"],
                event["ceased_on"],
                event["ceased"],
                event["reported_controller_name"],
                event["reported_controller_legal_form"],
                event["reported_controller_legal_authority"],
                event["reported_controller_country_registered"],
                event["reported_controller_place_registered"],
                event["source_etag"],
            )
            candidate = (
                controlled,
                controller,
                row["notified_on"].strip(),
                row["ceased_on"].strip(),
                row["ceased"].strip().lower(),
                row["controller_name"].strip(),
                row["legal_form"].strip(),
                row["legal_authority"].strip(),
                row["country_registered"].strip(),
                row["place_registered"].strip(),
                row["etag"].strip(),
            )
            if identity != candidate:
                raise ValueError(
                    f"Inconsistent duplicate event at CSV row {row_number}"
                )
            if row["nature_of_control"].strip():
                event["natures"].add(row["nature_of_control"].strip())

    return events, companies


def write_prefixes(stream) -> None:
    stream.write(
        f"""@prefix psc: <{ONTOLOGY}> .
@prefix noc: <{NATURE_OF_CONTROL}> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

"""
    )


def write_companies(stream, companies: set[str]) -> None:
    for company_number in sorted(companies):
        stream.write(
            f"{company_iri(company_number)} a psc:Company ;\n"
            f"    psc:companyNumber {turtle_string(company_number)} .\n\n"
        )


def write_events(stream, events: dict[str, dict]) -> None:
    for source_url, event in sorted(events.items()):
        predicates = [
            f"    psc:controllerCompany {company_iri(event['controller'])}",
            f"    psc:controlledCompany {company_iri(event['controlled'])}",
        ]
        predicates.extend(
            f"    psc:hasNatureOfControl {nature_iri(nature)}"
            for nature in sorted(event["natures"])
        )
        reported_values = [
            ("reportedControllerName", event["reported_controller_name"]),
            (
                "reportedControllerLegalForm",
                event["reported_controller_legal_form"],
            ),
            (
                "reportedControllerLegalAuthority",
                event["reported_controller_legal_authority"],
            ),
            (
                "reportedControllerCountryRegistered",
                event["reported_controller_country_registered"],
            ),
            (
                "reportedControllerPlaceRegistered",
                event["reported_controller_place_registered"],
            ),
        ]
        predicates.extend(
            f"    psc:{predicate} {turtle_string(value)}"
            for predicate, value in reported_values
            if value
        )
        if event["notified_on"]:
            predicates.append(
                "    psc:notifiedOn "
                f'{turtle_string(event["notified_on"])}^^xsd:date'
            )
        if event["ceased_on"]:
            predicates.append(
                "    psc:ceasedOn "
                f'{turtle_string(event["ceased_on"])}^^xsd:date'
            )
        ceased = "true" if event["ceased"] == "true" else "false"
        predicates.extend(
            [
                f"    psc:ceased {ceased}",
                f"    prov:wasDerivedFrom <{source_url}>",
            ]
        )
        if event["source_etag"]:
            predicates.append(
                "    psc:sourceETag "
                f'{turtle_string(event["source_etag"])}'
            )
        stream.write(
            f"{event_iri(source_url)} "
            "a psc:CorporateEntityPSCNotification ;\n"
            + " ;\n".join(predicates)
            + " .\n\n"
        )


def main() -> None:
    args = parse_args()
    events, companies = load_csv(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        write_prefixes(stream)
        write_companies(stream, companies)
        write_events(stream, events)
    print(
        f"Wrote {len(companies)} companies and {len(events)} PSC events "
        f"to {args.output}"
    )


if __name__ == "__main__":
    main()
