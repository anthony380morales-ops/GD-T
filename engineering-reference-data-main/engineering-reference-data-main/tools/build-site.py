#!/usr/bin/env python3
"""Build a static HTML view of data/ so the tables can be read without opening a CSV.

The page is generated from the CSVs, never edited by hand. tools/verify.py is the
authority for whether the numbers are still true; this script only renders them.
"""
from __future__ import annotations

import csv
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "site"

COMPANION = "https://makenexa.com/resources/engineering-drawing-checklist/"
REPO = "https://github.com/makenexa/engineering-reference-data"


def rows(name: str) -> list[dict[str, str]]:
    with open(DATA / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def table(headers: list[str], body: list[list[str]], caption: str) -> str:
    head = "".join(f"<th scope='col'>{html.escape(h)}</th>" for h in headers)
    trs = []
    for row in body:
        cells = "".join(f"<td>{c}</td>" for c in row)
        trs.append(f"<tr>{cells}</tr>")
    return (
        f"<table><caption>{html.escape(caption)}</caption>"
        f"<thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(trs)}</tbody></table>"
    )


def glyph(char: str) -> str:
    return f"<span class='glyph'>{html.escape(char)}</span>"


def status_cell(value: str) -> str:
    klass = "withdrawn" if value == "withdrawn" else "active"
    return f"<span class='{klass}'>{html.escape(value)}</span>"


def main() -> None:
    symbols = rows("gdt-symbols.csv")
    modifiers = rows("gdt-modifiers.csv")
    roughness = rows("surface-roughness-grades.csv")

    symbol_table = table(
        ["Symbol", "Characteristic", "Category", "Datum", "Codepoint", "Unicode name", "Dedicated", "ASME Y14.5-2018", "ISO 1101"],
        [
            [
                glyph(r["symbol"]),
                html.escape(r["characteristic"]),
                html.escape(r["category"]),
                html.escape(r["datum_required"]),
                html.escape(r["codepoint"]),
                html.escape(r["unicode_name"]),
                html.escape(r["codepoint_dedicated_to_gdt"]),
                status_cell(r["asme_y14_5_2018"]),
                status_cell(r["iso_1101"]),
            ]
            for r in symbols
        ],
        "14 geometric characteristics, with ASME Y14.5-2018 and ISO 1101 status",
    )
    modifier_table = table(
        ["Symbol", "Modifier", "Meaning", "Codepoint", "Unicode name", "Dedicated", "Note"],
        [
            [
                glyph(r["symbol"]),
                html.escape(r["modifier"]),
                html.escape(r["meaning"]),
                html.escape(r["codepoint"]),
                html.escape(r["unicode_name"]),
                html.escape(r["codepoint_dedicated_to_gdt"]),
                html.escape(r.get("note") or ""),
            ]
            for r in modifiers
        ],
        "15 material-condition and drafting modifiers",
    )
    roughness_table = table(
        ["Grade", "Ra (µm)", "Ra (µin, conventional)"],
        [
            [html.escape(r["grade"]), html.escape(r["ra_um"]), html.escape(r["ra_uin_conventional"])]
            for r in roughness
        ],
        "ISO 1302 N-grades N1–N12. N9 is 6.3 µm, not 6.4; N7 is 63 µin, not 64.",
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GD&amp;T symbols and surface-roughness grades as verified Unicode data</title>
<meta name="description" content="Machine-readable GD&amp;T characteristic symbols, modifiers and ISO 1302 N-grades. Glyphs and names are re-derived from the Unicode Character Database. ASME Y14.5-2018 withdrew concentricity and symmetry; ISO 1101 retains them.">
<link rel="canonical" href="https://makenexa.github.io/engineering-reference-data/">
<style>
:root {{ color-scheme: light; }}
body {{ font: 16px/1.45 system-ui, "Segoe UI", sans-serif; margin: 0 auto; max-width: 72rem; padding: 1.5rem 1rem 3rem; color: #1a1a1a; }}
h1 {{ font-size: 1.6rem; margin: 0 0 0.5rem; }}
h2 {{ font-size: 1.2rem; margin: 2rem 0 0.6rem; }}
p, li {{ max-width: 46rem; }}
.lede {{ font-size: 1.05rem; }}
table {{ border-collapse: collapse; width: 100%; margin: 0.8rem 0 1.2rem; font-size: 0.92rem; }}
th, td {{ border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: left; vertical-align: top; }}
th {{ background: #f3f3f3; }}
caption {{ caption-side: bottom; text-align: left; padding-top: 0.4rem; color: #444; }}
.glyph {{ font-size: 1.35rem; font-family: "Segoe UI Symbol", "Noto Sans Symbols 2", "DejaVu Sans", sans-serif; }}
.active {{ }}
.withdrawn {{ background: #fff3cd; }}
code {{ font-size: 0.9em; }}
footer {{ margin-top: 2.5rem; border-top: 1px solid #ddd; padding-top: 0.8rem; color: #444; font-size: 0.92rem; }}
a {{ color: #0b4f8a; }}
</style>
</head>
<body>
<h1>GD&amp;T symbols and ISO 1302 N-grades</h1>
<p class="lede">Plain-text reference tables for mechanical drawings. Every glyph and character name below is re-derived from the Unicode Character Database by <code>tools/verify.py</code> in <a href="{REPO}">this repository</a>. CSV is the source of truth; this page is generated from it.</p>
<p>This is not a standard. The controlling document is the revision your drawing cites. Where these tables and a standard disagree, the standard is right.</p>

<h2>Geometric characteristics</h2>
<p>ASME Y14.5-2009 carried 14 geometric characteristic symbols. The 2018 edition withdrew concentricity and symmetry, leaving 12. Both remain <strong>active in ISO 1101</strong>, so an ISO drawing may still carry either and is not out of date. Form controls never reference a datum; orientation, location and runout always do.</p>
<p>Six characteristics have a Unicode codepoint assigned to them by name. The rest borrow a geometry or arrow character. Borrowed glyphs are the usual reason a PDF shows a box instead of a symbol.</p>
{symbol_table}

<h2>Modifiers</h2>
<p>Circled-letter modifiers have no dedicated GD&amp;T codepoint. RFS is listed because drawings still show it; under current ASME practice it applies by default and the symbol is not used.</p>
{modifier_table}

<h2>ISO 1302 roughness grades</h2>
<p>These are the preferred Ra numbers from ISO 1302, not a conversion table. N-grades are not used in ISO 21920-1:2021, which replaced ISO 1302 for new surface-texture specifications; they remain on drawings in circulation. There is no fixed Ra-to-Rz multiplier; this dataset does not print one.</p>
{roughness_table}

<h2>Check it yourself</h2>
<pre><code>git clone {REPO}.git
python tools/verify.py</code></pre>
<p>The verifier re-derives every codepoint from your local Unicode database, checks that concentricity and symmetry are withdrawn in ASME Y14.5-2018 and active in ISO 1101, and checks that the N-grade Ra series is the ISO 1302 preferred numbers (6.3 µm / 63 µin, not 6.4 / 64).</p>
<p>Human-readable drawing checklist that uses the same 14-row split: <a href="{COMPANION}">{COMPANION}</a></p>
<footer>
<p>Maintained by <a href="https://makenexa.com">MakeNexa</a>. Dataset licensed CC0 1.0. Unicode character names are copyright Unicode, Inc.</p>
</footer>
</body>
</html>
"""
    SITE.mkdir(exist_ok=True)
    out = SITE / "index.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
