# Release Instructions
## INFNIT™ Marathon des Sables Dataset 1986–2026

Follow these steps in order.

---

## Step 1 — GitHub (already done ✓)

Repo: https://github.com/alnakib80-cpu/INFNIT-MDS-Dataset

Add remaining files:
```powershell
cd E:\INFNIT\Vault\UltraMarathon
# Copy release package files into repo
xcopy /E /I "C:\path\to\INFNIT_MDS_Release\*" "E:\INFNIT\Vault\UltraMarathon\"
git add .
git commit -m "Add README, data dictionary, docs, provenance"
git push -u origin master
```

---

## Step 2 — Zenodo (get DOI first)

1. Go to https://zenodo.org
2. Sign in with GitHub account
3. Click **New Upload**
4. Upload these files:
   - `dataset/INFNIT_MDS_DATASET.csv`
   - `README.md`
   - `dataset/data_dictionary.md`
   - `provenance/methodology.md`
5. Fill metadata from `docs/zenodo_metadata.md`
6. Set licence: **CC BY 4.0**
7. Click **Publish**
8. Copy the DOI (format: 10.5281/zenodo.XXXXXXX)
9. Update `README.md` and `docs/citation.bib` with real DOI
10. Push updated README to GitHub

---

## Step 3 — Kaggle

1. Go to https://kaggle.com/datasets/new
2. Dataset title: `INFNIT Marathon des Sables Dataset 1986-2026`
3. Upload `INFNIT_MDS_DATASET.csv`
4. Paste description from `docs/kaggle_dataset_card.md`
5. Set licence: **CC BY 4.0**
6. Add tags: `ultramarathon`, `sports`, `running`, `survival-analysis`, `endurance`
7. Add Zenodo DOI to description
8. Publish
9. Create a linked notebook (EDA) — use `notebooks/02_exploratory_analysis.ipynb`

---

## Step 4 — Tweet / LinkedIn announcement

Suggested post:

> Releasing the INFNIT™ Marathon des Sables Dataset 1986–2026 — 24,163 records, 40 editions, and the first public dataset with 922 DNF records showing exactly which stage athletes withdrew. 
>
> Built as part of my AI research on ultramarathon survival prediction.
>
> Free on Kaggle + Zenodo (CC BY 4.0)
> [Kaggle link] | [Zenodo DOI] | [GitHub]
>
> #ultramarathon #MarathonDesSables #sportsanalytics #opendata #AI

---

## Checklist

- [ ] GitHub repo populated with all release files
- [ ] Zenodo deposit complete — DOI obtained
- [ ] README updated with real DOI
- [ ] Kaggle dataset published
- [ ] Kaggle EDA notebook attached
- [ ] LinkedIn/Twitter announcement posted
- [ ] DOI added to Papers I–IV references
- [ ] Thesis references updated
