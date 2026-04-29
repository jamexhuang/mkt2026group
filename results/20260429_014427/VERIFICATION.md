# Verification Report — Booking.com Engagement Study v4.0.0

**Release tag:** `20260429_014427`
**Generated:** 2026-04-29
**Predecessor:** `20260330_151218` (v2.0.0)
**Scope:** four deliverables (EN+ZH × Comprehensive+Group) plus the regenerated v4.0.0 statistical artifacts.

---

## 1. Headline change

The only effective methodological change vs the v2.0.0 baseline is the re-coding of the three control variables from raw counts to binary dummies:

| Variable | v2.0.0 | v4.0.0 |
| --- | --- | --- |
| Picture | count (0–4) | dummy (>0 → 1) |
| URL | count (0–2) | dummy (>0 → 1) |
| At-Mention | count (0–3) | dummy (>0 → 1) |

The single change lifts model fit on the same N = 766 sample:

| Metric | v2.0.0 | v4.0.0 | Δ |
| --- | --- | --- | --- |
| R² | 0.4924 | **0.5119** | +0.0195 |
| Adj. R² | 0.4871 | **0.5068** | +0.0197 |
| F(8, 757) | 63.857 | **76.681** | +12.82 |
| Max VIF | 1.705 | 1.639 | −0.066 (≤2) |

✅ Confirmed empirically — matches the teammate's claim that "if we use dummy CVs the model has more explanatory power".

---

## 2. Output inventory (this release)

```
results/20260429_014427/
├── data/
│   └── research_data_v4.csv             # 766 × 38, encoding-clean snapshot
├── plots/
│   └── *.png                            # 8 diagnostic plots
├── python/
│   ├── plots/*.png                      # mirror copies
│   ├── report.html
│   ├── stats_analysis.csv
│   ├── correlation_matrix.csv
│   ├── correlation_significance.csv
│   ├── regression_results.txt
│   └── run_statistics.py                # archived snapshot of the script
├── tex_source/
│   ├── Comprehensive_Results_Report_EN.tex   ✅ 17 pp PDF
│   ├── Comprehensive_Results_Report_EN.pdf
│   ├── Comprehensive_Results_Report_ZH.tex   ✅ 17 pp PDF
│   ├── Comprehensive_Results_Report_ZH.pdf
│   ├── Group_Final_Report_EN.tex             ✅ 8 pp PDF
│   ├── Group_Final_Report_EN.pdf
│   ├── Group_Final_Report_ZH.tex             ✅ 7 pp PDF
│   └── Group_Final_Report_ZH.pdf
└── VERIFICATION.md (this file)
```

---

## 3. Group Final Report — word-budget compliance (English)

The EN report follows the assignment brief's per-section budgets (Background 150, Content/Hypotheses 400, Data 350, Measurement 400, Models 350, Results 450, Managerial 300, Limitations 100; total 2,500).

| Section | Budget | Actual | Δ | % |
| --- | ---: | ---: | ---: | ---: |
| Background | 150 | 145 | −5 | −3.3% |
| Content Features and Hypotheses | 400 | 400 | +0 | 0.0% |
| Data | 350 | 350 | +0 | 0.0% |
| Measurement of Variables | 400 | 404 | +4 | +1.0% |
| Model Specifications | 350 | 340 | −10 | −2.9% |
| Results | 450 | 436 | −14 | −3.1% |
| Managerial Suggestions | 300 | 286 | −14 | −4.7% |
| Limitations and Possible Improvements | 100 | 97 | −3 | −3.0% |
| **TOTAL** | **2,500** | **2,458** | −42 | −1.7% |

✅ Hard cap (≤2,500): **PASS**
✅ All sections within ±5% of budget
✅ ZH version mirrors the same section structure (~3,672 CJK chars total — Chinese character count is informational only; the assignment word cap applies to the English version)

---

## 4. Statistical numbers cross-checked between deliverables

The same eight regression coefficients, same R², same F, same VIFs appear in:
- `regression_results.txt` (machine output)
- `Comprehensive_Results_Report_EN.tex` Table 1 / Table 2 / Table 3
- `Comprehensive_Results_Report_ZH.tex` 對應表
- `Group_Final_Report_EN.tex` Table 1
- `Group_Final_Report_ZH.tex` 表 1

| Coef | Value | SE(HC1) | t | p | %-effect |
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

✅ Identical across all four .tex sources.

---

## 5. Hypothesis decisions

