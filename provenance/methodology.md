# Data Collection Methodology
## INFNIT™ Marathon des Sables Dataset 1986–2026

---

## 1. DUV Statistik Pipeline (1986–2019)

**Source:** statistik.d-u-v.org

**Method:** Python requests + BeautifulSoup. Results fetched per event per year via DUV geteventlist.php and getresultevent.php with 1.2-second delays and HTTP cache.

**Fields captured:** rank, nationality, yob, gender, age category, finish time, avg_speed, age_graded.

**Limitations:** Finisher records only. 2020 absent (COVID-19 cancellation).

---

## 2. LiveTrail API Pipeline (2021–2026)

**Source:** api.v3.livetrail.net

**Discovery:** Playwright browser automation intercepting XHR requests on LiveTrail athlete pages revealed the tenant pattern: x-tenant: marathondessables_{YYYY}.

**Collection:**
1. Paginated runners list: GET /api/events/runners?raceId=mds&limit=100&page={n}
2. Individual timing: GET /api/events/runners/{bib} — returns raceTime (seconds) and lastPassage.pointId
3. 6,887 total records across 2019, 2021–2026

**DNF Stage Mapping (pointId ranges):**

| Range | Stage |
|-------|-------|
| 0–19 | Stage 1 |
| 20–29 | Stage 2 |
| 30–39 | Stage 3 |
| 40–59 | Stage 4 (Long) |
| 60–69 | Stage 5 |
| 70–79 | Stage 6 |

**Note:** 2019 individual runner endpoint returns HTTP 500. Finish times for 2019 sourced from DUV.

---

## 3. Anonymisation

The following fields were set to null prior to public release (UK GDPR Article 5(1)(c)):

- `name` — athlete full name
- `club` — club affiliation
- `bib` — bib number (publicly assigned but enables re-identification via official start lists)

Verified: all three fields are 100% null across 24,163 records. Full records retained by author.

---

## 4. Dataset Integration

- DUV for 1986–2019, LiveTrail for 2021–2026 — no overlap
- Deduplication: DUV on year+rank+status; LiveTrail on year+bib
- data_completeness flag: FINISHER_ONLY (1986–2019) | FULL (2021–2026)

---

## 5. Known Limitations

1. 2020 absent — MDS cancelled (COVID-19)
2. 2019 DNFs not available — DUV finishers only
3. 2023 ON_RACE (42 athletes) — LiveTrail data freeze artefact
4. Nationality format: DUV 3-letter IOC vs LiveTrail 2-letter ISO
5. Stage distances vary by edition — 2026 Stage 4 was ~91–100km; prior editions ~75–80km
