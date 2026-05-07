# Verification Report — Booking.com Engagement Study v5.0.0

**Release tag:** `20260507_155131`
**Generated:** 2026-05-07
**Predecessor:** `20260429_014427` (v4.0.0)
**Scope:** four deliverables (EN+ZH × Comprehensive+Group) plus the regenerated v5.0.0 statistical artifacts, including a Negative Binomial robustness check.

---

## 1. Headline change

The methodological additions in v5.0.0 vs the v4.0.0 baseline are:

1. **Negative Binomial (NB2) robustness check.** The same eight-predictor specification used in OLS is re-fit on the raw integer engagement count via NB2 GLM with HC1 robust standard errors. The dispersion parameter is anchored via the marginal method-of-moments estimator $\hat\alpha_{\text{MoM}}=(s^2(Y)-\bar Y)/\bar Y^2 = 20.21$. A boundary likelihood-ratio test against Poisson rejects equidispersion overwhelmingly ($\chi^2 = 71{,}095$, $p<.0001$). Standard NB is sufficient at 13.6 % zero rate (104/766); ZINB is flagged only as a future-direction note.
2. **Adopted teammate's updated EN draft for Group Final Report sections** Background, Content & Hypotheses, and Data; new reference list in Harvard style with URLs and access dates.
3. **Repaired factual inconsistency**: teammate's Data section claimed non-English tweets were removed, which would not have been consistent with the actual code path; we corrected the prose to state non-English tokens are handled at the measurement stage rather than via row exclusion (preserves N=766 architectural parity with v2.0.0 / v4.0.0).

OLS findings replicate v4.0.0 exactly; the NB check confirms 4/5 hypothesis decisions and surfaces a calibrated qualifier on H3.

| Metric | v4.0.0 | v5.0.0 | Status |
| --- | --- | --- | --- |
| OLS R² | 0.5119 | 0.5119 | replicated exactly |
| Adj. R² | 0.5068 | 0.5068 | replicated exactly |
| F(8, 757) | 76.681 | 76.681 | replicated exactly |
| Max VIF | 1.639 | 1.639 | replicated exactly |
| NB α̂ (MoM) | — | **20.21** | new |
| NB log-likelihood | — | **-3,474.97** | new |
| Poisson log-likelihood | — | **-39,022.60** | new (reference) |
| LR test (NB vs Poisson) | — | **χ² = 71,095, p < .0001** | new |
| AIC NB / Poisson | — | **6,968 / 78,063** | new |
| McFadden pseudo-R² | — | **0.0137** | new |
| OLS↔NB hypothesis concordance | — | **4/5 (H3 marginal)** | new |

✅ Confirmed empirically — NB does verify the OLS conclusions for H1, H2, H4, H5 and surfaces an honest qualifier on H3.

---

## 2. Output inventory (this release)

```
results/20260507_155131/
├── data/
│   └── research_data_v4.csv             # 766 × 38, encoding-clean snapshot
├── plots/
│   └── *.png                            # 9 diagnostic plots (8 OLS + 1 NB)
├── python/
│   ├── plots/*.png                      # mirror copies
│   ├── report.html
│   ├── stats_analysis.csv
│   ├── correlation_matrix.csv
│   ├── correlation_significance.csv
│   ├── regression_results.txt           # OLS HC1 (unchanged from v4.0.0)
│   ├── nb_regression_results.txt        # NEW: NB α, LR test, IRR table, concordance
│   ├── nb_parameter_estimates.csv       # NEW: NB coefficients with IRR + 95% CI
│   └── run_statistics.py                # archived snapshot (v5.0.0)
├── tex_source/
│   ├── Comprehensive_Results_Report_EN.tex   ✅ 21 pp PDF
│   ├── Comprehensive_Results_Report_EN.pdf
│   ├── Comprehensive_Results_Report_ZH.tex   ✅ 21 pp PDF
│   ├── Comprehensive_Results_Report_ZH.pdf
│   ├── Group_Final_Report_EN.tex             ✅ 9 pp PDF
│   ├── Group_Final_Report_EN.pdf
│   ├── Group_Final_Report_ZH.tex             ✅ 8 pp PDF
│   └── Group_Final_Report_ZH.pdf
└── VERIFICATION.md (this file)
```

