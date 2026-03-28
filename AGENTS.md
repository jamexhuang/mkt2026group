# AGENTS.md — MKT2026 Group Project

Guide for AI agents (Claude, Copilot, etc.) working on this repository.

---

## Project Overview

**Research question:** How do textual features in Booking.com's posts on X (Twitter) influence social media engagement?

**Dataset:** 766 Booking.com posts from 2021-11-01 to 2022-11-21, scraped via Apify.
**Assignment:** MKT2026 group paper, deadline Friday 15 May.

---

## Repository Structure

```
mkt2026group/
├── data/                    # datasets and data documentation
│   ├── research_data.csv      # canonical dataset (766 rows × 37 cols) — DO NOT MODIFY
│   ├── brand_personality.xlsx # sincerity lexicon used in NLP pipeline
│   ├── column_mapping.md      # data dictionary for all 37 columns
│   └── raw/                   # original Excel before processing
│
├── analysis/                # all statistical analysis
│   ├── python/
│   │   ├── run_statistics.py  # main Python stats script (v1.1.0)
│   │   └── output/            # descriptive stats, correlations, regression TXT
│   └── sas/
│       ├── Booking_Engagement_Analysis.sas  # SAS script (v1.0.0)
│       ├── input/             # sas_ready.csv (written by run_statistics.py)
│       └── output/            # SAS-generated output (populated after SAS run)
│
├── paper/                   # reference papers for validation
│   ├── pdf/                   # 9 reference PDFs
│   └── txt/                   # text extracts for validation (add as needed)
│
├── proposal/                # bilingual (EN+ZH) LaTeX proposal
│   ├── Bookingcom_Bilingual_Proposal.tex
│   └── Bookingcom_Bilingual_Proposal.pdf
│
├── docs/                    # project documentation
│   └── citation_check_report.md
│
└── legacy/                  # archived code — do not run or modify
    ├── notebooks/             # original Colab notebook
    ├── scripts/               # exported Python scripts from notebook
    └── old-analysis/          # superseded stats scripts from paper/
```

---

## Analysis Pipeline

Run steps 1 → 2 in order:

### Step 1 — Python (generates stats + SAS input)
```bash
cd /workspaces/mkt2026group
pip install pandas numpy scipy statsmodels openpyxl
python analysis/python/run_statistics.py
```
Outputs:
- `analysis/python/output/stats_analysis.csv`
- `analysis/python/output/correlation_matrix.csv`
- `analysis/python/output/correlation_significance.csv`
- `analysis/python/output/regression_results.txt`
- `analysis/sas/input/sas_ready.csv`  ← SAS input

### Step 2 — SAS (run after Step 1)
1. Open `analysis/sas/Booking_Engagement_Analysis.sas` in SAS or SAS Studio
2. Verify `%LET datapath` at the top points to the absolute path of `analysis/sas/input/sas_ready.csv`
3. Submit the file
4. SAS output goes to `analysis/sas/output/`

> **SAS path note:** SAS resolves `%LET datapath` at runtime as an absolute path. The default in the script is set to `/workspaces/mkt2026group/analysis/sas/input/sas_ready.csv` (Codespaces / Linux). Update this if running on Windows or in SAS Studio with a different mount path.

---

## Research Context

### Hypotheses
| ID | Variable | Direction | Result |
|----|----------|-----------|--------|
| H1 | Text length | + engagement | **Rejected** (β = −0.022***) |
| H2 | Question mark (dummy) | + engagement | Supported |
| H3 | Emotional valence | + engagement | Supported |
| H4 | Hashtag count | + engagement | Supported |

### DV
`log_engagement = log(1 + like + comment + share)`

### Controls
`picture`, `url`, `at_mention`

### Extension variable (Model 2)
`emoji`

### Model fit
- Model 1 R² = 0.46
- Model 2 R² = 0.49
- All VIFs < 5 (no multicollinearity issues)

---

## Key Data Columns (`data/research_data.csv`)

| Column | Role |
|--------|------|
| `like`, `comment`, `share` | Raw engagement components |
| `length` | Word count of tweet text |
| `question` | 1 if post contains "?", else 0 |
| `valence` | Emotional valence score (NLP) |
| `hashtag` | Number of hashtags |
| `picture` | Number of images |
| `url` | Number of URLs |
| `at_mention` | Number of @mentions |
| `emoji` | Number of emoji |

Full schema: `data/column_mapping.md`

---

## Reference Papers

All 9 cited papers are in `paper/pdf/`. Text extracts (if created) go in `paper/txt/`.

| File | Topic |
|------|-------|
| `Gkikas2022.pdf` | Text length & hashtag effects on engagement |
| `Harst2024.pdf` | "Less is more" content design |
| `Ko2022.pdf` | Emoji effects on brand engagement |
| `Kumar2022.pdf` | Hashtag strategy and engagement |
| `Li2020.pdf` | Image content and engagement |
| `Mohammad2024.pdf` | Hotel brand engagement on social media |
| `Moran2020.pdf` | Content features and engagement |
| `Reddy2024.pdf` | Sentiment analysis and engagement |
| `Vries2012.pdf` | Question marks as interactivity cues |

---

## What Agents Can Help With

- Editing or extending `analysis/python/run_statistics.py` (add new tests, variables)
- Editing `analysis/sas/Booking_Engagement_Analysis.sas` (add SAS PROCs)
- Updating `proposal/Bookingcom_Bilingual_Proposal.tex` (LaTeX edits)
- Interpreting results in `analysis/python/output/regression_results.txt`
- Extracting text from PDFs in `paper/pdf/` to `paper/txt/`
- Updating `data/column_mapping.md`

## What Agents Should NOT Do

- Modify `data/research_data.csv` directly (it is the canonical processed dataset)
- Delete or modify anything under `legacy/`
- Move `paper/pdf/` content — PDFs are reference-only
