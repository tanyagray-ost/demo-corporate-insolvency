#!/usr/bin/env python3

import argparse
import csv
import json
import sqlite3
import sys
import time
from pathlib import Path


CORPORATE_PSC_KIND = "corporate-entity-person-with-significant-control"
CSV_COLUMNS = [
    "controlled_company_number",
    "controller_company_number",
    "controller_name",
    "notified_on",
    "ceased_on",
    "ceased",
    "nature_of_control",
    "legal_form",
    "legal_authority",
    "country_registered",
    "place_registered",
    "psc_kind",
    "source_url",
    "etag",
    "depth_from_root",
]


def normalise_company_number(value: str) -> str:
    number = value.strip().upper()
    return number.zfill(8) if number.isdigit() else number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract a corporate-only ownership graph from a Companies House "
            "PSC snapshot without loading the snapshot into memory."
        )
    )
    parser.add_argument("snapshot", type=Path, help="PSC snapshot NDJSON file")
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        help="Root Companies House number; may be supplied more than once",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output CSV path",
    )
    parser.add_argument(
        "--database",
        type=Path,
        help="Reusable SQLite index path (defaults alongside the snapshot)",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild the SQLite index even if it matches the snapshot",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=1_000_000,
        help="Report progress after this many input records",
    )
    args = parser.parse_args()
    if not args.root:
        args.root = ["03782379"]
    args.root = [normalise_company_number(root) for root in args.root]
    if args.database is None:
        args.database = args.snapshot.with_suffix(".corporate-psc.sqlite")
    return args


def initialise_database(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        DROP TABLE IF EXISTS metadata;
        DROP TABLE IF EXISTS control_natures;
        DROP TABLE IF EXISTS relationships;

        CREATE TABLE metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            controlled_company_number TEXT NOT NULL,
            controller_company_number TEXT NOT NULL,
            controller_name TEXT NOT NULL,
            notified_on TEXT,
            ceased_on TEXT,
            ceased INTEGER NOT NULL,
            legal_form TEXT,
            legal_authority TEXT,
            country_registered TEXT,
            place_registered TEXT,
            psc_kind TEXT NOT NULL,
            source_url TEXT NOT NULL UNIQUE,
            etag TEXT
        );

        CREATE TABLE control_natures (
            relationship_id INTEGER NOT NULL,
            nature_of_control TEXT NOT NULL,
            PRIMARY KEY (relationship_id, nature_of_control),
            FOREIGN KEY (relationship_id) REFERENCES relationships(id)
        );
        """
    )


def index_matches_snapshot(
    connection: sqlite3.Connection, snapshot: Path
) -> bool:
    try:
        metadata = dict(connection.execute("SELECT key, value FROM metadata"))
    except sqlite3.OperationalError:
        return False
    stat = snapshot.stat()
    return (
        metadata.get("complete") == "true"
        and metadata.get("snapshot_path") == str(snapshot.resolve())
        and metadata.get("snapshot_size") == str(stat.st_size)
        and metadata.get("snapshot_mtime_ns") == str(stat.st_mtime_ns)
    )


def index_snapshot(
    connection: sqlite3.Connection, snapshot: Path, progress_every: int
) -> None:
    initialise_database(connection)
    started = time.monotonic()
    corporate_records = 0
    line_number = 0

    relationship_sql = """
        INSERT OR IGNORE INTO relationships (
            controlled_company_number,
            controller_company_number,
            controller_name,
            notified_on,
            ceased_on,
            ceased,
            legal_form,
            legal_authority,
            country_registered,
            place_registered,
            psc_kind,
            source_url,
            etag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    with snapshot.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at input line {line_number}: {error}"
                ) from error

            data = record.get("data", {})
            if data.get("kind") != CORPORATE_PSC_KIND:
                if progress_every and line_number % progress_every == 0:
                    report_progress(line_number, corporate_records, started)
                continue

            identification = data.get("identification", {})
            registration_number = identification.get("registration_number")
            controlled_number = record.get("company_number")
            source_path = data.get("links", {}).get("self")
            if not registration_number or not controlled_number or not source_path:
                continue

            values = (
                normalise_company_number(controlled_number),
                normalise_company_number(registration_number),
                data.get("name", ""),
                data.get("notified_on"),
                data.get("ceased_on"),
                int(bool(data.get("ceased", False) or data.get("ceased_on"))),
                identification.get("legal_form"),
                identification.get("legal_authority"),
                identification.get("country_registered"),
                identification.get("place_registered"),
                data["kind"],
                "https://api.company-information.service.gov.uk" + source_path,
                data.get("etag"),
            )
            cursor = connection.execute(relationship_sql, values)
            if cursor.rowcount:
                relationship_id = cursor.lastrowid
            else:
                relationship_id = connection.execute(
                    "SELECT id FROM relationships WHERE source_url = ?",
                    (values[-2],),
                ).fetchone()[0]

            connection.executemany(
                """
                INSERT OR IGNORE INTO control_natures (
                    relationship_id, nature_of_control
                ) VALUES (?, ?)
                """,
                [
                    (relationship_id, nature)
                    for nature in data.get("natures_of_control", [])
                ],
            )
            corporate_records += 1

            if corporate_records % 10_000 == 0:
                connection.commit()
            if progress_every and line_number % progress_every == 0:
                report_progress(line_number, corporate_records, started)

    connection.executescript(
        """
        CREATE INDEX relationships_by_controller
            ON relationships(controller_company_number);
        CREATE INDEX relationships_by_controlled
            ON relationships(controlled_company_number);
        """
    )
    stat = snapshot.stat()
    connection.executemany(
        "INSERT INTO metadata (key, value) VALUES (?, ?)",
        [
            ("complete", "true"),
            ("snapshot_path", str(snapshot.resolve())),
            ("snapshot_size", str(stat.st_size)),
            ("snapshot_mtime_ns", str(stat.st_mtime_ns)),
        ],
    )
    connection.commit()
    report_progress(line_number, corporate_records, started)