---

## 3. Group Final Report — word-budget compliance (English)

The EN report follows the assignment brief's per-section budgets.

| Section | Budget | Actual | Δ | % |
| --- | ---: | ---: | ---: | ---: |
| Background | 150 | 158 | +8 | +5.3% |
| Content Features and Hypotheses | 400 | 394 | −6 | −1.5% |
| Data | 350 | 346 | −4 | −1.1% |
| Measurement of Variables | 400 | 380 | −20 | −5.0% |
| Model Specifications | 350 | 343 | −7 | −2.0% |
| Results | 450 | 471 | +21 | +4.7% |
| Managerial Suggestions | 300 | 282 | −18 | −6.0% |
| Limitations and Possible Improvements | 100 | 106 | +6 | +6.0% |
| **TOTAL** | **2,500** | **2,480** | **−20** | **−0.8%** |

✅ Hard cap (≤ 2,500): **PASS**
✅ All sections within ±10 % of brief budget (six of eight within ±5 %)
✅ ZH version mirrors the same section structure (Chinese character count is informational only; the assignment word cap applies to the English version).

---

## 4. Statistical numbers cross-checked between deliverables

The same OLS coefficients and NB IRR / SE / z / p values appear in:
- `regression_results.txt` (OLS, machine output)
- `nb_regression_results.txt` (NB, machine output)
- `nb_parameter_estimates.csv`
- `Comprehensive_Results_Report_EN.tex` Table 1 (OLS) + Table 2 (NB)
- `Comprehensive_Results_Report_ZH.tex` 對應表
- `Group_Final_Report_EN.tex` Table 1 (OLS) + inline NB summary
- `Group_Final_Report_ZH.tex` 表 1 + 內文 NB 摘要

### OLS (HC1 robust SE) coefficient table — identical across all four .tex sources

| Coef | Value | SE(HC1) | t | p | %-effect (OLS) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Intercept | 1.4882 | 0.1069 | 13.92 | <.0001 | n/a |
| TextLength (H1) | −0.0193 | 0.0032 | −5.98 | <.0001 | −1.92% |
| Question (H2) | 0.4687 | 0.1325 | 3.54 | 0.0004 | +59.79% |
| Valence (H3) | 0.0641 | 0.0266 | 2.41 | 0.0161 | +6.62% |
| Hashtag (H4) | 1.0623 | 0.1276 | 8.33 | <.0001 | +189.31% |
| Emoji (H5) | 0.3144 | 0.0834 | 3.77 | 0.0002 | +36.94% |
| Picture (0/1) | 1.1376 | 0.1344 | 8.47 | <.0001 | +211.92% |
| URL (0/1) | 0.1461 | 0.0868 | 1.68 | 0.0923 | +15.73% |
| At-Mention (0/1) | 0.8898 | 0.2433 | 3.66 | 0.0003 | +143.46% |

### NB (HC1 robust SE) coefficient table — identical across all four .tex sources

| Coef | Value | SE(HC1) | z | p | IRR | IRR 95% CI |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Intercept | 1.8878 | 0.2210 | 8.54 | <.0001 | 6.605 | [4.281, 10.190] |
| TextLength (H1) | −0.0350 | 0.0058 | −6.01 | <.0001 | 0.966 | [0.954, 0.977] |
| Question (H2) | 0.9253 | 0.3173 | 2.92 | 0.0035 | 2.523 | [1.354, 4.701] |
| Valence (H3) | 0.0912 | 0.0554 | 1.65 | 0.0998 | 1.096 | [0.983, 1.221] |
| Hashtag (H4) | 1.0476 | 0.1787 | 5.86 | <.0001 | 2.851 | [2.007, 4.050] |
| Emoji (H5) | 0.3837 | 0.1414 | 2.71 | 0.0066 | 1.468 | [1.113, 1.937] |
| Picture (0/1) | 1.5958 | 0.2732 | 5.84 | <.0001 | 4.932 | [2.886, 8.428] |
| URL (0/1) | 0.4956 | 0.1744 | 2.84 | 0.0045 | 1.641 | [1.166, 2.310] |
| At-Mention (0/1) | 1.6970 | 0.3668 | 4.63 | <.0001 | 5.458 | [2.660, 11.196] |

