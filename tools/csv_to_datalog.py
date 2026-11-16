#!/usr/bin/env python3
"""Generate Datalog facts from the CSV files in the data directory."""

import argparse
import csv
import re
from pathlib import Path


NUMBER = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?\Z")


def datalog_value(value):
    """Convert one CSV value to a Datalog constant."""
    if value == "":
        return "null"
    if NUMBER.fullmatch(value):
        return value
    escaped = value.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


def generate_facts(data_dir, output_path):
    """Write one Datalog fact for every row in every CSV in data_dir."""
    data_dir = Path(data_dir)
    output_path = Path(output_path)
    csv_files = sorted(data_dir.glob("*.csv"))

    lines = [
        "% Ndreqe - Faza 1: fakte te gjeneruara nga CSV-te e data/.",
        f"% {len(csv_files)} relacione, nje fakt per cdo rresht te CSV-ve.",
        "% Vlerat NULL/empty perfaqesohen me konstanten null.",
        "",
    ]

    for csv_path in csv_files:
        relation = csv_path.stem.lower()
        with csv_path.open("r", encoding="utf-8", newline="") as source:
            rows = list(csv.reader(source))

        if not rows:
            continue

        lines.append(f"% Relation: {relation} | facts: {len(rows) - 1}")
        for row in rows[1:]:
            values = ", ".join(datalog_value(value) for value in row)
            lines.append(f"{relation}({values}).")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=repository_root / "data")
    parser.add_argument(
        "--output",
        type=Path,
        default=repository_root / "faza1" / "fakte.dl",
    )
    args = parser.parse_args()
    generate_facts(args.data_dir, args.output)


if __name__ == "__main__":
    main()
