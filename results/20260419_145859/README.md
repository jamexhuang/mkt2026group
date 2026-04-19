# Booking.com Social Media Engagement Study - Complete Results (v3.0.0)
## Generated: 2026-04-19

This directory contains the complete statistical analysis results for the Booking.com social media engagement study, v3.0.0 — the English-only filtered version.

**Key change from v2:** Non-English posts (Spanish, French, Portuguese, others) are excluded using `langdetect`. The analysis sample is N=624 English-language posts, down from N=766 in v2.

## Directory Structure

```
results/20260419_145859/
├── Comprehensive_Results_Report.pdf    ← MAIN PDF REPORT (25 pages)
├── README.md                          ← This file
├── VERIFICATION.md                    ← Verification against proposal & v2
├── tex_source/                        ← LaTeX source files
│   └── Comprehensive_Results_Report.tex
├── python/                            ← Python analysis outputs
│   ├── report.html                    ← Full HTML statistical report
│   ├── stats_analysis.csv             ← Descriptive statistics
│   ├── correlation_matrix.csv         ← Pearson correlation matrix
│   ├── correlation_significance.csv   ← Correlation with significance stars
│   ├── regression_results.txt         ← Regression coefficients & tests
│   └── plots/                         ← Saved plot PNG files (8 plots)
├── plots/                             ← Diagnostic plots (root copy)
│   ├── residual_histogram.png
│   ├── qq_plot.png
│   ├── resid_vs_fitted.png
│   ├── dv_distribution.png
│   ├── dist_by_question.png
│   ├── qq_by_question.png
│   ├── boxplot_question.png
│   └── raw_engagement_dist.png
└── data/
    └── research_data_en_only.csv      ← Filtered dataset (English only, N=624)
```

## Language Filter Details

| Category | Count |
|----------|-------|
| Original sample | 766 |
| Non-English removed (langdetect) | 139 |
| Zero-length removed | 3 |
| **Final analysis sample** | **624** |

Non-English posts were detected using the `langdetect` library after removing URLs, @mentions, and hashtags from tweet text.

## Key Findings

### Model Performance
- **R² = 0.5010** (50.1% variance explained — up from 49.2% in v2)
- **N = 624** English-language posts from Booking.com X account
- **Time period:** 2021-11-01 to 2022-11-21
- **All VIF < 2.0** (no multicollinearity issues)

### Hypothesis Test Results

| Hypothesis | Variable | Prediction | Result | Coefficient | p-value | Decision |
|------------|----------|------------|--------|-------------|---------|----------|
| H1 | Text Length | Positive (+) | **Negative** | -0.036*** | <.0001 | **REJECTED** |
| H2 | Question Mark | Positive (+) | Positive | 0.305* | 0.0428 | SUPPORTED |
| H3 | Emotional Valence | Positive (+) | Positive | 0.065* | 0.0299 | SUPPORTED |
| H4 | Hashtag Count | Positive (+) | Positive | 0.904*** | <.0001 | SUPPORTED |
| H5 | Emoji Count | Positive (+) | Positive | 0.286** | 0.0011 | SUPPORTED |

**Significance levels:** *** p<.001, ** p<.01, * p<.05

### Version Comparison (v2 → v3)

| Item | v2 (N=766) | v3 (N=624) | Change |
|------|-----------|-----------|--------|
| R² | 0.4924 | 0.5010 | +0.009 |
| H1 Text Length β | -0.021*** | -0.036*** | Stronger effect |
| H2 Question Mark β | 0.479*** | 0.305* | Attenuated |
| H3 Valence β | 0.084** | 0.065* | Attenuated |
| H4 Hashtag β | 1.096*** | 0.904*** | Attenuated |
| H5 Emoji β | 0.343*** | 0.286** | Attenuated |
| URL Count | 0.169* | 0.149 (n.s.) | Lost significance |
| At-Mention | 0.515* | 0.790** | Stronger |

### Key Managerial Insights

1. **Brevity Wins (Stronger):** Shorter English posts outperform longer ones even more strongly than in v2 (β = -0.036 vs -0.021)
2. **Questions Drive Interaction:** Posts with question marks see 35.6% higher engagement (e^0.305 - 1)
3. **Positive Tone Matters:** Emotional valence increases engagement by 6.7% per unit
4. **Hashtags Are Powerful:** Each hashtag nearly doubles engagement (147% increase, e^0.904 - 1)
5. **Emojis Work:** Each emoji boosts engagement by 33.1% (e^0.286 - 1)

## Quality Checks

| Check | Status | Value |
|-------|--------|-------|
| N in range 620–650 | ✅ | N = 624 |
| All VIF < 5 | ✅ | Max VIF = 1.668 |
| Coefficient signs consistent with v2 | ✅ | No sign flips |
| R² similar to v2 | ✅ | 0.5010 (vs 0.4924) |
| All 8 plots generated | ✅ | plots/*.png |
| PDF compiled cleanly | ✅ | 25 pages |

## Python Analysis Details

- **Script:** `analysis/python/run_statistics.py` (v3.0.0)
- **Language detection:** `langdetect` 1.0.9
- **Statistical method:** Robust OLS regression with HC1 standard errors
- **Diagnostic tests:** Breusch-Pagan, Shapiro-Wilk, VIF analysis

## Reproducibility

To reproduce these results:
1. Install packages: `pip install pandas numpy scipy statsmodels matplotlib langdetect`
2. Run: `python analysis/python/run_statistics.py`
3. Outputs will be generated in a new `results/20260419_HHMMSS/` timestamped directory

## Contact & Citation

For questions about this analysis, please refer to:
- **Repository:** jamexhuang/mkt2026group
- **Course:** MKT2026 Group Project
- **Generated:** 2026-04-19 using Python v3.0.0 statistical scripts

---

**Note:** This is the v3.0.0 English-only results package. For the original v2 results (N=766), see `results/20260330_151218/`. The source data (`data/research_data.csv`) is unchanged.