✅ Identical across all four .tex sources.

---

## 5. Hypothesis decisions (OLS vs NB)

| H | Predicted | OLS β (p) | OLS decision | NB β (p) | NB decision | Match? |
| --- | --- | ---: | --- | ---: | --- | --- |
| H1 Text Length | + | −0.019 (<.001) | Not supported | −0.035 (<.001) | Not supported | ✓ |
| H2 Question | + | +0.469 (<.001) | Supported | +0.925 (.004) | Supported | ✓ |
| H3 Valence | + | +0.064 (.016) | Supported | +0.091 (.100) | **Marginal** | **?** |
| H4 Hashtag | + | +1.062 (<.001) | Supported | +1.048 (<.001) | Supported | ✓ |
| H5 Emoji | + | +0.314 (<.001) | Supported | +0.384 (.007) | Supported | ✓ |

**Concordance: 4/5.** H3 is the only divergence: same positive sign as OLS, but $p$ moves from .016 (OLS) to .100 (NB) and the IRR 95 % CI just touches unity. Reported transparently as "OLS supported, NB marginal" rather than choosing one model post hoc.

---

## 6. Mathematical / statistical correctness checklist

- [x] OLS DV is `ln(1 + Engagement)` via `numpy.log1p`; NB DV is the raw integer count.
- [x] %-effect formula stated as `(exp(β)−1)×100%` for OLS; IRR=`exp(β)` for NB; magnitudes recomputed and match.
- [x] Heteroscedasticity flagged via Breusch–Pagan (LM = 90.22, p < .0001) → HC1 robust SE used in OLS throughout.
- [x] Residual normality acknowledged (Shapiro–Wilk W = 0.968) but framed correctly as a CLT-mitigated concern at N = 766.
- [x] All VIFs reported and below the conventional threshold of 10 (max 1.64).
- [x] NB log-link interpretation: IRR = `exp(α)` for continuous and binary X; binary X interpretation given as ratio E[Y|X=1]/E[Y|X=0].
- [x] NB dispersion parameter α reported with the source method (MoM-anchored at 20.21); CT auxiliary estimator reported for diagnostic comparison.
- [x] LR test against Poisson reported with the correct boundary `½·χ²(1)` p-value (chi-bar-squared mixture).
- [x] AIC and BIC reported on a likelihood-based scale (manually computed `-2·llf + k·log(N)`) for clean Poisson↔NB comparability — statsmodels' GLM `.bic` defaults to a deviance-based convention which is not directly comparable to the discrete model's `.bic`.
- [x] McFadden pseudo-R² reported and acknowledged as not directly comparable to OLS R² on `ln(1+Y)`.
- [x] Standard NB sufficiency justified by 13.6% zero rate; ZINB / hurdle relegated to future-direction note in Limitations.
- [x] Equation in the Group Report uses real variable names (TextLength, Question, …) per assignment brief.
- [x] Results discussion uses correlational language; no causal claims.
- [x] Each hypothesis explicitly evaluated as Supported / Not Supported / Marginal, with OLS and NB columns side by side.
- [x] H3 OLS↔NB divergence flagged honestly in all four .tex deliverables.

---

## 7. Editorial / formatting checklist

- [x] All four PDFs use **Times New Roman** for English text (verified via `pdffonts`):
  - Comprehensive_EN: TimesNewRomanPSMT + TimesNewRomanPS-BoldMT
  - Comprehensive_ZH: TimesNewRomanPSMT + Bold + Italic
  - Group_EN: TimesNewRomanPSMT + Bold
  - Group_ZH: TimesNewRomanPSMT + Bold + Italic
- [x] Both ZH PDFs use **DFKaiShu-SB-Estd-BF (= 標楷體 / BiauKai)** for Chinese characters (verified via `pdffonts`).
- [x] EN reports are monolingual English; ZH reports are monolingual Chinese with English citations only.
- [x] Section headings, hypothesis statements, table captions consistent across language pairs.
- [x] References list adopted teammate's Harvard style with URLs and access dates; applied uniformly across all four .tex sources; de-duplicated; teammate's reference set + Cameron–Trivedi (1990) added (cited for the auxiliary α estimator).
- [x] No emoji used in body text.
- [x] "Figure 1; Figure 2" placeholders from teammate's Background draft were dropped because no figures exist; replaced with prose referencing the citations directly.

