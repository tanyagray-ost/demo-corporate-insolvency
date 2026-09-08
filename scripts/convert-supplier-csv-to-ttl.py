#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path
from urllib.parse import quote


BASE = "https://w3id.org/rdfox-project-x-demo/"
COMPANY = BASE + "resource/company/"
RELATIONSHIP = BASE + "resource/supplier-relationship/"

REQUIRED_COLUMNS = {
    "relationship_id",
    "customer_company_name",
    "customer_company_number",
    "supplier_company_name",
    "supplier_company_number",
    "supplier_reference_type",
    "supply_category",
    "relationship_status",
    "valid_from",
    "valid_to",
    "synthetic",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert the synthetic supplier-list CSV into Turtle."
    )
    parser.add_argument("input", type=Path, help="Supplier-list CSV")
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


def resource_iri(base: str, identifier: str) -> str:
    return f"<{base}{quote(identifier, safe='')}>"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or ())
        if missing:
            raise ValueError(
                "Missing required CSV columns: " + ", ".join(sorted(missing))
            )

        rows = []
        relationship_ids = set()
        for row_number, row in enumerate(reader, start=2):
            cleaned = {key: value.strip() for key, value in row.items()}
            required_values = (
                "relationship_id",
                "customer_company_name",
                "customer_company_number",
                "supplier_company_name",
                "supplier_company_number",
            )
            if any(not cleaned[key] for key in required_values):
                raise ValueError(
                    f"Missing relationship or company value at row {row_number}"
                )
            if cleaned["relationship_id"] in relationship_ids:
                raise ValueError(
                    f"Duplicate relationship ID at row {row_number}"
                )
            if cleaned["synthetic"].lower() not in {"true", "false"}:
                raise ValueError(
                    f"Invalid synthetic Boolean at row {row_number}"
                )
            relationship_ids.add(cleaned["relationship_id"])
            rows.append(cleaned)
    return rows


def write_turtle(path: Path, rows: list[dict[str, str]]) -> None:
    companies: dict[str, str] = {}
    for row in rows:
        for role in ("customer", "supplier"):
            number = row[f"{role}_company_number"]
            name = row[f"{role}_company_name"]
            previous = companies.setdefault(number, name)
            if previous != name:
                raise ValueError(
                    f"Inconsistent names for company number {number}"
                )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(
            """@prefix psc: <https://w3id.org/rdfox-project-x-demo/ontology/psc#> .
@prefix supply: <https://w3id.org/rdfox-project-x-demo/ontology/supply#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

"""
        )
        for number, name in sorted(companies.items()):
            stream.write(
                f"{resource_iri(COMPANY, number)} a psc:Company ;\n"
                f"    psc:companyNumber {turtle_string(number)} ;\n"
                f"    supply:companyName {turtle_string(name)} .\n\n"
            )

        for row in rows:
            predicates = [
                "    supply:customer "
                + resource_iri(COMPANY, row["customer_company_number"]),
                "    supply:supplier "
                + resource_iri(COMPANY, row["supplier_company_number"]),
                "    supply:supplierReferenceType "
                + turtle_string(row["supplier_reference_type"]),
                "    supply:supplyCategory "
                + turtle_string(row["supply_category"]),
                "    supply:relationshipStatus "
                + turtle_string(row["relationship_status"]),
            ]
            if row["valid_from"]:
                predicates.append(
                    "    supply:validFrom "
                    f"{turtle_string(row['valid_from'])}^^xsd:date"
                )
            if row["valid_to"]:
                predicates.append(
                    "    supply:validTo "
                    f"{turtle_string(row['valid_to'])}^^xsd:date"
                )
            predicates.append(
                f"    supply:synthetic {row['synthetic'].lower()}"
            )
            stream.write(
                f"{resource_iri(RELATIONSHIP, row['relationship_id'])} "
                "a supply:SupplierRelationship ;\n"
                + " ;\n".join(predicates)
                + " .\n\n"
            )


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)
    write_turtle(args.output, rows)
    print(f"Wrote {len(rows)} supplier relationships to {args.output}")


if __name__ == "__main__":
    main()
