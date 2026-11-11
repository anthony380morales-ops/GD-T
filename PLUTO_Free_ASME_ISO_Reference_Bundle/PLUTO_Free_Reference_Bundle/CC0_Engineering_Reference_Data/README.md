# PLUTO seed reference data (CC0 1.0)

These CSV/JSON tables are copied from the public GitHub project [makenexa/engineering-reference-data](https://github.com/makenexa/engineering-reference-data). Its LICENSE file dedicates the data to the public domain under CC0 1.0. Source commit/repository state should be rechecked before production ingestion.

## Included
- `data/gdt-symbols.csv` and `.json`: 14 characteristic symbol records, categories, datum flags, Unicode codepoints, and the source project's ASME Y14.5-2018 vs ISO 1101 status labels.
- `data/gdt-modifiers.csv` and `.json`: 15 modifier/annotation symbol records.
- `data/surface-roughness-grades.csv` and `.json`: legacy ISO 1302 N1-N12 Ra values.
- `LICENSE_CC0-1.0.txt`: CC0 statement from the source repository.

## Critical limitations
1. This is a convenience seed dataset, not a copy of ASME Y14.5 or ISO 1101, and not a normative interpretation source.
2. The source project is a small third-party reference dataset. Its verifier checks Unicode identity, row counts, certain status labels, a category-to-datum flag rule, and synchronization between CSV and JSON. It does not establish that the full technical interpretation complies with the standards or that every mapping is correct for all drafting conventions.
3. The N-grade Ra table is explicitly historical ISO 1302 data. ISO 21920-1:2021 replaced ISO 1302 for new profile surface-texture indications; do not use the N-grade table as the current ISO 21920 surface-texture rules.
4. The source data says ASME Y14.5-2018 withdrew concentricity and symmetry while ISO 1101 retains them. This is a quick edition-awareness flag; PLUTO must verify the cited standard and edition for each drawing.
5. Never infer engineering acceptability or release a drawing from these tables alone. Use licensed standards, verified test cases, and qualified engineering review.

## Source and verification
- Source repository: https://github.com/makenexa/engineering-reference-data
- Source data directory: https://github.com/makenexa/engineering-reference-data/tree/main/data
- Dataset rendered reference: https://makenexa.github.io/engineering-reference-data/
- Unicode verification script: https://github.com/makenexa/engineering-reference-data/blob/main/tools/verify.py
- License: CC0 1.0
