# INFNIT™ Marathon Des Sables Dataset 1986–2026

The most complete Marathon Des Sables results dataset ever compiled, combining DUV historical records with LiveTrail stage-level data across 40 editions from 1986 to 2026.

**24,163 records | 1986–2026 | 40 editions | 2,201 DNFs | 100+ nationalities**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20340189.svg)](https://doi.org/10.5281/zenodo.20340189)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Coverage

| Field | Value |
|-------|-------|
| Total records | 24,163 |
| Years | 1986–2026 |
| Editions | 40 |
| Finishers | 23,183 |
| DNFs | 2,201 |
| DNF data available | 2019–2026 (LiveTrail) |

---

## Key DNF Statistics

| Year | Total | DNF | DNF Rate |
|------|-------|-----|----------|
| 2019 | 1,568 | 86 | 5.5% |
| 2021 | 1,367 | 659 | **48.2%** |
| 2022 | 1,922 | 327 | 17.0% |
| 2023 | 2,212 | 688 | 31.1% |
| 2024 | 1,702 | 147 | 8.6% |
| 2025 | 1,792 | 99 | 5.5% |
| 2026 | 2,885 | 195 | 6.8% |

*2021 extreme heat edition — 48.2% DNF rate confirms survival phase transition finding.*
*DNF variance across editions: 8.76×*

---

## Columns

| Column | Type | Description |
|--------|------|-------------|
| pseudo_id | str | SHA-256 pseudonymous identifier — no names |
| source_file | str | Data source (DUV or LiveTrail) |
| race_series | str | Race series identifier (MDS) |
| edition | str | Edition identifier |
| year | int | Race year (1986–2026) |
| gender | str | M (male) or F (female) |
| nationality | str | Runner nationality (ISO alpha-3) |
| yob | float | Year of birth |
| age_at_race | float | Age at time of race |
| age_cat | str | Age category |
| tier | str | Performance tier |
| status | str | FINISHER, WITHDRAWN, DID_NOT_START, OUT_OF_TIME |
| dnf_flag | int | 0 (finisher) or 1 (did not finish) |
| rank | float | Overall finishing position |
| rank_gender | float | Finishing position within gender |
| finish_hours | float | Finish time as decimal hours |
| avg_speed | float | Average speed km/h |
| distance_km | float | Race distance in kilometres |
| stage_count | float | Number of stages |
| data_completeness | str | Coverage indicator |

---

## DNF Data Coverage

DNF records are available for 2019–2026 only via LiveTrail. Pre-2019 records are finisher-only from DUV. The `data_completeness` column flags this distinction.

---

## Data Sources

- **DUV Ultramarathon Statistics** (statistik.d-u-v.org) — historical finisher records 1986–2026
- **LiveTrail** (livetrail.net) — individual runner data including DNF status 2019–2026

---

## GDPR Note

Name columns removed. `pseudo_id` is a SHA-256 hash of non-PII fields (source, edition, rank, gender, nationality, yob). No personal identifiers in this dataset. GDPR-compliant for research use.

---

## License

This dataset is released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to share and adapt this material for any purpose, provided appropriate credit is given.

---

## Citation

```
Al-Nakib, F. (2026). INFNIT™ Marathon Des Sables Dataset 1986–2026 (v2.0.0).
Zenodo. https://doi.org/10.5281/zenodo.20340189
```

---

## Related Datasets

- [INFNIT™ DUV Ultramarathon Dataset](https://doi.org/10.5281/zenodo.20341196)
- [INFNIT™ UTMB World Series Dataset](https://doi.org/10.5281/zenodo.20348998)

---

## About INFNIT™

Part of the INFNIT™ research programme — AI-driven ultramarathon performance platform combining BiLSTM, PPO reinforcement learning, and survival analysis for elite endurance racing.

**MA AI, University of Southampton**
**GitHub:** https://github.com/alnakib80-cpu/INFNIT-Marathon-Des-Sables-MDS--Dataset
