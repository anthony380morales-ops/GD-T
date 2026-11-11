#!/usr/bin/env python3
"""Regenerate the .json files from the .csv files.

CSV is the source of truth; JSON is a convenience copy for people who would rather
fetch one file than parse three. tools/verify.py fails if the two ever disagree, so
run this after editing any CSV.
"""
import csv
import json
import pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"

for csv_path in sorted(DATA.glob("*.csv")):
    with open(csv_path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = csv_path.with_suffix(".json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rows, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"{out.name}: {len(rows)} rows")
