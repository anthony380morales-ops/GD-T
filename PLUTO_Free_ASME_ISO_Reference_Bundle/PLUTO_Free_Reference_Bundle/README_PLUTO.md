# PLUTO free ASME / ISO reference acquisition bundle

Prepared 2026-11-11. This package intentionally separates **freely reusable data** from **free-to-download but copyrighted learning PDFs** and **paid/copyrighted standards**.

## What is attached

`CC0_Engineering_Reference_Data/` contains actual CSV/JSON reference tables copied from `makenexa/engineering-reference-data` under that project's CC0 1.0 license, plus the source license and citation. These are machine-readable seed data for symbols, modifiers, and legacy surface roughness N-grades.

`Source_Links/PLUTO_reference_download_register.csv` contains direct download links or official product pages, editions, rights notes, and recommended PLUTO applications.

## Important legal distinction

- **Do not expect full ASME/ISO standards to be free.** ASME confirms its standards are copyrighted. ISO likewise protects standard text and its copyright page states that use of ISO standards content for ML/AI training or enabling AI requires permission except the specified Open Data resources.
- Official ASME/ISO product pages may expose a free preview, but a preview is not the complete standard. Buy/license the complete editions PLUTO actually needs.
- ISO Open Data is machine-readable and licensed ODC-By 1.0, but contains catalogue metadata (titles, status, editions, scopes, committees, ICS, etc.), not the technical clauses of the standards.
- NIST and DOE learning PDFs are freely downloadable through the linked official/host pages. Free download does not always mean permission to republish or ingest into commercial AI training. Check the particular document's notices and obtain permission where unclear.
- The DOE handbooks are old training references and explicitly not current ASME/ISO authorities.
- NPL guides are downloadable but contain copyright notices; obtain permission for AI training or redistribution.

## High-priority full standards to license

### ASME
- Y14.5-2018 (R2024): GD&T rules.
- Y14.100-2017: drawing practices.
- Y14.35-2025: revisions.
- Y14.41-2026: digital product definition.
- Y14.3-2012 (R2024): orthographic/pictorial views.
- Y14.43-2011 (R2020): gages and fixtures.
- Y14.45-2021: measurement data reporting.
- Y14.47-2023: model organization practices.

### ISO
- 1101:2017: geometrical tolerancing.
- 5459:2024: datums and datum systems.
- 5458:2018: pattern and combined geometrical specifications.
- 2692:2021: maximum/least material and reciprocity requirements.
- 8015:2011: GPS fundamentals.
- 22081:2021: general geometrical and size specifications.
- 14253-1:2017: inspection decision rules.
- 21920-1:2021: surface texture indication.
- 10303-242:2025: STEP AP242 and semantic product/manufacturing information.

## Machine-readable CC0 data limitations

The source project's own README explicitly calls its tables convenience reference data, not a standard. The 14-row geometric-characteristic table is intentionally small; the modifier table is a selection, not a complete symbol/annotation grammar. The N1-N12 table is historical ISO 1302 data. ISO 21920-1:2021 replaced ISO 1302 for new profile surface-texture indications and is currently under revision, so do not treat N-grades as the current ISO 21920 rule set.

## Suggested implementation

1. Ingest the CC0 CSV/JSON as a **seed registry only**.
2. Store source, license, standard, edition, applicability and confidence for every datum.
3. Build ASME and ISO rule modules separately. Do not merge their semantics or assume one standard's symbols/defaults apply to the other.
4. License current ASME/ISO standards for the relevant business jurisdictions/contracts and record AI-ingestion permission explicitly.
5. Use NIST PMI test cases (FTC/STC/CTC) and their STEP AP242/definitions/verification results as engineering conformance benchmarks.
6. Keep training examples separate from held-out validation drawings. Require qualified human approval for any engineering release.

## Source repositories and policies

- CC0 dataset: https://github.com/makenexa/engineering-reference-data
- CC0 legal text: https://creativecommons.org/publicdomain/zero/1.0/legalcode
- ASME copyright: https://www.asme.org/codes-standards/find-codes-standards/use-of-asme-copyrighted-information
- ISO Open Data: https://www.iso.org/open-data.html
- ISO copyright / ML-AI use: https://www.iso.org/copyright.html