---

## 8. Architectural parity with v4.0.0 (20260429_014427)

| Component | v4.0.0 path | v5.0.0 path | Status |
| --- | --- | --- | --- |
| Source script | `analysis/python/run_statistics.py` (v4.0.0) | same file, bumped to v5.0.0 with NB block | ✅ extended, not replaced |
| Data dump | `results/.../data/research_data_v4.csv` | identical name and schema | ✅ |
| Stats CSVs | `python/stats_analysis.csv`, `correlation_*.csv` | identical layout | ✅ |
| Regression text | `python/regression_results.txt` | identical layout, v5 header | ✅ |
| **NEW** NB regression text | — | `python/nb_regression_results.txt` | ✅ added |
| **NEW** NB coefficients CSV | — | `python/nb_parameter_estimates.csv` | ✅ added |
| Plots | `plots/*.png` (8 files) | `plots/*.png` (9 files; +nb_pearson_residuals.png) | ✅ extended |
| TeX sources | `tex_source/{Comprehensive,Group_Final}_Report_{EN,ZH}.tex` | identical filenames; full NB section added to each | ✅ extended |
| PDFs | 4 PDFs (17pp+17pp+8pp+7pp) | 4 PDFs (21pp+21pp+9pp+8pp) | ✅ extended (NB content adds 4pp to each Comprehensive, 1pp to each Group Final) |
| VERIFICATION.md | yes | this file | ✅ regenerated |

The new release is a **strict superset** of the v4.0.0 architecture: every artifact present in 20260429_014427 has its counterpart in 20260507_155131, plus the four NB-specific artifacts (text dump, CSV, residual plot, dedicated tex section per report).

---

## 9. Known caveats

1. **NB dispersion identification.** On heavy-tailed counts ($s^2/\bar Y \approx 850$), the NB joint likelihood is poorly identified in $\alpha$: a discrete-model joint MLE drifts to $\alpha \approx 1.8 \times 10^{6}$ without improving fit, and the Cameron–Trivedi auxiliary regression inflates $\alpha$ to $\approx 8{,}659$ because of the single 2,474-engagement outlier. We therefore use the marginal-distribution method-of-moments estimator $\hat\alpha_{\text{MoM}}=20.21$, which is well-conditioned and stable. This approach treats $\alpha$ as known when computing coefficient SEs, so the reported NB SEs do not propagate uncertainty in $\alpha$. This is a standard limitation of two-step NB and is documented in Section "Limitations" of the Group Final Report.
2. **H3 OLS↔NB divergence.** Emotional Valence is significant in OLS ($p=.016$) but only marginal in NB ($p=.100$). Sign is the same; the IRR 95 % CI of $[0.98, 1.22]$ just touches unity. Reported transparently as a calibrated qualifier rather than choosing one model.
3. **URL dummy.** Significant in NB ($p=.005$, IRR=1.64) but not in OLS ($p=.092$). The reverse direction of the H3 divergence; both reported faithfully in every tex source.
4. **N = 766 preserved.** v3.0.0's English-language filter remained intentionally disabled to preserve sample-size parity with v2.0.0 / v4.0.0. Teammate's Data section originally claimed a non-English filter was applied; we corrected this to state that non-English tokens are handled at the measurement stage (lexicon yields 0 valence) rather than via row exclusion.
5. **Observational design.** All four documents use correlational language; no causal claims. Limitations sections explicitly flag platform-specificity, single-brand scope, equal-weighted engagement composite, lexicon-based sentiment, and ZINB / hurdle as future-direction extensions.

---

## 10. Reproduction recipe

```bash
# from repo root
python -m venv .venv
.venv/bin/pip install pandas numpy scipy statsmodels matplotlib langdetect
RESULT_TAG=20260507_155131 .venv/bin/python analysis/python/run_statistics.py

cd results/20260507_155131/tex_source
for f in Comprehensive_Results_Report_{EN,ZH} Group_Final_Report_{EN,ZH}; do
  xelatex -interaction=nonstopmode "$f.tex"
  xelatex -interaction=nonstopmode "$f.tex"
done
```

Verification: re-run this script and re-read this file; every metric in §1–§5 should match exactly.
