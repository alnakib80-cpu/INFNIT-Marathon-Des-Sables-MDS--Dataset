# Data Dictionary — INFNIT™ Marathon des Sables Dataset 1986–2026

## Anonymisation Statement

Athlete names, club affiliations, and bib numbers have been removed from this dataset prior to public release in accordance with data minimisation principles (UK GDPR Article 5(1)(c)). The `name`, `club`, and `bib` columns are present in the schema but contain null values throughout. The scientific value of the dataset — performance distributions, survival analysis, stage dropout patterns — is unaffected. Full records are retained by the author.

---

## Column Reference

| Column | Type | Description | Availability |
|--------|------|-------------|--------------|
| `year` | int | Edition year | All editions |
| `edition` | int | Edition number (1 = 1986, 40 = 2026) | All editions |
| `status` | str | Athlete outcome: `FINISHER`, `WITHDRAWN`, `ON_RACE`, `OUT_OF_TIME`, `STOPPED_BY_ORGANIZATION` | All editions |
| `data_completeness` | str | `FULL` (2021–2026) or `FINISHER_ONLY` (1986–2019) | All editions |
| `source` | str | `DUV` or `LiveTrail` | All editions |
| `rank` | int | Overall scratch rank within edition | All editions |
| `finish_hours` | float | Total race time in decimal hours | All editions |
| `performance` | str | Race time formatted as HH:MM:SS h | All editions |
| `name` | str | **Removed — null throughout** (anonymised prior to release) | None |
| `club` | str | **Removed — null throughout** (anonymised prior to release) | None |
| `bib` | float | **Removed — null throughout** (anonymised prior to release) | None |
| `nationality` | str | Country code: 2-letter ISO (LiveTrail) or 3-letter IOC (DUV) | Most records |
| `gender` | str | `M` or `F` | Most records |
| `yob` | float | Year of birth | DUV records only |
| `age_cat` | str | Age/gender category (e.g. M0 M, M4 W, M35) | Most records |
| `rank_gender` | float | Rank within gender group | Most records |
| `rank_cat` | float | Rank within age/gender category | Most records |
| `avg_speed` | float | Average speed km/h | DUV records only |
| `age_graded` | str | Age-graded performance time | DUV records only |
| `tier` | str | Performance tier: `ELITE` (top 10%), `MID` (10–40%), `BACK` (40–100%) | DUV records |
| `last_stage` | float | Stage of withdrawal (DNFs) or 6 (finishers). LiveTrail 2021–2026 only. | LiveTrail 2021–2026 |
| `event_name` | str | Full event name string | All editions |
| `distance` | str | Race distance descriptor | All editions |
| `date` | str | Event date | DUV records |
| `event_id` | float | DUV internal event ID | DUV records only |

---

## Status Values

| Status | Description |
|--------|-------------|
| `FINISHER` | Completed all 6 stages within time limits |
| `WITHDRAWN` | Voluntarily withdrew during the race (DNF) |
| `OUT_OF_TIME` | Exceeded stage time limit |
| `ON_RACE` | Still racing at data capture time (2023 data artefact) |
| `STOPPED_BY_ORGANIZATION` | Withdrawn by race medical/organisation |

---

## Stage Reference (2026 Edition)

| Stage | Distance | Point ID Range | Start Date |
|-------|----------|----------------|------------|
| 1 | ~35 km | 0–19 | 5 Apr 2026 |
| 2 | ~40 km | 20–29 | 6 Apr 2026 |
| 3 | ~29 km | 30–39 | 7 Apr 2026 |
| 4 (Long) | ~91 km | 40–59 | 8 Apr 2026 |
| 5 | ~42 km | 60–69 | 10 Apr 2026 |
| 6 | ~33 km | 70–79 | 11 Apr 2026 |

---

## Data Completeness by Year

| Years | Source | Finishers | DNFs | Fields Available |
|-------|--------|-----------|------|-----------------|
| 1986–2019 | DUV Statistik | ✓ | ✗ | rank, nationality, time, tier, gender, yob, age_cat |
| 2021–2026 | LiveTrail | ✓ | ✓ | rank, time, last_stage, nationality, gender, age_cat |

**Notes:** 2020 absent (COVID-19 cancellation). name/club/bib null throughout.

---

## Quick Start

```python
import pandas as pd

df = pd.read_csv('dataset/INFNIT_MDS_DATASET.csv')

# DNF stage distribution
dnf = df[(df['status'] == 'WITHDRAWN') & df['last_stage'].notna()]
print(dnf['last_stage'].value_counts().sort_index())

# Median finish time by year
finishers = df[df['status'] == 'FINISHER']
print(finishers.groupby('year')['finish_hours'].median().round(1))
```
