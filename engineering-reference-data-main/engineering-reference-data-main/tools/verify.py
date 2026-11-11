#!/usr/bin/env python3
"""Re-derive every checkable claim in data/ from sources other than these files.

Unicode glyphs and names come from the Unicode Character Database shipped with
Python. Row counts, ASME/ISO status, datum rules and the ISO 1302 N-grade Ra
series are invariants of the dataset: if a row moves, this script fails until
the change is deliberate. CSV is the source of truth; JSON is a convenience
copy and must match.

    python tools/verify.py
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

SYMBOLS_CSV = "gdt-symbols.csv"
MODIFIERS_CSV = "gdt-modifiers.csv"
ROUGHNESS_CSV = "surface-roughness-grades.csv"

# UCD names that drafting practice borrowed. Dedicated rows must not use these;
# borrowed rows must.
BORROWED_UCD_NAMES = {
    "WHITE CIRCLE",
    "ARC",
    "SEGMENT",
    "ANGLE",
    "PERPENDICULAR",
    "PARALLEL TO",
    "BULLSEYE",
    "NORTH EAST ARROW",
    "DIAMETER SIGN",
    "DOWNWARDS ARROW FROM BAR",
}

# ISO 1302 preferred Ra numbers. N9 is 6.3 µm, not 6.4; N7 in microinches is 63,
# not 64. Both are R10 preferred numbers, not binary doubling.
ISO_1302_RA_UM = {
    "N1": 0.025,
    "N2": 0.05,
    "N3": 0.1,
    "N4": 0.2,
    "N5": 0.4,
    "N6": 0.8,
    "N7": 1.6,
    "N8": 3.2,
    "N9": 6.3,
    "N10": 12.5,
    "N11": 25.0,
    "N12": 50.0,
}
ISO_1302_RA_UIN = {
    "N1": 1,
    "N2": 2,
    "N3": 4,
    "N4": 8,
    "N5": 16,
    "N6": 32,
    "N7": 63,
    "N8": 125,
    "N9": 250,
    "N10": 500,
    "N11": 1000,
    "N12": 2000,
}

WITHDRAWN_IN_ASME_2018 = {"Concentricity", "Symmetry"}

DATUM_BY_CATEGORY = {
    "form": "no",
    "profile": "optional",
    "orientation": "yes",
    "location": "yes",
    "runout": "yes",
}


def read_csv(name: str) -> list[dict[str, str]]:
    with open(DATA / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def is_borrowed(ucd_name: str) -> bool:
    return ucd_name.startswith("CIRCLED LATIN") or ucd_name in BORROWED_UCD_NAMES


def check_unicode(rows: list[dict[str, str]], filename: str, label_key: str) -> list[str]:
    failures = []
    seen = set()
    for row in rows:
        label = row[label_key]
        cp_text = row["codepoint"]
        if not cp_text.startswith("U+"):
            failures.append(f"{filename}: {label}: codepoint {cp_text!r} is not in U+XXXX form")
            continue
        try:
            cp = int(cp_text[2:], 16)
        except ValueError:
            failures.append(f"{filename}: {label}: codepoint {cp_text!r} is not hexadecimal")
            continue
        if cp in seen:
            failures.append(f"{filename}: {label}: duplicate codepoint {cp_text}")
        seen.add(cp)
        char = chr(cp)
        if row["symbol"] != char:
            failures.append(
                f"{filename}: {label}: symbol column is {row['symbol']!r} but {cp_text} is {char!r}"
            )
        try:
            actual = unicodedata.name(char)
        except ValueError:
            failures.append(f"{filename}: {label}: {cp_text} has no name in this UCD")
            continue
        if actual != row["unicode_name"]:
            failures.append(
                f"{filename}: {label}: {cp_text} is named {actual!r}, data says {row['unicode_name']!r}"
            )
        dedicated = row["codepoint_dedicated_to_gdt"] == "yes"
        borrowed = is_borrowed(actual)
        if dedicated and borrowed:
            failures.append(
                f"{filename}: {label}: marked dedicated but {actual!r} is a borrowed character"
            )
        if not dedicated and not borrowed:
            failures.append(
                f"{filename}: {label}: marked borrowed but {actual!r} is not in the borrowed-name list"
            )
    return failures


def check_symbols(rows: list[dict[str, str]]) -> list[str]:
    failures = []
    if len(rows) != 14:
        failures.append(f"{SYMBOLS_CSV}: expected 14 geometric characteristics, found {len(rows)}")
    names = [row["characteristic"] for row in rows]
    if len(names) != len(set(names)):
        failures.append(f"{SYMBOLS_CSV}: duplicate characteristic name")
    for expected in WITHDRAWN_IN_ASME_2018:
        if expected not in names:
            failures.append(f"{SYMBOLS_CSV}: missing {expected}, which is the ASME Y14.5-2018 withdrawal")
    for row in rows:
        name = row["characteristic"]
        asme = row["asme_y14_5_2018"]
        iso = row["iso_1101"]
        if name in WITHDRAWN_IN_ASME_2018:
            if asme != "withdrawn":
                failures.append(f"{SYMBOLS_CSV}: {name}: asme_y14_5_2018 must be withdrawn, not {asme!r}")
            if iso != "active":
                failures.append(f"{SYMBOLS_CSV}: {name}: iso_1101 must be active, not {iso!r}")
        else:
            if asme != "active":
                failures.append(f"{SYMBOLS_CSV}: {name}: asme_y14_5_2018 must be active, not {asme!r}")
            if iso != "active":
                failures.append(f"{SYMBOLS_CSV}: {name}: iso_1101 must be active, not {iso!r}")
        expected_datum = DATUM_BY_CATEGORY.get(row["category"])
        if expected_datum and row["datum_required"] != expected_datum:
            failures.append(
                f"{SYMBOLS_CSV}: {name}: category {row['category']!r} requires datum_required={expected_datum!r}"
            )
    asme_active = sum(1 for row in rows if row["asme_y14_5_2018"] == "active")
    if asme_active != 12:
        failures.append(f"{SYMBOLS_CSV}: ASME Y14.5-2018 must have 12 active characteristics, found {asme_active}")
    return failures


def check_modifiers(rows: list[dict[str, str]]) -> list[str]:
    failures = []
    if len(rows) != 15:
        failures.append(f"{MODIFIERS_CSV}: expected 15 modifiers, found {len(rows)}")
    names = [row["modifier"] for row in rows]
    if len(names) != len(set(names)):
        failures.append(f"{MODIFIERS_CSV}: duplicate modifier name")
    return failures


def check_roughness(rows: list[dict[str, str]]) -> list[str]:
    failures = []
    if len(rows) != 12:
        failures.append(f"{ROUGHNESS_CSV}: expected 12 N-grades, found {len(rows)}")
    grades = [row["grade"] for row in rows]
    if grades != [f"N{i}" for i in range(1, 13)]:
        failures.append(f"{ROUGHNESS_CSV}: grades must be N1..N12 in order, found {grades}")
    for row in rows:
        grade = row["grade"]
        try:
            ra_um = float(row["ra_um"])
            ra_uin = int(row["ra_uin_conventional"])
        except ValueError:
            failures.append(f"{ROUGHNESS_CSV}: {grade}: non-numeric Ra")
            continue
        if ra_um != ISO_1302_RA_UM[grade]:
            failures.append(
                f"{ROUGHNESS_CSV}: {grade}: ra_um {ra_um} != ISO 1302 preferred {ISO_1302_RA_UM[grade]}"
            )
        if ra_uin != ISO_1302_RA_UIN[grade]:
            failures.append(
                f"{ROUGHNESS_CSV}: {grade}: ra_uin_conventional {ra_uin} != ISO 1302 preferred {ISO_1302_RA_UIN[grade]}"
            )
    return failures


def check_json_sync() -> list[str]:
    failures = []
    for csv_path in sorted(DATA.glob("*.csv")):
        json_path = csv_path.with_suffix(".json")
        if not json_path.exists():
            failures.append(f"{json_path.name} is missing; run tools/to-json.py")
            continue
        with open(csv_path, encoding="utf-8", newline="") as fh:
            from_csv = list(csv.DictReader(fh))
        from_json = json.loads(json_path.read_text(encoding="utf-8"))
        if from_csv != from_json:
            failures.append(f"{json_path.name} does not match {csv_path.name}; run tools/to-json.py")
    return failures


def main() -> int:
    failures: list[str] = []
    symbols = read_csv(SYMBOLS_CSV)
    modifiers = read_csv(MODIFIERS_CSV)
    roughness = read_csv(ROUGHNESS_CSV)

    failures.extend(check_unicode(symbols, SYMBOLS_CSV, "characteristic"))
    failures.extend(check_unicode(modifiers, MODIFIERS_CSV, "modifier"))
    failures.extend(check_symbols(symbols))
    failures.extend(check_modifiers(modifiers))
    failures.extend(check_roughness(roughness))
    failures.extend(check_json_sync())

    checked = len(symbols) + len(modifiers)
    print(f"Unicode UCD version: {unicodedata.unidata_version}")
    print(f"checked {checked} codepoints and {len(roughness)} N-grades")
    if failures:
        print(f"\n{len(failures)} FAILURE(S):", file=sys.stderr)
        for item in failures:
            print("  " + item, file=sys.stderr)
        return 1
    print("all claims verified")
    print(f"csv/json in sync across {len(list(DATA.glob('*.csv')))} datasets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
