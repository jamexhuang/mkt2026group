# MKT2026 Group Project — Booking.com Engagement Study

**Research question:** How do textual features in Booking.com's posts on X (Twitter) influence social media engagement?

**Deadline:** Friday, 15 May 14:00 | **Report length:** 2,500 words max | **Weighting:** 50%

---

## Hypotheses

| # | Feature | Expected direction |
|---|---------|-------------------|
| H1 | Text length | + engagement |
| H2 | Question mark | + engagement |
| H3 | Emotional valence | + engagement |
| H4 | Hashtag count | + engagement |

**DV:** `log(1 + like + comment + share)`
**Controls:** picture count, URL count, at-mention count
**Extension (Model 2):** emoji count

---

## Project Structure

```
mkt2026group/
├── AGENTS.md              ← guide for AI agents working on this repo
├── data/
│   ├── research_data.csv    ← canonical dataset (766 posts, 37 columns)
│   ├── brand_personality.xlsx
│   ├── column_mapping.md    ← data dictionary
│   └── raw/                 ← original Excel before processing
├── analysis/
│   ├── python/
│   │   ├── run_statistics.py  ← main stats script (v1.1.0)
│   │   └── output/            ← CSV tables + regression_results.txt
│   └── sas/
│       ├── Booking_Engagement_Analysis.sas
│       ├── input/             ← sas_ready.csv (written by Python script)
│       └── output/            ← SAS output (after running SAS)
├── paper/
│   ├── pdf/               ← 9 reference PDFs
│   └── txt/               ← text extracts for validation
├── proposal/
│   ├── Bookingcom_Bilingual_Proposal.tex
│   └── Bookingcom_Bilingual_Proposal.pdf
├── docs/
│   └── citation_check_report.md
└── legacy/                ← archived code, do not modify
```

---

## Running the Analysis

### 1. Python (descriptive stats + regression + generate SAS input)
```bash
pip install pandas numpy scipy statsmodels openpyxl
python analysis/python/run_statistics.py
```
Outputs → `analysis/python/output/` + `analysis/sas/input/sas_ready.csv`

### 2. SAS (after running Python)
1. Open `analysis/sas/Booking_Engagement_Analysis.sas`
2. Set `%LET datapath` to the absolute path of `analysis/sas/input/sas_ready.csv`
3. Submit in SAS / SAS Studio
4. Results → `analysis/sas/output/`

---

## Key Results (from `analysis/python/output/regression_results.txt`)

- H1 **Rejected** — text length has a significant *negative* effect (β = −0.022***)
- H2, H3, H4 **Supported**
- R² = 0.46 (Model 1), 0.49 (Model 2) | All VIFs < 5

---

## Resources

- Assignment brief: [Google Drive PDF](https://drive.google.com/file/d/17iqkG-H_l4Wc9g-oKvUeguPbRCdVE-H6/view?usp=drive_link)
- Raw data file: [Google Sheets](https://docs.google.com/spreadsheets/d/1Y0Iri6bQY7lxvEwM8ZTtMa_sr-1YaPBD/edit?usp=drive_link&ouid=101577574054266753595&rtpof=true&sd=true)
- Data source: [Apify](https://apify.com/)

---

## Report Outline

1. Background (5%)
2. Content Features and Hypotheses (15%)
3. Data (15%)
4. Measurement of Variables (15%)
5. Model Specifications (15%)
6. Results (15%)
7. Managerial Suggestions (15%)
8. Limitations and Possible Improvements (5%)

---

See `AGENTS.md` for a full technical guide (file paths, pipeline, data schema).

> Original assignment brief and team notes: `legacy/task-notes.md`
