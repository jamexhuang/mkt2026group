# Column Mapping: Dataset Fields ↔ Proposal Constructs

> **Source file:** `data/Final_Report_data_cleaned (2) (1).xlsx`  
> **Output file:** `data/research_data.csv`  
> **Proposal reference:** `Bookingcom_Bilingual_Proposal.tex`  
> **Total rows:** 766 posts，2021-11-01 ~ 2022-11-21  
> **Encoding:** UTF-8 with BOM（`utf-8-sig`），emoji 與非 ASCII 字元完整保留

---

## Part 1 — Research Variables（研究用欄位，放前 13 欄）

| 欄位位置（CSV 列） | Dataset 欄位名稱 | Proposal 構念 (EN) | Proposal 欄位名稱 | 角色 |
|:---:|:---|:---|:---|:---|
| A | `id` | Post identifier | `id` | 識別碼 (ID) |
| B | `tweet_content` | Raw post text | `tweet_content` | 原始貼文內容 |
| C | `like` | Likes count | `like` | 依變數組成（DV component） |
| D | `comment` | Comments count | `comment` | 依變數組成（DV component） |
| E | `share` | Shares count | `share` | 依變數組成（DV component） |
| F | `length` | Text length | `length` | 主要自變數（Main IV） |
| G | `question` | Question mark count | `question` | 主要自變數（Main IV） |
| H | `valence` | Emotional valence | `valence` | 主要自變數（Main IV） |
| I | `hashtag` | Hashtag count | `hashtag` | 主要自變數（Main IV） |
| J | `picture` | Picture / media count | `picture` | 控制變數（Control） |
| K | `url` | URL count | `url` | 控制變數（Control） |
| L | `at_mention` | At-mention count | `at_mention` | 控制變數（Control） |
| M | `emoji` | Emoji count | `emoji` | 延伸變數（Extension IV） |

> **Dependent Variable（依變數）：**  
> `Engagement_i = like_i + comment_i + share_i`  
> 或 log 轉換版：`log(1 + Engagement_i)`

---

## Part 2 — Non-Research Variables（非研究核心欄位，排後面）

| Dataset 欄位名稱 | 說明 | 是否出現在 Proposal |
|:---|:---|:---:|
| `tt_account` | 帳號名稱（固定為 Booking.com） | ✗ |
| `date` | 貼文日期時間戳記 | ✗（僅描述觀察期間） |
| `text_clean1` | 第一階段清理文字（移除 URL 等） | ✗（前處理中間產物） |
| `exclamation` | 驚嘆號數量 | ✗ |
| `text_clean2` | 第二階段清理文字 | ✗ |
| `text_clean3` | 第三階段清理文字 | ✗ |
| `text_clean4` | 第四階段清理文字 | ✗ |
| `text_clean5` | 第五階段清理文字 | ✗ |
| `text_clean6` | 第六階段清理文字（最終清理版） | ✗ |
| `tweet_tokenized` | 斷詞結果 | ✗ |
| `tweet_stemmed` | 詞幹化結果 | ✗ |
| `three_gram` | Trigrams | ✗ |
| `two_gram` | Bigrams | ✗ |
| `one_gram` | Unigrams | ✗ |
| `matched_sincerity_terms` | 誠意維度匹配詞彙 | ✗ |
| `matched_sincerity_count` | 誠意匹配詞數量 | ✗ |
| `sincerity` | 誠意分數（品牌個性維度） | ✗ |
| `matched_valence_terms` | 情感極性匹配詞彙 | ✗（valence 最終分數才用） |
| `matched_valence_scores` | 各匹配詞的 valence 分數列表 | ✗（中間計算值） |
| `matched_extremity_terms` | 極端性匹配詞彙 | ✗ |
| `matched_extremity_scores` | 極端性分數列表 | ✗ |
| `matched_emotionality_terms` | 情緒性匹配詞彙 | ✗ |
| `matched_emotionality_scores` | 情緒性分數列表 | ✗ |
| `extremity` | 極端性分數（品牌個性維度） | ✗ |
| `emotionality` | 情緒性分數（品牌個性維度） | ✗ |

---

## Notes / 備注

1. **欄位名稱一致性**：Dataset 中的欄位名稱（如 `at_mention`、`valence`）與 Proposal 中的 Dataset field 欄完全一致，**無需改名**。
2. **Emoji 保留**：`tweet_content` 中包含 emoji（如 🏔️ 👇 🌊 ✈️）及其他 Unicode 字元；CSV 使用 `utf-8-sig` 編碼確保完整保留，共 399 筆含非 ASCII 字元。
3. **不刪行**：全部 766 筆資料完整保留，No rows dropped。
4. **Derived variable**：`engagement`（= `like + comment + share`）在 CSV 中**未建立為新欄位**，保持 proposal 原始設計由三欄推導，以利分析彈性（亦可加 `log(1+engagement)` 版本）。
5. **Extension variable**：`emoji` 雖非主假說核心，但 Proposal 明確定義為 extension variable，故歸入研究用欄位（前 13 欄）。
