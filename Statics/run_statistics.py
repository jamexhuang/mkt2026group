"""
run_statistics.py  —  Booking.com Social Media Engagement Study
Statistical Analysis Script  v1.1.0  (2026-03-28)
Brief: Descriptive stats, correlation, OLS regression (baseline + extension)

Changes v1.1.0: sas_ready.csv now keeps ALL original columns (no columns
                dropped), only reordered so research variables come first.

Input:  ../data/research_data.csv
Output: output/stats_analysis.csv          ← descriptive statistics
        output/correlation_matrix.csv      ← Pearson correlation matrix
        output/correlation_significance.csv ← correlation with sig stars
        output/regression_results.txt      ← regression coefficients & tests
        output/sas_ready.csv               ← full CSV reordered for SAS
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import os

# ─── optional imports ─────────────────────────────────────────────────────────
try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    print("[WARNING] statsmodels not found. Regression output will be skipped.")
    print("          Install with: pip install statsmodels")

# ─── setup ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "research_data.csv")
OUT_DIR   = os.path.join(BASE_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# ─── 1. Load data ─────────────────────────────────────────────────────────────
print("=" * 60)
print("Booking.com Engagement Study — Statistical Analysis v1.0.0")
print("=" * 60)

df_raw = pd.read_csv(DATA_PATH, encoding="utf-8-sig", low_memory=False)
print(f"\n[INFO] Raw data loaded: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")

# ─── 2. Build analysis variables ─────────────────────────────────────────────
#
#  CSV column  →  Proposal variable
#  like, comment, share  →  engagement  (DV)
#  length       →  TextLength  (H1)
#  question     →  Question    (H2, binary dummy 0/1)
#  valence      →  Valence     (H3)
#  hashtag      →  Hashtag     (H4)
#  picture      →  Picture     (control)
#  url          →  URL         (control)
#  at_mention   →  AtMention   (control)
#  emoji        →  Emoji       (extension)

df = df_raw.copy()

# compute engagement and log-transformed DV
df["engagement"]     = df["like"] + df["comment"] + df["share"]
df["log_engagement"] = np.log1p(df["engagement"])   # log(1 + engagement)

# ensure question is binary (0/1); in proposal it is already a dummy
df["question"] = (df["question"] > 0).astype(int)

# analysis columns — ordered as in proposal
ANALYSIS_COLS = [
    "engagement", "log_engagement",
    "length", "question", "valence", "hashtag",
    "picture", "url", "at_mention", "emoji"
]
LABEL = {
    "engagement":     "Engagement (raw)",
    "log_engagement": "log(1+Engagement)",
    "length":         "Text Length",
    "question":       "Question Mark (dummy)",
    "valence":        "Emotional Valence",
    "hashtag":        "Hashtag Count",
    "picture":        "Picture Count",
    "url":            "URL Count",
    "at_mention":     "At-Mention Count",
    "emoji":          "Emoji Count",
}

df_ana = df[ANALYSIS_COLS].dropna()
print(f"[INFO] Analysis sample: {len(df_ana)} observations (after dropna)")
missing = df_raw.shape[0] - len(df_ana)
if missing > 0:
    print(f"[INFO] Dropped {missing} rows due to missing values in analysis columns")

# ─── 3. Descriptive Statistics ────────────────────────────────────────────────
print("\n--- Descriptive Statistics ---")

desc_rows = []
for col in ANALYSIS_COLS:
    s = df_ana[col]
    row = {
        "Variable":  LABEL[col],
        "CSV_Field": col,
        "N":         int(s.count()),
        "Mean":      round(s.mean(), 4),
        "SD":        round(s.std(ddof=1), 4),
        "Min":       round(s.min(), 4),
        "Median":    round(s.median(), 4),
        "Max":       round(s.max(), 4),
        "Skewness":  round(stats.skew(s), 4),
        "Kurtosis":  round(stats.kurtosis(s), 4),   # excess kurtosis
    }
    # for dummy variable: also show proportion of 1s
    if col == "question":
        row["Prop_1"] = round(s.mean(), 4)
    else:
        row["Prop_1"] = ""
    desc_rows.append(row)

df_desc = pd.DataFrame(desc_rows)
desc_path = os.path.join(OUT_DIR, "stats_analysis.csv")
df_desc.to_csv(desc_path, index=False, encoding="utf-8-sig")
print(df_desc[["Variable", "N", "Mean", "SD", "Min", "Median", "Max"]].to_string(index=False))
print(f"\n[Saved] {desc_path}")

# ─── 4. Correlation Matrix ────────────────────────────────────────────────────
print("\n--- Pearson Correlation Matrix ---")

corr_cols = ["log_engagement", "length", "question", "valence",
             "hashtag", "picture", "url", "at_mention", "emoji"]
df_corr = df_ana[corr_cols].corr(method="pearson").round(3)
df_corr.index   = [LABEL[c] for c in corr_cols]
df_corr.columns = [LABEL[c] for c in corr_cols]

corr_path = os.path.join(OUT_DIR, "correlation_matrix.csv")
df_corr.to_csv(corr_path, encoding="utf-8-sig")
print(df_corr.to_string())
print(f"\n[Saved] {corr_path}")

# significance stars for correlation
print("\n--- Correlation p-values (two-tailed) ---")
n = len(df_ana)
pval_rows = {}
for c1 in corr_cols:
    pval_rows[c1] = {}
    for c2 in corr_cols:
        if c1 == c2:
            pval_rows[c1][c2] = ""
        else:
            r, p = stats.pearsonr(df_ana[c1], df_ana[c2])
            stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            pval_rows[c1][c2] = f"{r:.3f}{stars}"

df_pval = pd.DataFrame(pval_rows).T
df_pval.index   = [LABEL[c] for c in corr_cols]
df_pval.columns = [LABEL[c] for c in corr_cols]
pval_path = os.path.join(OUT_DIR, "correlation_significance.csv")
df_pval.to_csv(pval_path, encoding="utf-8-sig")
print(f"[Saved] {pval_path}")
print("(*** p<.001, ** p<.01, * p<.05)")

# ─── 5. OLS Regression ───────────────────────────────────────────────────────
reg_lines = []

if HAS_STATSMODELS:
    print("\n--- OLS Regression ---")

    # Model 1: Baseline (H1–H4 + controls)
    formula1 = ("log_engagement ~ length + question + valence + hashtag "
                "+ picture + url + at_mention")
    res1 = smf.ols(formula1, data=df_ana).fit()

    # Model 2: Extension (+ emoji)
    formula2 = formula1 + " + emoji"
    res2 = smf.ols(formula2, data=df_ana).fit()

    reg_lines.append("=" * 70)
    reg_lines.append("REGRESSION RESULTS  —  Booking.com Engagement Study  v1.0.0")
    reg_lines.append("DV: log(1 + Engagement)")
    reg_lines.append("=" * 70)

    for label, res, hyps in [
        ("Model 1 — Baseline (H1–H4 + Controls)", res1,
         {"length": "H1", "question": "H2", "valence": "H3", "hashtag": "H4"}),
        ("Model 2 — Extension (+ Emoji)", res2,
         {"length": "H1", "question": "H2", "valence": "H3", "hashtag": "H4"}),
    ]:
        reg_lines.append(f"\n{'─'*70}")
        reg_lines.append(label)
        reg_lines.append(f"{'─'*70}")
        reg_lines.append(
            f"{'Variable':<22} {'Hyp':<6} {'Coeff':>10} {'SE':>10} "
            f"{'t':>8} {'p-value':>10} {'Sig':>5}")
        reg_lines.append("─" * 70)

        param_order = ["Intercept", "length", "question", "valence",
                       "hashtag", "picture", "url", "at_mention", "emoji"]
        for pname in [p for p in param_order if p in res.params.index]:
            hyp_tag = hyps.get(pname, "")
            coeff  = res.params[pname]
            se_val = res.bse[pname]
            t_val  = res.tvalues[pname]
            p_val  = res.pvalues[pname]
            sig    = ("***" if p_val < 0.001 else
                      "**"  if p_val < 0.01  else
                      "*"   if p_val < 0.05  else "")
            reg_lines.append(
                f"{LABEL.get(pname, pname):<22} {hyp_tag:<6} "
                f"{coeff:>10.4f} {se_val:>10.4f} {t_val:>8.3f} "
                f"{p_val:>10.4f} {sig:>5}")

        reg_lines.append("─" * 70)
        reg_lines.append(f"N = {int(res.nobs):,}   R² = {res.rsquared:.4f}   "
                         f"Adj. R² = {res.rsquared_adj:.4f}   "
                         f"F({int(res.df_model)},{int(res.df_resid)}) = "
                         f"{res.fvalue:.3f},  p = {res.f_pvalue:.4f}")

    # VIF for Model 1
    reg_lines.append(f"\n{'─'*70}")
    reg_lines.append("Variance Inflation Factors (VIF) — Model 1")
    reg_lines.append("─" * 70)
    X_vif = sm.add_constant(
        df_ana[["length","question","valence","hashtag","picture","url","at_mention"]]
    )
    vif_vals = [variance_inflation_factor(X_vif.values, i)
                for i in range(X_vif.shape[1])]
    vif_names = X_vif.columns.tolist()
    for nm, vf in zip(vif_names[1:], vif_vals[1:]):   # skip const
        flag = "  ← check" if vf > 10 else ""
        reg_lines.append(f"  {LABEL.get(nm,nm):<22}  VIF = {vf:.3f}{flag}")

    reg_lines.append(f"\n{'─'*70}")
    reg_lines.append("Note: *** p<.001, ** p<.01, * p<.05 (two-tailed)")
    reg_lines.append("─" * 70)

    # print summary
    reg_text = "\n".join(reg_lines)
    print(reg_text)

    reg_path = os.path.join(OUT_DIR, "regression_results.txt")
    with open(reg_path, "w", encoding="utf-8") as f:
        f.write(reg_text)
    print(f"\n[Saved] {reg_path}")
else:
    reg_lines.append("[SKIPPED] statsmodels not installed — regression not run")

# ─── 6. Export SAS-Ready CSV ─────────────────────────────────────────────────
#
#  Strategy: keep ALL original columns from research_data.csv
#  Only reorder so research variables come first, just like column_mapping.md.
#  Derived columns (engagement, log_engage) are inserted at the front.
#  No rows are dropped — all 766 observations preserved.

print("\n--- Exporting SAS-ready CSV ---")

# Start from the original raw data (all 766 rows, all columns)
sas_df = df_raw.copy()
sas_df.insert(0, "obs", range(1, len(sas_df) + 1))

# Re-derive engagement columns on the full dataset
sas_df["engagement"]   = sas_df["like"] + sas_df["comment"] + sas_df["share"]
sas_df["log_engage"]   = np.log1p(sas_df["engagement"])
sas_df["question"]     = (sas_df["question"] > 0).astype(int)

# Research-variable columns go first (matches column_mapping.md Part 1 + derived)
RESEARCH_FIRST = [
    "obs",
    "id", "tweet_content",
    "like", "comment", "share",
    "engagement", "log_engage",   # derived DV columns
    "length", "question", "valence", "hashtag",
    "picture", "url", "at_mention", "emoji",
]

# Remaining original columns (all others, in original order)
existing_cols   = list(sas_df.columns)
remaining_cols  = [c for c in existing_cols if c not in RESEARCH_FIRST]
ordered_cols    = [c for c in RESEARCH_FIRST if c in existing_cols] + remaining_cols

sas_df = sas_df[ordered_cols]

sas_path = os.path.join(OUT_DIR, "sas_ready.csv")
sas_df.to_csv(sas_path, index=False, encoding="utf-8-sig")
print(f"[Saved] {sas_path}")
print(f"  Rows   : {sas_df.shape[0]}  (all original rows kept)")
print(f"  Columns: {sas_df.shape[1]}")
print(f"  First 18 columns: {list(sas_df.columns[:18])}")

# ─── 7. Summary ──────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  Output files saved to: Statics/output/")
print("  ─ stats_analysis.csv          (descriptive statistics)")
print("  ─ correlation_matrix.csv      (Pearson r matrix)")
print("  ─ correlation_significance.csv (r with significance stars)")
print("  ─ regression_results.txt      (OLS Model 1 & Model 2)")
print("  ─ sas_ready.csv               (all columns, research vars first)")
print("=" * 60)
print("\nDone. Script: run_statistics.py  v1.1.0")
