# Analysis

Place reproducible analysis scripts here. Do not place restricted or personally identifiable data in this repository.

## Controlled PubMed screening

The 2026-09-07 title/abstract pass uses these scripts:

- `refresh_pubmed_screening.py`: retrieves current PubMed XML through the
  installed NCBI Entrez skill and writes only compact hashes/summaries to Git;
- `screen_pubmed_titles.py`: applies the prospective four-state rubric and
  produces the versioned per-record CSV ledger;
- `verify_screening_release.py`: compares the screened XLSX against the
  pre-screening workbook and runs identity, formula and negative controls;
- `google_screening_requests.py`: reproduces the verified values as native
  Google Sheets `updateCells` requests;
- `build_screening_manifest.py`: hashes the external raw/backup evidence and
  selected repository artifacts.

Raw PubMed XML and full decision JSON are deliberately kept in the external
backup directory named by the run manifest. The scripts do not import Zotero
records, merge items or make an article Claim-Ready.
