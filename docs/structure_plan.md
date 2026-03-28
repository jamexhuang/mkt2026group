# 專案目錄整理計劃

## 目標結構

```
mkt2026group/
├── README.md                        # 群組討論筆記（保留在根目錄）
├── .gitignore
├── .git/
│
├── docs/                            # 文件與報告
│   ├── citation_check_report.md    # 從根目錄移入
│   ├── column_mapping.md           # 從 data/ 移入（屬於文件類）
│   └── structure_plan.md           # 本文件
│
├── paper/                           # 論文主文件（LaTeX）
│   ├── src/                         # LaTeX 源碼
│   │   ├── Bookingcom_Bilingual_Proposal.tex
│   │   ├── Statistical_Results.tex
│   │   └── Bookingcom_Bilingual_Proposal.log
│   └── output/                      # 論文輸出
│       ├── Bookingcom_Bilingual_Paper.docx
│       └── Bookingcom_Bilingual_Proposal.pdf  (最終版)
│
├── data/                            # 數據文件
│   ├── raw/                         # 原始數據
│   │   ├── Final_Report_data_cleaned (2) (1).xlsx
│   │   └── brand_personality.xlsx
│   ├── processed/                   # 處理後數據
│   │   ├── research_data.csv        # 主要研究數據
│   │   └── sas_ready.csv           # SAS 分析用數據（合併）
│   └── references/                  # 參考文獻
│       └── papers/
│           ├── Gkikas2022.pdf
│           ├── Harst2024.pdf
│           └── ... (其他論文)
│
├── analysis/                        # 統計分析腳本
│   ├── sas/                         # SAS 腳本
│   │   └── Booking_Engagement_Analysis.sas   (最新版)
│   ├── python/                      # Python 腳本
│   │   └── run_statistics.py        (最新版)
│   └── output/                      # 分析輸出
│       ├── correlation_matrix.csv
│       ├── correlation_significance.csv
│       ├── regression_results.txt
│       ├── stats_analysis.csv
│       └── 結果_ 程式 1.sas.html
│
└── .legacy/                         # 舊版本（保留不刪除）
    ├── Final_report.ipynb
    ├── py_export/
    │   ├── modular/
    │   └── single/
    └── tmp/
        └── James.sas
```

## 移動計劃（不刪除任何文件）

1. 建立 `docs/` 目錄
   - 移動 `citation_check_report.md` → `docs/`
   - 移動 `data/column_mapping.md` → `docs/`

2. 建立 `paper/` 新結構（整合 LaTeX 和 LaTeX_output）
   - 移動 `LaTeX/*.tex`, `LaTeX/*.log` → `paper/src/`
   - 移動 `LaTeX/*.docx` → `paper/output/`
   - 移動 `LaTeX_output/*.pdf` → `paper/output/`
   - 移動 `LaTeX/*.pdf` → `paper/output/draft/`（舊版本保留）

3. 建立 `analysis/` 目錄（整合 Statics 和 paper 中的腳本）
   - 移動 `Statics/Booking_Engagement_Analysis.sas` → `analysis/sas/`
   - 移動 `Statics/run_statistics.py` → `analysis/python/`
   - 移動 `Statics/output/*` → `analysis/output/`
   - 移動 `Statics/raw_output/*` → `analysis/output/raw/`
   - 將 `paper/` 舊腳本歸入 `.legacy/`

4. 整理 `data/` 目錄
   - 建立 `data/raw/` 和 `data/processed/`
   - 移動原始 Excel 文件 → `data/raw/`
   - 移動 CSV 文件 → `data/processed/`
   - 移動 `data/papers/` → `data/references/papers/`
