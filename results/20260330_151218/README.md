# Booking.com Social Media Engagement Study - Complete Results
## Generated: 2026-03-30 15:12:18

This directory contains the complete statistical analysis results for the Booking.com social media engagement study, including Python computation process and outputs.

## Directory Structure

```
results/20260330_151218/
├── Comprehensive_Results_Report.pdf    ← MAIN PDF REPORT (22 pages)
├── README.md                          ← This file
├── tex_source/                        ← LaTeX source files
│   └── Comprehensive_Results_Report.tex
├── python/                            ← Python analysis outputs
│   ├── report.html                    ← Full HTML statistical report
│   ├── stats_analysis.csv             ← Descriptive statistics
│   ├── correlation_matrix.csv         ← Pearson correlation matrix
│   ├── correlation_significance.csv   ← Correlation with significance stars
│   ├── regression_results.txt         ← Regression coefficients & tests
│   └── plots/                         ← Saved plot PNG files
├── plots/                             ← Diagnostic plots (linked to PDF)
│   ├── residual_histogram.png
│   ├── qq_plot.png
│   ├── resid_vs_fitted.png
│   ├── dist_by_question.png
│   └── qq_by_question.png
└── data/                              ← Research data
    └── research_data.csv              ← Canonical dataset (N=766)
```

## Main Report: Comprehensive_Results_Report.pdf

The main PDF report (22 pages) includes:

### Part 1: Research Framework
- Executive Summary (English & Chinese)
- Research Question & Hypotheses
- Model Specification & Variables
- Data Description

### Part 2: Statistical Analysis
- **Descriptive Statistics** (Table 1)
  - N = 766 observations
  - All variables: mean, SD, quartiles, skewness

- **Correlation Analysis** (Table 2)
  - Full Pearson correlation matrix
  - Significance levels indicated

- **Regression Analysis** (Table 3-6)
  - Model diagnostics (heteroscedasticity, normality, multicollinearity)
  - Robust OLS with HC1 standard errors
  - VIF values (all < 2.0, no multicollinearity)

- **Visual Diagnostics**
  - Residual plots
  - Q-Q plots
  - Distribution by groups

### Part 3: Results & Verification
- Hypothesis testing results
- Coefficient interpretation
- Model verification against proposal
- Managerial implications

### Part 4: Appendix
- Technical details
- Software & packages used
- References

## Key Findings

### Model Performance
- **R² = 0.4924** (49.2% variance explained)
- **N = 766** posts from Booking.com X account
- **Time period:** 2021-11-01 to 2022-11-21
- **All VIF < 2.0** (no multicollinearity issues)

### Hypothesis Test Results

| Hypothesis | Variable | Prediction | Result | Coefficient | p-value | Decision |
|------------|----------|------------|--------|-------------|---------|----------|
| H1 | Text Length | Positive (+) | **Negative** | -0.021*** | <.0001 | **REJECTED** |
| H2 | Question Mark | Positive (+) | Positive | 0.479*** | 0.0006 | SUPPORTED |
| H3 | Emotional Valence | Positive (+) | Positive | 0.084** | 0.0052 | SUPPORTED |
| H4 | Hashtag Count | Positive (+) | Positive | 1.096*** | <.0001 | SUPPORTED |
| H5 | Emoji Count | Positive (+) | Positive | 0.343*** | 0.0002 | SUPPORTED |

**Significance levels:** *** p<.001, ** p<.01, * p<.05

### Key Managerial Insights

1. **Brevity Wins**: Shorter posts generate higher engagement (contrary to H1)
2. **Questions Drive Interaction**: Posts with question marks see 61.5% higher engagement
3. **Positive Tone Matters**: Emotional valence increases engagement by 8.8% per unit
4. **Hashtags Are Powerful**: Each hashtag nearly triples engagement (199% increase)
5. **Emojis Work**: Each emoji boosts engagement by 41%

## Python Analysis Details

All analyses were conducted using:
- **Script:** `analysis/python/run_statistics.py` (v2.0.0)
- **Python packages:** pandas, numpy, scipy, statsmodels, matplotlib
- **Statistical method:** Robust OLS regression with HC1 standard errors
- **Diagnostic tests:** Breusch-Pagan, Shapiro-Wilk, VIF analysis

### Output Files

1. **report.html** - Full interactive HTML report with all tables and plots
2. **stats_analysis.csv** - Descriptive statistics for all variables
3. **correlation_matrix.csv** - Pearson correlation values
4. **correlation_significance.csv** - Correlations with significance stars
5. **regression_results.txt** - Plain text regression summary
6. **plots/*.png** - All diagnostic and exploratory plots

## Verification Status

✅ All results verified against original proposal:
- ✅ Model specification matches proposal
- ✅ Variable definitions align with proposal
- ✅ Sample size (N=766) confirmed
- ✅ Statistical methods correctly implemented
- ✅ Results consistent with theoretical framework
- ✅ All hypotheses properly tested
- ✅ Diagnostic checks completed (heteroscedasticity, normality, multicollinearity)

## Reproducibility

To reproduce these results:
1. Ensure Python packages are installed: `pip install pandas numpy scipy statsmodels matplotlib openpyxl`
2. Run: `python analysis/python/run_statistics.py`
3. Outputs will be generated in `analysis/python/output/`

## Contact & Citation

For questions about this analysis, please refer to:
- **Repository:** jamexhuang/mkt2026group
- **Course:** MKT2026 Group Project
- **Generated:** 2026-03-30 using Python v2.0.0 statistical scripts

---

**Note:** This is the complete, verified results package for the Booking.com social media engagement study. The main PDF report contains all analyses, interpretations, and managerial recommendations.
