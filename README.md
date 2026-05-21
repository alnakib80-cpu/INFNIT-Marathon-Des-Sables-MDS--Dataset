# INFNIT™ Marathon des Sables Dataset 1986–2026

**The most comprehensive Marathon des Sables performance dataset ever assembled.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

---

## Overview

24,163 anonymised athlete records across 40 editions of the Marathon des Sables (MDS) — 1986 through the 40th edition in 2026.

| Metric | Value |
|--------|-------|
| Total records | 24,163 |
| Editions covered | 40 (1986–2026, 2020 cancelled) |
| Finisher records | 23,183 |
| DNF records with stage dropout | 922 |
| Full detail years | 2021–2026 |
| Finisher-only years | 1986–2019 |

**Anonymisation:** Names, club affiliations, and bib numbers removed prior to release (UK GDPR Article 5(1)(c)). Performance, demographic, and stage dropout data fully retained.

---

## What Makes This Dataset Unique

- **922 DNF records with exact stage dropout** — first public dataset to capture where athletes withdrew at checkpoint level
- **40 years of finisher data** — longest longitudinal MDS record publicly available
- **Survival phase transition** — Stage 4 (~91km) accounts for 41% of DNFs in normal conditions
- **Dual-source** — DUV Statistik (1986–2019) + LiveTrail API (2021–2026)

---

## Key Findings

- S4 dominant collapse: 41.2% of DNFs in 2026 — long stage effect confirmed
- S2 pacing failure: Stage 2 DNFs were 32.8% faster than finisher pace at dropout
- Post-S5 survival: effectively zero attrition after Stage 5
- 2021 heat anomaly: 44.6% DNF rate — October extreme heat edition
- Velocity tiers: ELITE 2.10 m/s | MID 1.57 m/s | BACK 1.11 m/s

---

## Files

```
dataset/
├── INFNIT_MDS_DATASET.csv     # Master dataset (24,163 rows, anonymised)
├── data_dictionary.md         # Column definitions + anonymisation statement
└── editions_reference.md      # Edition history

docs/
├── kaggle_dataset_card.md     # Kaggle description
├── zenodo_metadata.md         # Zenodo deposit fields
└── citation.bib               # BibTeX

provenance/
└── methodology.md             # Data collection + anonymisation methodology
```

---

## Quick Start

```python
import pandas as pd

df = pd.read_csv('dataset/INFNIT_MDS_DATASET.csv')

dnf = df[(df['status'] == 'WITHDRAWN') & df['last_stage'].notna()]
print(dnf['last_stage'].value_counts().sort_index())
```

---

## Citation

```bibtex
@dataset{alnakib_mds_2026,
  author    = {Al Nakib, Faisal},
  title     = {INFNIT™ Marathon des Sables Dataset 1986–2026},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.XXXXXXX},
  url       = {https://github.com/alnakib80-cpu/INFNIT-MDS-Dataset}
}
```

---

## Author

**Faisal Al Nakib** | MA AI, University of Southampton | INFNIT™ Founder | UK IPO UK00004363115

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Sources

- DUV Statistik (statistik.d-u-v.org) — 1986–2019
- LiveTrail (livetrail.net) — 2021–2026