def report_progress(
    line_number: int, corporate_records: int, started: float
) -> None:
    elapsed = max(time.monotonic() - started, 0.001)
    print(
        f"Scanned {line_number:,} records; indexed "
        f"{corporate_records:,} corporate PSCs "
        f"({line_number / elapsed:,.0f} records/s)",
        file=sys.stderr,
        flush=True,
    )


def discover_group(
    connection: sqlite3.Connection, roots: list[str]
) -> tuple[dict[str, int], set[int]]:
    depths = {root: 0 for root in roots}
    frontier = set(roots)
    relationship_ids: set[int] = set()

    while frontier:
        next_frontier: set[str] = set()
        for controller in frontier:
            rows = connection.execute(
                """
                SELECT id, controlled_company_number
                FROM relationships
                WHERE controller_company_number = ?
                """,
                (controller,),
            )
            for relationship_id, controlled in rows:
                relationship_ids.add(relationship_id)
                if controlled not in depths:
                    depths[controlled] = depths[controller] + 1
                    next_frontier.add(controlled)
        frontier = next_frontier

    return depths, relationship_ids


def write_csv(
    connection: sqlite3.Connection,
    output: Path,
    depths: dict[str, int],
    relationship_ids: set[int],
) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    row_count = 0

    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_COLUMNS)
        writer.writeheader()

        for relationship_id in sorted(relationship_ids):
            row = connection.execute(
                """
                SELECT
                    controlled_company_number,
                    controller_company_number,
                    controller_name,
                    notified_on,
                    ceased_on,
                    ceased,
                    legal_form,
                    legal_authority,
                    country_registered,
                    place_registered,
                    psc_kind,
                    source_url,
                    etag
                FROM relationships
                WHERE id = ?
                """,
                (relationship_id,),
            ).fetchone()
            natures = [
                item[0]
                for item in connection.execute(
                    """
                    SELECT nature_of_control
                    FROM control_natures
                    WHERE relationship_id = ?
                    ORDER BY nature_of_control
                    """,
                    (relationship_id,),
                )
            ] or [""]

            for nature in natures:
                writer.writerow(
                    {
                        "controlled_company_number": row[0],
                        "controller_company_number": row[1],
                        "controller_name": row[2],
                        "notified_on": row[3] or "",
                        "ceased_on": row[4] or "",
                        "ceased": "true" if row[5] else "false",
                        "nature_of_control": nature,
                        "legal_form": row[6] or "",
                        "legal_authority": row[7] or "",
                        "country_registered": row[8] or "",
                        "place_registered": row[9] or "",
                        "psc_kind": row[10],
                        "source_url": row[11],
                        "etag": row[12] or "",
                        "depth_from_root": depths[row[0]],
                    }
                )
                row_count += 1

    return row_count


def main() -> None:
    args = parse_args()
    if not args.snapshot.is_file():
        raise SystemExit(f"Snapshot does not exist: {args.snapshot}")

    args.database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(args.database)
    try:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = NORMAL")
        connection.execute("PRAGMA foreign_keys = ON")

        if args.rebuild or not index_matches_snapshot(connection, args.snapshot):
            print(f"Indexing {args.snapshot} into {args.database}", file=sys.stderr)
            index_snapshot(connection, args.snapshot, args.progress_every)
        else:
            print(f"Reusing index {args.database}", file=sys.stderr)

        depths, relationship_ids = discover_group(connection, args.root)
        row_count = write_csv(
            connection, args.output, depths, relationship_ids
        )
    finally:
        connection.close()

    print(
        f"Wrote {row_count:,} CSV rows for "
        f"{len(relationship_ids):,} corporate relationships and "
        f"{len(depths):,} companies to {args.output}"
    )


if __name__ == "__main__":
    main()
