"""
run_statistics.py  —  Booking.com Social Media Engagement Study
Comprehensive Statistical Analysis Script  v2.0.0  (2026-03-28)

Generates a full HTML report with:
  - Data Preview
  - Descriptive Statistics
  - Frequency Tables
  - Pearson Correlation (with & without p-values)
  - OLS Regression (ANOVA, coefficients, standardized betas, VIF, CI)
  - Residual Diagnostics (normality tests, quantiles, extreme obs)
  - Breusch-Pagan Heteroscedasticity Test
  - Robust OLS (HC Standard Errors)
  - Independent Samples t-test
  - Plots (residual histogram, Q-Q, distribution by group)

Model (single):
  DV:  log(1 + Engagement)
  IV:  TextLength (H1), Question (H2), Valence (H3), Hashtag (H4), Emoji (H5)
  CV:  Picture, URL, AtMention

Input:  ../../data/research_data.csv
Output: output/report.html                 ← full HTML report
        output/stats_analysis.csv          ← descriptive statistics
        output/correlation_matrix.csv      ← Pearson correlation matrix
        output/correlation_significance.csv ← correlation with sig stars
        output/regression_results.txt      ← regression coefficients & tests
        ../sas/input/sas_ready.csv         ← full CSV reordered for SAS input
        output/plots/*.png                 ← diagnostic plots
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import os
import warnings
import io
from datetime import datetime

warnings.filterwarnings("ignore")

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_agg import FigureCanvasAgg
import base64

# ─── Setup ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "..", "data", "research_data.csv")
OUT_DIR   = os.path.join(BASE_DIR, "output")
PLOT_DIR = os.path.join(OUT_DIR, "plots")
SAS_IN_DIR = os.path.join(BASE_DIR, "..", "sas", "input")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(SAS_IN_DIR, exist_ok=True)

# Try to use a CJK-compatible font for matplotlib
for font_name in ["PingFang TC", "Microsoft JhengHei", "Noto Sans CJK TC",
                   "Arial Unicode MS", "STHeiti"]:
    if any(font_name in f.name for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = [font_name, "sans-serif"]
        break

plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150

# ─── Variable config ─────────────────────────────────────────────────────────
LABEL = {
    "engagement":     "Engagement (raw)",
    "log_engagement": "log(1+Engagement)",
    "length":         "Text Length (words)",
    "question":       "Question Mark (0/1)",
    "valence":        "Emotional Valence",
    "hashtag":        "Hashtag Count",
    "emoji":          "Emoji Count",
    "picture":        "Picture Count",
    "url":            "URL Count",
    "at_mention":     "At-Mention Count",
}

ANALYSIS_COLS = [
    "engagement", "log_engagement",
    "length", "question", "valence", "hashtag", "emoji",
    "picture", "url", "at_mention",
]

# Model: IV (H1-H5) + CV
IV_COLS = ["length", "question", "valence", "hashtag", "emoji"]
CV_COLS = ["picture", "url", "at_mention"]
ALL_X_COLS = IV_COLS + CV_COLS
HYP_MAP = {"length": "H1", "question": "H2", "valence": "H3",
           "hashtag": "H4", "emoji": "H5"}

DV = "log_engagement"


# ═══════════════════════════════════════════════════════════════════════════════
#  HTML report builder
# ═══════════════════════════════════════════════════════════════════════════════
class HtmlReport:
    """Accumulates HTML content for the final report."""

    def __init__(self, title: str):
        self.title = title
        self.parts: list[str] = []

    def h2(self, text: str):
        self.parts.append(f'<h2 class="section">{text}</h2>')

    def h3(self, text: str):
        self.parts.append(f'<h3 class="sub">{text}</h3>')

    def p(self, text: str):
        self.parts.append(f"<p>{text}</p>")

    def pre(self, text: str):
        self.parts.append(f"<pre>{text}</pre>")

    def hr(self):
        self.parts.append("<hr>")

    def table(self, df: pd.DataFrame, caption: str = "", index: bool = True,
              float_fmt: str = ""):
        """Convert a DataFrame to an HTML table with optional caption."""
        html = "<div class='tbl-wrap'>"
        if caption:
            html += f"<div class='caption'>{caption}</div>"
        kw = dict(classes="tbl", border=0, index=index)
        if float_fmt:
            kw["float_format"] = lambda x: float_fmt % x
        html += df.to_html(**kw)
        html += "</div>"
        self.parts.append(html)

    def img(self, path_or_fig, caption: str = ""):
        """Embed a matplotlib figure as base64 or reference a saved PNG."""
        if isinstance(path_or_fig, plt.Figure):
            buf = io.BytesIO()
            path_or_fig.savefig(buf, format="png", bbox_inches="tight",
                                dpi=150)
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode("utf-8")
            tag = f'<img src="data:image/png;base64,{b64}">'
            plt.close(path_or_fig)
        else:
            tag = f'<img src="{path_or_fig}">'
        html = f'<div class="fig">{tag}'
        if caption:
            html += f'<div class="caption">{caption}</div>'
        html += "</div>"
        self.parts.append(html)

    def render(self) -> str:
        body = "\n".join(self.parts)
        return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>{self.title}</title>
<style>
body {{ font-family: 'Segoe UI', Arial, 'PingFang TC', sans-serif;
       max-width: 1100px; margin: 30px auto; padding: 0 20px;
       color: #333; background: #fff; font-size: 14px; }}
h1 {{ text-align: center; border-bottom: 3px solid #2c5f8a; padding-bottom: 12px; }}
h2.section {{ background: #2c5f8a; color: #fff; padding: 8px 16px;
              margin-top: 40px; font-size: 16px; }}
h3.sub {{ color: #2c5f8a; border-bottom: 1px solid #ccc; padding-bottom: 4px;
          margin-top: 24px; font-size: 14px; }}
.tbl-wrap {{ margin: 16px 0; overflow-x: auto; }}
.caption {{ font-weight: bold; text-align: center; margin-bottom: 6px;
            font-size: 13px; color: #555; }}
table.tbl {{ border-collapse: collapse; margin: 0 auto; font-size: 13px; }}
table.tbl th {{ background: #e8eef4; padding: 6px 10px; border: 1px solid #bbb;
                text-align: center; white-space: nowrap; }}
table.tbl td {{ padding: 5px 10px; border: 1px solid #ccc; text-align: right;
                white-space: nowrap; }}
table.tbl td:first-child, table.tbl th:first-child {{ text-align: left; }}
pre {{ background: #f4f4f4; padding: 12px; border: 1px solid #ddd;
       overflow-x: auto; font-size: 12px; line-height: 1.4; }}
.fig {{ text-align: center; margin: 20px 0; }}
.fig img {{ max-width: 100%; border: 1px solid #ddd; }}
hr {{ border: none; border-top: 2px solid #ccc; margin: 30px 0; }}
p {{ line-height: 1.6; }}
.note {{ font-size: 12px; color: #777; margin-top: 4px; }}
.sig {{ font-size: 11px; color: #888; }}
</style>
</head>
<body>
<h1>{self.title}</h1>
<p style="text-align:center; color:#666;">
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
Python Statistical Analysis — Comprehensive Report
</p>
{body}
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  1. Load Data
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("Booking.com Engagement Study — Statistical Analysis v2.0.0")
print("=" * 70)

df_raw = pd.read_csv(DATA_PATH, encoding="utf-8-sig", low_memory=False)
print(f"\n[INFO] Raw data loaded: {df_raw.shape[0]} rows × {df_raw.shape[1]} cols")

rpt = HtmlReport("Booking.com Social Media Engagement — Statistical Report")

# ═══════════════════════════════════════════════════════════════════════════════
#  2. Build Analysis Variables
# ═══════════════════════════════════════════════════════════════════════════════
df = df_raw.copy()
df["engagement"] = df["like"] + df["comment"] + df["share"]
df["log_engagement"] = np.log1p(df["engagement"])
df["question"] = (df["question"] > 0).astype(int)

df_ana = df[ANALYSIS_COLS].dropna()
N = len(df_ana)
print(f"[INFO] Analysis sample: {N} observations (after dropna)")

# ═══════════════════════════════════════════════════════════════════════════════
#  3. Data Preview
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Data Preview — First 10 Observations")

preview_cols = ["obs", "id", "like", "comment", "share",
                "engagement", "log_engagement", "length", "question",
                "valence", "hashtag", "picture", "url", "at_mention", "emoji"]
df_preview = df.head(10).copy()
df_preview.insert(0, "obs", range(1, 11))
df_preview["id"] = df_raw["id"].head(10).values
# only keep preview cols that exist
preview_cols = [c for c in preview_cols if c in df_preview.columns]
rpt.table(df_preview[preview_cols].round(4), index=False)

# ═══════════════════════════════════════════════════════════════════════════════
#  4. Descriptive Statistics
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 1. Descriptive Statistics")
rpt.h3("MEANS")

desc_rows = []
for col in ANALYSIS_COLS:
    s = df_ana[col]
    row = {
        "Variable": col,
        "Label":    LABEL[col],
        "N":        int(s.count()),
        "Mean":     s.mean(),
        "SD":       s.std(ddof=1),
        "Min":      s.min(),
        "Q1":       s.quantile(0.25),
        "Median":   s.median(),
        "Q3":       s.quantile(0.75),
        "Max":      s.max(),
        "Skewness": stats.skew(s),
        "Kurtosis": stats.kurtosis(s),
    }
    desc_rows.append(row)

df_desc = pd.DataFrame(desc_rows)
df_desc_display = df_desc.copy()
for c in ["Mean", "SD", "Min", "Q1", "Median", "Q3", "Max"]:
    df_desc_display[c] = df_desc_display[c].map(lambda x: f"{x:.4f}")
for c in ["Skewness", "Kurtosis"]:
    df_desc_display[c] = df_desc_display[c].map(lambda x: f"{x:.4f}")
rpt.table(df_desc_display, index=False)

# Save CSV
df_desc.to_csv(os.path.join(OUT_DIR, "stats_analysis.csv"),
               index=False, encoding="utf-8-sig")
print(f"[Saved] stats_analysis.csv")

# ═══════════════════════════════════════════════════════════════════════════════
#  5. Frequency Table — Question Mark
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 1b. Question Mark — Frequency Distribution")
rpt.h3("FREQ")

freq = df_ana["question"].value_counts().sort_index()
df_freq = pd.DataFrame({
    "Question Mark (0=No, 1=Yes)": freq.index.map({0: "0", 1: "1"}),
    "Frequency": freq.values,
    "Percent (%)": (freq.values / N * 100).round(2),
})
rpt.table(df_freq, index=False)

# ═══════════════════════════════════════════════════════════════════════════════
#  6. Pearson Correlation Matrix
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 2. Pearson Correlation Matrix")
rpt.h3("CORR")

corr_cols = [DV] + ALL_X_COLS
corr_labels = [LABEL.get(c, c) for c in corr_cols]

# 6a. r values only
df_corr = df_ana[corr_cols].corr(method="pearson")
df_corr.index = corr_labels
df_corr.columns = corr_labels
rpt.p(f"<b>{len(corr_cols)} Variables:</b> {', '.join(corr_cols)}")
rpt.p(f"<b>Pearson Correlation Coefficients, N = {N}</b>")
rpt.table(df_corr.round(5))

df_corr.to_csv(os.path.join(OUT_DIR, "correlation_matrix.csv"),
               encoding="utf-8-sig")
print(f"[Saved] correlation_matrix.csv")

# 6b. r with p-values
rpt.h2("Table 2b. Pearson Correlation Matrix (with p-values)")
rpt.h3("CORR")
rpt.p(f"<b>Pearson Correlation Coefficients, N = {N}</b><br>"
       "Prob &gt; |r| under H0: Rho=0")

pval_r = {}
pval_p = {}
pval_display = {}
for c1 in corr_cols:
    pval_r[c1] = {}
    pval_p[c1] = {}
    pval_display[c1] = {}
    for c2 in corr_cols:
        if c1 == c2:
            pval_display[c1][c2] = "1.00000"
            pval_r[c1][c2] = 1.0
            pval_p[c1][c2] = ""
        else:
            r, p = stats.pearsonr(df_ana[c1], df_ana[c2])
            pval_r[c1][c2] = r
            pval_p[c1][c2] = p
            p_str = "<.0001" if p < 0.0001 else f"{p:.4f}"
            pval_display[c1][c2] = f"{r:.5f}<br><span class='sig'>{p_str}</span>"

df_pval_display = pd.DataFrame(pval_display)
df_pval_display.index = corr_labels
df_pval_display.columns = corr_labels
# Use raw HTML for this table
html_tbl = "<div class='tbl-wrap'><table class='tbl'><thead><tr><th></th>"
for label in corr_labels:
    html_tbl += f"<th>{label}</th>"
html_tbl += "</tr></thead><tbody>"
for i, c1 in enumerate(corr_cols):
    html_tbl += f"<tr><td style='text-align:left;font-weight:bold'>{corr_labels[i]}</td>"
    for j, c2 in enumerate(corr_cols):
        html_tbl += f"<td>{pval_display[c1][c2]}</td>"
    html_tbl += "</tr>"
html_tbl += "</tbody></table></div>"
rpt.parts.append(html_tbl)

# Significance stars version for CSV
sig_display = {}
for c1 in corr_cols:
    sig_display[c1] = {}
    for c2 in corr_cols:
        if c1 == c2:
            sig_display[c1][c2] = ""
        else:
            r = pval_r[c1][c2]
            p = pval_p[c1][c2]
            stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            sig_display[c1][c2] = f"{r:.3f}{stars}"
df_sig = pd.DataFrame(sig_display)
df_sig.index = corr_labels
df_sig.columns = corr_labels
df_sig.to_csv(os.path.join(OUT_DIR, "correlation_significance.csv"),
              encoding="utf-8-sig")
print(f"[Saved] correlation_significance.csv")


# ═══════════════════════════════════════════════════════════════════════════════
#  7. OLS Regression
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 3. OLS Regression")
rpt.h3("REG")
rpt.p(f"<b>DV:</b> {DV} — {LABEL[DV]}")

formula = f"{DV} ~ " + " + ".join(ALL_X_COLS)
res_ols = smf.ols(formula, data=df_ana).fit()

# ANOVA table
ss_model = res_ols.ess
ss_error = res_ols.ssr
ss_total = ss_model + ss_error
df_model = int(res_ols.df_model)
df_error = int(res_ols.df_resid)
df_total = df_model + df_error
ms_model = ss_model / df_model
ms_error = ss_error / df_error

anova_data = {
    "Source": ["Model", "Error", "Corrected Total"],
    "DF": [df_model, df_error, df_total],
    "Sum of Squares": [f"{ss_model:.5f}", f"{ss_error:.5f}", f"{ss_total:.5f}"],
    "Mean Square": [f"{ms_model:.5f}", f"{ms_error:.5f}", ""],
    "F Value": [f"{res_ols.fvalue:.2f}", "", ""],
    "Pr > F": [f"<.0001" if res_ols.f_pvalue < 0.0001 else f"{res_ols.f_pvalue:.4f}", "", ""],
}
rpt.p(f"<b>Observations read:</b> {N} &nbsp;&nbsp; <b>Observations used:</b> {N}")
rpt.h3("Analysis of Variance (ANOVA)")
rpt.table(pd.DataFrame(anova_data), index=False)

# Model fit statistics
root_mse = np.sqrt(ms_error)
fit_data = {
    "Statistic": ["Root MSE", "Dependent Mean", "Coeff Var", "R-Square", "Adj R-Square"],
    "Value": [
        f"{root_mse:.5f}",
        f"{df_ana[DV].mean():.5f}",
        f"{root_mse / df_ana[DV].mean() * 100:.5f}",
        f"{res_ols.rsquared:.4f}",
        f"{res_ols.rsquared_adj:.4f}",
    ],
}
rpt.h3("Fit Statistics")
rpt.table(pd.DataFrame(fit_data), index=False)

# Parameter estimates with standardized betas, VIF, CI
rpt.h3("Parameter Estimates")

X_with_const = sm.add_constant(df_ana[ALL_X_COLS])
vif_vals = {ALL_X_COLS[i]: variance_inflation_factor(X_with_const.values, i + 1)
            for i in range(len(ALL_X_COLS))}

# Standardized betas: standardize X and Y, refit
df_std = df_ana[ALL_X_COLS + [DV]].apply(lambda x: (x - x.mean()) / x.std(ddof=1))
res_std = smf.ols(formula, data=df_std).fit()

param_rows = []
for pname in ["Intercept"] + ALL_X_COLS:
    coeff = res_ols.params[pname]
    se_val = res_ols.bse[pname]
    t_val = res_ols.tvalues[pname]
    p_val = res_ols.pvalues[pname]
    ci = res_ols.conf_int().loc[pname]

    hyp = HYP_MAP.get(pname, "")
    label = LABEL.get(pname, pname)
    if pname in CV_COLS:
        label += " (control)"
    if hyp:
        label = f"{hyp}: {label}"

    std_beta = res_std.params.get(pname, 0) if pname != "Intercept" else 0
    tol = 1.0 / vif_vals[pname] if pname in vif_vals else np.nan
    vif = vif_vals.get(pname, np.nan)

    p_str = "<.0001" if p_val < 0.0001 else f"{p_val:.4f}"

    param_rows.append({
        "Variable": pname,
        "Label": label,
        "DF": 1,
        "Estimate": f"{coeff:.5f}",
        "Std Error": f"{se_val:.5f}",
        "t Value": f"{t_val:.2f}",
        "Pr > |t|": p_str,
        "Std Beta": f"{std_beta:.5f}" if pname != "Intercept" else "0",
        "Tolerance": f"{tol:.5f}" if not np.isnan(tol) else ".",
        "VIF": f"{vif:.5f}" if not np.isnan(vif) else "0",
        "95% CI Lower": f"{ci[0]:.5f}",
        "95% CI Upper": f"{ci[1]:.5f}",
    })

df_params = pd.DataFrame(param_rows)
rpt.table(df_params, index=False)

# Durbin-Watson
dw = durbin_watson(res_ols.resid)
rpt.p(f"<b>Durbin-Watson:</b> {dw:.4f}")

# ═══════════════════════════════════════════════════════════════════════════════
#  8. Residual Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 4. Residual Diagnostics — Normality Tests")
rpt.h3("UNIVARIATE")
rpt.p("<b>Variable:</b> Residuals (e)")

resid = res_ols.resid

# Moments
moments_data = {
    "Statistic": ["N", "Mean", "Std Deviation", "Variance", "Skewness", "Kurtosis",
                   "Uncorrected SS", "Corrected SS", "Std Error Mean"],
    "Value": [
        f"{N}",
        f"{resid.mean():.10f}",
        f"{resid.std(ddof=1):.8f}",
        f"{resid.var(ddof=1):.8f}",
        f"{stats.skew(resid):.8f}",
        f"{stats.kurtosis(resid):.8f}",
        f"{(resid**2).sum():.5f}",
        f"{((resid - resid.mean())**2).sum():.5f}",
        f"{resid.std(ddof=1) / np.sqrt(N):.8f}",
    ],
}
rpt.h3("Moments")
rpt.table(pd.DataFrame(moments_data), index=False)

# Basic Statistical Measures
rpt.h3("Basic Statistical Measures")
basic_loc = {
    "Location": ["Mean", "Median", "Mode"],
    "Value": [
        f"{resid.mean():.5f}",
        f"{resid.median():.5f}",
        f"{resid.mode().iloc[0]:.5f}" if len(resid.mode()) > 0 else ".",
    ],
}
basic_var = {
    "Variability": ["Std Deviation", "Variance", "Range", "Interquartile Range"],
    "Value": [
        f"{resid.std(ddof=1):.5f}",
        f"{resid.var(ddof=1):.5f}",
        f"{resid.max() - resid.min():.5f}",
        f"{resid.quantile(0.75) - resid.quantile(0.25):.5f}",
    ],
}
# Combine side by side
loc_df = pd.DataFrame(basic_loc)
var_df = pd.DataFrame(basic_var)
rpt.table(loc_df, caption="Location", index=False)
rpt.table(var_df, caption="Variability", index=False)

# Tests for Location: Mu0=0
t_stat_loc, t_p_loc = stats.ttest_1samp(resid, 0)
sign_count = (resid > 0).sum() - (resid < 0).sum()
n_pos = (resid > 0).sum()
n_neg = (resid < 0).sum()
# Sign test
sign_m = int(n_pos - n_neg) // 2
# Wilcoxon signed-rank test
try:
    wilcox_stat, wilcox_p = stats.wilcoxon(resid)
except:
    wilcox_stat, wilcox_p = np.nan, np.nan

# Sign test p-value via binomial
try:
    sign_p = stats.binomtest(n_pos, N, 0.5).pvalue
except AttributeError:
    sign_p = np.nan

loc_test = {
    "Test": ["Student's t", "Sign", "Signed Rank"],
    "Statistic": [f"t = {t_stat_loc:.4f}",
                   f"M = {sign_m}",
                   f"S = {wilcox_stat:.1f}" if not np.isnan(wilcox_stat) else "."],
    "p Value": [f"{t_p_loc:.4f}",
                f"{sign_p:.4f}" if not np.isnan(sign_p) else ".",
                f"{wilcox_p:.4f}" if not np.isnan(wilcox_p) else "."],
}
rpt.h3("Tests for Location: Mu0=0")
rpt.table(pd.DataFrame(loc_test), index=False)

# Normality Tests
rpt.h3("Tests for Normality")
sw_stat, sw_p = stats.shapiro(resid)
ks_stat, ks_p = stats.kstest(resid, "norm", args=(resid.mean(), resid.std(ddof=1)))
# Anderson-Darling
ad_result = stats.anderson(resid, dist="norm")

norm_tests = {
    "Test": ["Shapiro-Wilk", "Kolmogorov-Smirnov", "Anderson-Darling"],
    "Statistic": [
        f"W = {sw_stat:.6f}",
        f"D = {ks_stat:.6f}",
        f"A² = {ad_result.statistic:.6f}",
    ],
    "p Value": [
        "<0.0001" if sw_p < 0.0001 else f"{sw_p:.4f}",
        "<0.0100" if ks_p < 0.01 else f"{ks_p:.4f}",
        f"< {ad_result.significance_level[0]/100:.4f}" if ad_result.statistic > ad_result.critical_values[0] else f"> {ad_result.significance_level[-1]/100:.4f}",
    ],
}
rpt.table(pd.DataFrame(norm_tests), index=False)

# Quantiles
rpt.h3("Quantiles (Definition 5)")
quantile_pcts = [0, 0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 1.0]
quantile_labels = ["0% Min", "1%", "5%", "10%", "25% Q1", "50% Median",
                    "75% Q3", "90%", "95%", "99%", "100% Max"]
quantile_vals = [resid.quantile(q) for q in quantile_pcts]
df_quant = pd.DataFrame({
    "Level": quantile_labels,
    "Quantile": [f"{v:.6f}" for v in quantile_vals],
})
rpt.table(df_quant, index=False)

# Extreme Observations
rpt.h3("Extreme Observations")
resid_sorted = resid.sort_values()
lowest_5 = resid_sorted.head(5)
highest_5 = resid_sorted.tail(5).iloc[::-1]

extreme_data = {
    "Lowest Value": [f"{v:.5f}" for v in lowest_5.values],
    "Lowest Obs": [str(i + 1) for i in lowest_5.index],
    "Highest Value": [f"{v:.5f}" for v in highest_5.values],
    "Highest Obs": [str(i + 1) for i in highest_5.index],
}
rpt.table(pd.DataFrame(extreme_data), index=False)


# ═══════════════════════════════════════════════════════════════════════════════
#  9. Residual Plots
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 4b. Residual Plots")

# Histogram + Normal Curve
fig, ax = plt.subplots(figsize=(8, 5))
n_bins = 40
counts, bins, patches = ax.hist(resid, bins=n_bins, density=True, alpha=0.7,
                                 color="#4a86c8", edgecolor="#2c5f8a", linewidth=0.5)
x_norm = np.linspace(resid.min() - 0.5, resid.max() + 0.5, 200)
y_norm = stats.norm.pdf(x_norm, resid.mean(), resid.std(ddof=1))
ax.plot(x_norm, y_norm, "r-", linewidth=2,
        label=f"Normal (Mu={resid.mean():.3f}, Sigma={resid.std(ddof=1):.3f})")
ax.set_xlabel("Residual")
ax.set_ylabel("Density")
ax.set_title("Distribution of Residuals")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(PLOT_DIR, "residual_histogram.png"), dpi=150, bbox_inches="tight")
rpt.img(fig, "Residual Distribution with Normal Curve")

# Q-Q Plot
fig2, ax2 = plt.subplots(figsize=(6, 6))
sm.qqplot(resid, line="s", ax=ax2, markersize=3, alpha=0.6)
ax2.set_title("Q-Q Plot of Residuals")
fig2.tight_layout()
fig2.savefig(os.path.join(PLOT_DIR, "qq_plot.png"), dpi=150, bbox_inches="tight")
rpt.img(fig2, "Q-Q Plot of Residuals")

# Residuals vs Fitted
fig3, ax3 = plt.subplots(figsize=(8, 5))
fitted = res_ols.fittedvalues
ax3.scatter(fitted, resid, alpha=0.3, s=10, color="#4a86c8")
ax3.axhline(y=0, color="red", linewidth=1, linestyle="--")
ax3.set_xlabel("Fitted Values")
ax3.set_ylabel("Residuals")
ax3.set_title("Residuals vs Fitted Values")
fig3.tight_layout()
fig3.savefig(os.path.join(PLOT_DIR, "resid_vs_fitted.png"), dpi=150, bbox_inches="tight")
rpt.img(fig3, "Residuals vs Fitted Values")

print(f"[Saved] plots/residual_histogram.png, qq_plot.png, resid_vs_fitted.png")


# ═══════════════════════════════════════════════════════════════════════════════
#  10. Breusch-Pagan Heteroscedasticity Test
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 5. Heteroscedasticity Check — Breusch-Pagan Test")

# Breusch-Pagan via statsmodels
bp_stat, bp_p, bp_f, bp_fp = het_breuschpagan(res_ols.resid, res_ols.model.exog)

rpt.h3("Breusch-Pagan Test (statsmodels)")
bp_data = {
    "Test": ["Lagrange Multiplier (LM)", "LM p-value",
             "F-statistic", "F p-value"],
    "Value": [f"{bp_stat:.4f}", f"{bp_p:.6f}" if bp_p >= 0.0001 else "<.0001",
              f"{bp_f:.4f}", f"{bp_fp:.6f}" if bp_fp >= 0.0001 else "<.0001"],
}
rpt.table(pd.DataFrame(bp_data), index=False)

# Manual approach (like SAS: regress e² on X)
rpt.h3("Breusch-Pagan Approximation (OLS on squared residuals)")
rpt.p("<b>DV:</b> e² (squared residuals from main model)")

e2 = resid ** 2
bp_formula = "e2 ~ " + " + ".join(ALL_X_COLS)
df_bp = df_ana[ALL_X_COLS].copy()
df_bp["e2"] = e2.values
res_bp = smf.ols(bp_formula, data=df_bp).fit()

# ANOVA for BP
bp_anova = {
    "Source": ["Model", "Error", "Corrected Total"],
    "DF": [int(res_bp.df_model), int(res_bp.df_resid),
            int(res_bp.df_model + res_bp.df_resid)],
    "Sum of Squares": [f"{res_bp.ess:.5f}", f"{res_bp.ssr:.5f}",
                        f"{res_bp.ess + res_bp.ssr:.5f}"],
    "Mean Square": [f"{res_bp.ess/res_bp.df_model:.5f}",
                     f"{res_bp.ssr/res_bp.df_resid:.5f}", ""],
    "F Value": [f"{res_bp.fvalue:.2f}", "", ""],
    "Pr > F": ["<.0001" if res_bp.f_pvalue < 0.0001 else f"{res_bp.f_pvalue:.4f}", "", ""],
}
rpt.table(pd.DataFrame(bp_anova), index=False)

bp_fit = {
    "Statistic": ["Root MSE", "R-Square", "Adj R-Square"],
    "Value": [f"{np.sqrt(res_bp.ssr/res_bp.df_resid):.5f}",
              f"{res_bp.rsquared:.4f}", f"{res_bp.rsquared_adj:.4f}"],
}
rpt.table(pd.DataFrame(bp_fit), index=False)

# BP parameter estimates
bp_params = []
for pname in ["Intercept"] + ALL_X_COLS:
    label = LABEL.get(pname, pname)
    hyp = HYP_MAP.get(pname, "")
    if pname in CV_COLS:
        label += " (control)"
    if hyp:
        label = f"{hyp}: {label}"
    p_val = res_bp.pvalues[pname]
    bp_params.append({
        "Variable": pname,
        "Label": label,
        "DF": 1,
        "Estimate": f"{res_bp.params[pname]:.5f}",
        "Std Error": f"{res_bp.bse[pname]:.5f}",
        "t Value": f"{res_bp.tvalues[pname]:.2f}",
        "Pr > |t|": "<.0001" if p_val < 0.0001 else f"{p_val:.4f}",
    })
rpt.table(pd.DataFrame(bp_params), index=False)


# ═══════════════════════════════════════════════════════════════════════════════
#  11. Robust OLS (HC Standard Errors)
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 6. Robust OLS — HC Standard Errors (SURVEYREG equivalent)")

# Use HC1 to match SAS SURVEYREG VARMETHOD=TAYLOR
res_hc = smf.ols(formula, data=df_ana).fit(cov_type="HC1")

rpt.h3("Data Summary")
summary_data = {
    "Item": ["Number of Observations", f"Mean of {DV}", f"Sum of {DV}"],
    "Value": [f"{N}", f"{df_ana[DV].mean():.5f}", f"{df_ana[DV].sum():.1f}"],
}
rpt.table(pd.DataFrame(summary_data), index=False)

rpt.h3("Fit Statistics")
hc_fit = {
    "Statistic": ["R-Square", "Root MSE", "Denominator DF"],
    "Value": [f"{res_hc.rsquared:.4f}",
              f"{np.sqrt(res_hc.mse_resid):.4f}",
              f"{int(res_hc.df_resid)}"],
}
rpt.table(pd.DataFrame(hc_fit), index=False)

# F-tests for each effect (Type III like SAS)
rpt.h3("Tests of Model Effects")
effect_rows = []
# Overall model F
effect_rows.append({
    "Effect": "Model",
    "Num DF": int(res_hc.df_model),
    "F Value": f"{res_hc.fvalue:.2f}",
    "Pr > F": "<.0001" if res_hc.f_pvalue < 0.0001 else f"{res_hc.f_pvalue:.4f}",
})
for pname in ["Intercept"] + ALL_X_COLS:
    t_val = res_hc.tvalues[pname]
    f_val = t_val ** 2
    p_val = res_hc.pvalues[pname]
    effect_rows.append({
        "Effect": pname,
        "Num DF": 1,
        "F Value": f"{f_val:.2f}",
        "Pr > F": "<.0001" if p_val < 0.0001 else f"{p_val:.4f}",
    })
rpt.table(pd.DataFrame(effect_rows), index=False)
rpt.p(f'<span class="note">Note: The denominator degrees of freedom for the F tests is {int(res_hc.df_resid)}.</span>')

# Estimated Regression Coefficients (HC)
rpt.h3("Estimated Regression Coefficients (Robust SE)")
hc_params = []
for pname in ["Intercept"] + ALL_X_COLS:
    coeff = res_hc.params[pname]
    se_val = res_hc.bse[pname]
    t_val = res_hc.tvalues[pname]
    p_val = res_hc.pvalues[pname]
    p_str = "<.0001" if p_val < 0.0001 else f"{p_val:.4f}"
    hc_params.append({
        "Parameter": pname,
        "Estimate": f"{coeff:.7f}",
        "Std Error": f"{se_val:.8f}",
        "t Value": f"{t_val:.2f}",
        "Pr > |t|": p_str,
    })
rpt.table(pd.DataFrame(hc_params), index=False)
rpt.p(f'<span class="note">Note: The degrees of freedom for the t tests is {int(res_hc.df_resid)}.</span>')

# Compare OLS SE vs HC SE
rpt.h3("Standard Error Comparison: OLS vs Robust (HC1)")
se_compare = []
for pname in ["Intercept"] + ALL_X_COLS:
    se_ols = res_ols.bse[pname]
    se_robust = res_hc.bse[pname]
    ratio = se_robust / se_ols
    p_ols = res_ols.pvalues[pname]
    p_hc = res_hc.pvalues[pname]

    def sig_stars(p):
        if p < 0.001: return "***"
        if p < 0.01: return "**"
        if p < 0.05: return "*"
        return ""

    se_compare.append({
        "Variable": pname,
        "OLS SE": f"{se_ols:.5f}",
        "Robust SE": f"{se_robust:.5f}",
        "Ratio (HC/OLS)": f"{ratio:.3f}",
        "OLS Sig": sig_stars(p_ols),
        "Robust Sig": sig_stars(p_hc),
    })
rpt.table(pd.DataFrame(se_compare), index=False)
rpt.p('<span class="note">Significance: *** p&lt;.001, ** p&lt;.01, * p&lt;.05</span>')


# ═══════════════════════════════════════════════════════════════════════════════
#  12. t-Test — Mean Engagement by Question Mark
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Table 7. Mean Engagement by Question Mark (t-test)")
rpt.h3("TTEST")

for dep_var, dep_label in [(DV, LABEL[DV]), ("engagement", LABEL["engagement"])]:
    rpt.p(f"<b>Variable:</b> {dep_var} — {dep_label}")

    g0 = df_ana.loc[df_ana["question"] == 0, dep_var]
    g1 = df_ana.loc[df_ana["question"] == 1, dep_var]

    # Group statistics
    grp_data = {
        "question": ["0", "1", "Diff (1-0)"],
        "Method": ["", "", "Pooled"],
        "N": [len(g0), len(g1), ""],
        "Mean": [f"{g0.mean():.4f}", f"{g1.mean():.4f}", f"{g1.mean()-g0.mean():.4f}"],
        "Std Dev": [f"{g0.std(ddof=1):.4f}", f"{g1.std(ddof=1):.4f}",
                     f"{df_ana[dep_var].std(ddof=1):.4f}"],
        "Std Error": [f"{g0.std(ddof=1)/np.sqrt(len(g0)):.4f}",
                       f"{g1.std(ddof=1)/np.sqrt(len(g1)):.4f}", ""],
        "Min": [f"{g0.min():.4f}", f"{g1.min():.4f}", ""],
        "Max": [f"{g0.max():.4f}", f"{g1.max():.4f}", ""],
    }
    rpt.table(pd.DataFrame(grp_data), index=False)

    # Equal variance (pooled) t-test
    t_eq, p_eq = stats.ttest_ind(g1, g0, equal_var=True)
    # Unequal variance (Satterthwaite) t-test
    t_uneq, p_uneq = stats.ttest_ind(g1, g0, equal_var=False)

    # Satterthwaite DF
    s0, s1 = g0.std(ddof=1), g1.std(ddof=1)
    n0, n1 = len(g0), len(g1)
    num = (s0**2/n0 + s1**2/n1)**2
    den = (s0**2/n0)**2/(n0-1) + (s1**2/n1)**2/(n1-1)
    df_satt = num / den

    ttest_result = {
        "Method": ["Pooled (Equal Var)", "Satterthwaite (Unequal Var)"],
        "Variance": ["Equal", "Unequal"],
        "DF": [f"{n0+n1-2}", f"{df_satt:.2f}"],
        "t Value": [f"{t_eq:.2f}", f"{t_uneq:.2f}"],
        "Pr > |t|": ["<.0001" if p_eq < 0.0001 else f"{p_eq:.4f}",
                      "<.0001" if p_uneq < 0.0001 else f"{p_uneq:.4f}"],
    }
    rpt.table(pd.DataFrame(ttest_result), index=False)

    # Equality of Variances (Levene / F test)
    f_var = max(s0**2, s1**2) / min(s0**2, s1**2)
    df1_f = (n0-1) if s0**2 > s1**2 else (n1-1)
    df2_f = (n1-1) if s0**2 > s1**2 else (n0-1)
    p_ftest = 2 * min(stats.f.cdf(f_var, df1_f, df2_f),
                       1 - stats.f.cdf(f_var, df1_f, df2_f))

    levene_stat, levene_p = stats.levene(g0, g1)

    var_eq = {
        "Test": ["Folded F", "Levene's Test"],
        "Num DF": [df1_f, 1],
        "Den DF": [df2_f, n0+n1-2],
        "F Value": [f"{f_var:.2f}", f"{levene_stat:.2f}"],
        "Pr > F": [f"{p_ftest:.4f}" if p_ftest >= 0.0001 else "<.0001",
                    f"{levene_p:.4f}" if levene_p >= 0.0001 else "<.0001"],
    }
    rpt.h3(f"Equality of Variances — {dep_label}")
    rpt.table(pd.DataFrame(var_eq), index=False)

    rpt.hr()

# Distribution plots by question group
fig4, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
for i, (qval, label) in enumerate([(0, "question=0"), (1, "question=1")]):
    subset = df_ana.loc[df_ana["question"] == qval, DV]
    axes[i].hist(subset, bins=30, density=True, alpha=0.7,
                 color="#4a86c8", edgecolor="#2c5f8a", linewidth=0.5)
    x_range = np.linspace(subset.min() - 0.5, subset.max() + 0.5, 200)
    axes[i].plot(x_range, stats.norm.pdf(x_range, subset.mean(), subset.std(ddof=1)),
                 "r-", linewidth=1.5)
    axes[i].set_title(label)
    axes[i].set_ylabel("Density")
axes[-1].set_xlabel(LABEL[DV])
fig4.suptitle(f"Distribution of {LABEL[DV]} by Question Mark", fontsize=13)
fig4.tight_layout()
fig4.savefig(os.path.join(PLOT_DIR, "dist_by_question.png"), dpi=150, bbox_inches="tight")
rpt.img(fig4, f"Distribution of {LABEL[DV]} by Question Mark Group")

# Q-Q by question
fig5, axes5 = plt.subplots(1, 2, figsize=(10, 5))
for i, (qval, label) in enumerate([(0, "question=0"), (1, "question=1")]):
    subset = df_ana.loc[df_ana["question"] == qval, DV]
    sm.qqplot(subset, line="s", ax=axes5[i], markersize=3, alpha=0.5)
    axes5[i].set_title(f"Q-Q: {label}")
fig5.suptitle(f"Q-Q Plot of {LABEL[DV]} by Question Mark", fontsize=13)
fig5.tight_layout()
fig5.savefig(os.path.join(PLOT_DIR, "qq_by_question.png"), dpi=150, bbox_inches="tight")
rpt.img(fig5, f"Q-Q Plot of {LABEL[DV]} by Question Mark Group")

print(f"[Saved] plots/dist_by_question.png, qq_by_question.png")


# ═══════════════════════════════════════════════════════════════════════════════
#  13. Additional Plots
# ═══════════════════════════════════════════════════════════════════════════════
rpt.h2("Supplementary Plots")

# Boxplot of engagement by question
fig6, ax6 = plt.subplots(figsize=(6, 5))
bp_plot = ax6.boxplot(
    [df_ana.loc[df_ana["question"]==0, DV].values,
     df_ana.loc[df_ana["question"]==1, DV].values],
    labels=["0 (No)", "1 (Yes)"],
    patch_artist=True,
    boxprops=dict(facecolor="#e8eef4"),
)
ax6.set_xlabel("Question Mark")
ax6.set_ylabel(LABEL[DV])
ax6.set_title(f"Boxplot: {LABEL[DV]} by Question Mark")
fig6.tight_layout()
fig6.savefig(os.path.join(PLOT_DIR, "boxplot_question.png"), dpi=150, bbox_inches="tight")
rpt.img(fig6, f"Boxplot: {LABEL[DV]} by Question Mark")

# DV distribution overall (histogram + kernel density)
fig7, ax7 = plt.subplots(figsize=(8, 5))
ax7.hist(df_ana[DV], bins=40, density=True, alpha=0.7,
         color="#4a86c8", edgecolor="#2c5f8a", linewidth=0.5)
x_range = np.linspace(df_ana[DV].min() - 0.5, df_ana[DV].max() + 0.5, 300)
ax7.plot(x_range, stats.norm.pdf(x_range, df_ana[DV].mean(), df_ana[DV].std(ddof=1)),
         "r-", linewidth=2, label="Normal Curve")
ax7.set_xlabel(LABEL[DV])
ax7.set_ylabel("Density")
ax7.set_title(f"Distribution of {LABEL[DV]}")
ax7.legend()
fig7.tight_layout()
fig7.savefig(os.path.join(PLOT_DIR, "dv_distribution.png"), dpi=150, bbox_inches="tight")
rpt.img(fig7, f"Distribution of {LABEL[DV]}")

# Raw engagement distribution
fig8, ax8 = plt.subplots(figsize=(8, 5))
ax8.hist(df_ana["engagement"], bins=50, alpha=0.7,
         color="#4a86c8", edgecolor="#2c5f8a", linewidth=0.5)
ax8.set_xlabel(LABEL["engagement"])
ax8.set_ylabel("Frequency")
ax8.set_title(f"Distribution of {LABEL['engagement']} (Raw)")
fig8.tight_layout()
fig8.savefig(os.path.join(PLOT_DIR, "raw_engagement_dist.png"), dpi=150, bbox_inches="tight")
rpt.img(fig8, f"Distribution of {LABEL['engagement']} (highly right-skewed)")


# ═══════════════════════════════════════════════════════════════════════════════
#  14. Regression Summary (Plain Text) — for backward compat
# ═══════════════════════════════════════════════════════════════════════════════
reg_lines = []
reg_lines.append("=" * 70)
reg_lines.append("REGRESSION RESULTS  —  Booking.com Engagement Study  v2.0.0")
reg_lines.append(f"DV: {LABEL[DV]}")
reg_lines.append("Model: IV (H1–H5) + CV  |  Robust Standard Errors (HC1)")
reg_lines.append("=" * 70)

reg_lines.append(f"\n{'─'*70}")
reg_lines.append("OLS with Robust (HC1) Standard Errors")
reg_lines.append(f"{'─'*70}")
reg_lines.append(
    f"{'Variable':<22} {'Hyp':<6} {'Coeff':>10} {'SE(OLS)':>10} "
    f"{'SE(HC1)':>10} {'t(HC1)':>8} {'p(HC1)':>10} {'Sig':>5}")
reg_lines.append("─" * 70)

for pname in ["Intercept"] + ALL_X_COLS:
    hyp_tag = HYP_MAP.get(pname, "")
    coeff = res_hc.params[pname]
    se_ols_val = res_ols.bse[pname]
    se_hc_val = res_hc.bse[pname]
    t_val = res_hc.tvalues[pname]
    p_val = res_hc.pvalues[pname]
    sig = ("***" if p_val < 0.001 else
           "**"  if p_val < 0.01  else
           "*"   if p_val < 0.05  else "")
    label = LABEL.get(pname, pname)
    reg_lines.append(
        f"{label:<22} {hyp_tag:<6} "
        f"{coeff:>10.4f} {se_ols_val:>10.5f} {se_hc_val:>10.5f} "
        f"{t_val:>8.2f} {p_val:>10.4f} {sig:>5}")

reg_lines.append("─" * 70)
reg_lines.append(f"N = {N:,}   R² = {res_hc.rsquared:.4f}   "
                 f"Adj. R² = {res_hc.rsquared_adj:.4f}   "
                 f"F({int(res_hc.df_model)},{int(res_hc.df_resid)}) = "
                 f"{res_hc.fvalue:.3f},  p = {res_hc.f_pvalue:.6f}")

# VIF
reg_lines.append(f"\n{'─'*70}")
reg_lines.append("Variance Inflation Factors (VIF)")
reg_lines.append("─" * 70)
for nm in ALL_X_COLS:
    vf = vif_vals[nm]
    flag = "  ← check" if vf > 10 else ""
    reg_lines.append(f"  {LABEL.get(nm,nm):<22}  VIF = {vf:.3f}{flag}")

reg_lines.append(f"\n{'─'*70}")
reg_lines.append("Note: *** p<.001, ** p<.01, * p<.05 (two-tailed)")
reg_lines.append("      Standard errors are HC1 (robust).")
reg_lines.append("─" * 70)

reg_text = "\n".join(reg_lines)
reg_path = os.path.join(OUT_DIR, "regression_results.txt")
with open(reg_path, "w", encoding="utf-8") as f:
    f.write(reg_text)
print(f"[Saved] regression_results.txt")
print(reg_text)


# ═══════════════════════════════════════════════════════════════════════════════
#  15. Export SAS-Ready CSV
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- Exporting SAS-ready CSV ---")

sas_df = df_raw.copy()
sas_df.insert(0, "obs", range(1, len(sas_df) + 1))
sas_df["engagement"] = sas_df["like"] + sas_df["comment"] + sas_df["share"]
sas_df["log_engage"] = np.log1p(sas_df["engagement"])
sas_df["question"] = (sas_df["question"] > 0).astype(int)

RESEARCH_FIRST = [
    "obs", "id", "tweet_content",
    "like", "comment", "share", "engagement", "log_engage",
    "length", "question", "valence", "hashtag", "emoji",
    "picture", "url", "at_mention",
]
existing_cols = list(sas_df.columns)
remaining_cols = [c for c in existing_cols if c not in RESEARCH_FIRST]
ordered_cols = [c for c in RESEARCH_FIRST if c in existing_cols] + remaining_cols
sas_df = sas_df[ordered_cols]

sas_path = os.path.join(SAS_IN_DIR, "sas_ready.csv")
sas_df.to_csv(sas_path, index=False, encoding="utf-8-sig")
print(f"[Saved] sas_ready.csv  ({sas_df.shape[0]} rows × {sas_df.shape[1]} cols)")

# ═══════════════════════════════════════════════════════════════════════════════
#  16. Write HTML Report
# ═══════════════════════════════════════════════════════════════════════════════
html_path = os.path.join(OUT_DIR, "report.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(rpt.render())
print(f"\n[Saved] report.html")


# ═══════════════════════════════════════════════════════════════════════════════
#  Summary
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("  Output files saved to: analysis/python/output/")
print("  ─ report.html                  (full HTML report)")
print("  ─ stats_analysis.csv           (descriptive statistics)")
print("  ─ correlation_matrix.csv       (Pearson r matrix)")
print("  ─ correlation_significance.csv (r with significance stars)")
print("  ─ regression_results.txt       (OLS + HC1 robust SE)")
print("  SAS input saved to: analysis/sas/input/")
print("  ─ sas_ready.csv               (all columns, research vars first)")
print("  ─ plots/*.png                  (diagnostic plots)")
print("=" * 70)
print("\nDone. Script: run_statistics.py  v2.0.0")