| H | Predicted | β (HC1) | p | Decision |
| --- | --- | ---: | ---: | --- |
| H1 Text Length | + | −0.019*** | <.001 | **Not supported** |
| H2 Question | + | +0.469*** | <.001 | **Supported** |
| H3 Valence | + | +0.064* | .016 | **Supported** |
| H4 Hashtag | + | +1.062*** | <.001 | **Supported** |
| H5 Emoji | + | +0.314*** | <.001 | **Supported** |

Same decisions in v2.0.0; only magnitudes shift slightly. ✅

---

## 6. Mathematical / statistical correctness checklist

- [x] DV is `ln(1 + Engagement)` via `numpy.log1p`; equation prose explicitly states the +1 offset and natural-log convention.
- [x] %-effect formula stated as `(exp(β)−1)×100%` for both continuous and binary predictors; magnitudes recomputed and match.
- [x] Heteroscedasticity flagged via Breusch–Pagan (LM = 90.22, p < .0001) → HC1 robust SE used throughout.
- [x] Residual normality acknowledged (Shapiro–Wilk W = 0.968) but framed correctly as a CLT-mitigated concern at N = 766, not as an inference invalidator.
- [x] All VIFs reported and below the conventional threshold of 10 (max 1.64).
- [x] Multicollinearity discussion explicitly references the VIF threshold of 10 (assignment brief requirement).
- [x] Model-selection rationale explicitly compares count-CV vs dummy-CV specs and reports both R² values; final spec justified by superior fit + no VIF deterioration.
- [x] Equation in the Group Report uses real variable names (TextLength, Question, …) per assignment brief instruction.
- [x] Results discussion uses correlational language ("is associated with", "tends to"); no causal claims.
- [x] Each hypothesis explicitly evaluated as Supported / Not Supported.

---

## 7. Editorial / formatting checklist

- [x] All four PDFs use **Times New Roman** for English text (verified via `pdffonts`).
- [x] Both ZH PDFs use **DFKaiShu-SB-Estd / 標楷體 (BiauKai)** for Chinese characters (verified via `pdffonts`).
- [x] EN reports are monolingual English; ZH reports are monolingual Chinese with English citations only.
- [x] Section headings, hypothesis statements, table captions consistent across language pairs.
- [x] References list de-duplicated; in-text citations reference each source by author–year style.
- [x] No emoji used in body text.

---

## 8. Architectural parity with v2.0.0 (20260330_151218)

| Component | v2 path | v4 path | Status |
| --- | --- | --- | --- |
| Source script | `analysis/python/run_statistics.py` (v2 / v3) | same file, bumped to v4.0.0 | ✅ |
| Data dump | `results/.../data/research_data.csv` | `results/.../data/research_data_v4.csv` | ✅ |
| Stats CSVs | `python/stats_analysis.csv`, `correlation_*.csv` | identical layout | ✅ |
| Regression text | `python/regression_results.txt` | identical layout, v4 header | ✅ |
| Plots | `plots/*.png` (8 files) | `plots/*.png` (8 files) | ✅ |
| TeX sources | `tex_source/Comprehensive_Results_Report.tex` | split into `_EN.tex` and `_ZH.tex`; **added** Group Final EN/ZH | ✅ extended, not removed |

The new release is a **superset** of the v2.0.0 architecture: every artifact present in 20260330_151218 has its counterpart in 20260429_014427, plus four PDF deliverables and an additional verification dossier.

---

## 9. Known caveats

1. **URL dummy not significant.** With 70% of posts already carrying a URL, "URL present" loses discriminative power once Picture and At-Mention are in the model. This is reported faithfully in every tex source rather than being hidden.
2. **Observational design.** All four documents use correlational language; no causal claims are made. Limitations sections explicitly flag platform-specificity, single-brand scope, equal-weighted engagement composite, and lexicon-based sentiment as constraints.
3. **N = 766.** Matches v2.0.0; the v3.0.0 English-language filter has been intentionally disabled to preserve sample-size parity. The Data section in the Group Report describes the API-side filtering (replies, retweets, video) but does not claim any further row-level filtering at analysis time, which is consistent with the actual code path.

---

## 10. Reproduction recipe

```bash
# from repo root
python -m venv .venv
.venv/bin/pip install pandas numpy scipy statsmodels matplotlib langdetect
RESULT_TAG=20260429_014427 .venv/bin/python analysis/python/run_statistics.py

cd results/20260429_014427/tex_source
for f in Comprehensive_Results_Report_{EN,ZH} Group_Final_Report_{EN,ZH}; do
  xelatex -interaction=nonstopmode "$f.tex"
  xelatex -interaction=nonstopmode "$f.tex"
done
```

Verification: re-run this script and re-read this file; every metric in §1–§5 should match exactly.
