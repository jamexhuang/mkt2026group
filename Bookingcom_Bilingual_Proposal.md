# How Textual Features Influence Social Media Engagement: Evidence from Booking.com on X

## Background and Motivation

Social media engagement has become an important performance indicator for brands because likes, comments, and shares reflect audience attention, interaction, and the social diffusion of branded content. For a travel platform such as Booking.com, engagement on X can be especially valuable because travel decisions are socially visible, information-intensive, and often shaped by peer endorsement. Mohammad et al. (2024) argue that social commerce interactions can strengthen credibility and influence downstream behavioral outcomes, which makes engagement a meaningful intermediate outcome for hospitality and travel brands. In this context, understanding which textual features encourage stronger engagement can help Booking.com design more effective posts and communicate more persuasively with potential travelers.

This proposal focuses on the textual design of Booking.com's posts rather than on broad brand strategy. The central idea is that the way a post is written can affect how users react to it. Prior literature suggests that content structure, interactivity cues, emotional tone, and discoverability signals can influence user responses on social media. Building on that logic, this study examines whether text length, question marks, emotional valence, and hashtags are associated with higher engagement for Booking.com posts on X, while controlling for non-textual post elements such as pictures, URLs, and at-mentions.

**中文摘要：**  
本研究以 Booking.com 在 X 上的贴文为对象，探讨「文字内容特征」是否会影响社群互动表现。对于旅游品牌而言，按赞、留言与分享不只是表面的热度，也代表受众关注、互动意愿与内容扩散潜力。因此，本 proposal 聚焦于贴文本身的写法，检验文字长度、问号、情绪正向程度与 hashtag 是否与较高的 engagement 有关，并控制图片、连结与 at-mention 等贴文元素。

## Research Question

The research question guiding this study is:

How do textual features in Booking.com's posts on X influence social media engagement?

More specifically, the study asks whether longer posts, more interactive wording through question marks, more positive emotional valence, and a greater number of hashtags are associated with higher engagement, after accounting for other post characteristics. This question is theoretically relevant because it links content design decisions to observable consumer response, and it is managerially relevant because it can guide the brand's day-to-day social media writing strategy.

**中文摘要：**  
本研究的核心问题是：Booking.com 在 X 上的贴文中，哪些文字特征会影响社群互动？进一步来说，我们关心较长的文字、问句设计、较正向的情绪语气，以及较多的 hashtag，是否会带来更高的 engagement，并在控制其他贴文特征后仍然成立。

## Hypotheses

The hypotheses are derived from prior studies on social media engagement and content design. First, longer text may provide richer information, context, and persuasive detail, which can help users understand the message and increase their willingness to engage. Gkikas et al. (2022) show that text characteristics, including length, are relevant predictors of engagement in social media contexts. In a travel setting, longer copy may also better communicate destinations, experiences, and value propositions.

Second, question marks are treated as an interactivity cue. De Vries, Gensler, and Leeflang (2012) argue that questions invite audience participation because they implicitly ask users to respond. For a brand such as Booking.com, a question can encourage users to imagine travel choices, express preferences, or reply with opinions, which should raise engagement.

Third, emotional valence captures whether the wording of a post is more positive or negative. Reddy and Prakash (2024) suggest that more positive sentiment can enhance user interaction and loyalty in social media environments. Because tourism communication often relies on aspiration, excitement, and pleasant imagery, positively valenced language is expected to generate stronger reactions.

Fourth, hashtags may improve discoverability, organize topical meaning, and connect a post to broader conversations. Kumar, Qiu, and Kumar (2022) argue that hashtags can play an important role in increasing social media audience engagement. For Booking.com, hashtags may make travel posts easier to locate and more visible within trend-based conversations, thereby improving engagement.

Based on this reasoning, the study proposes the following hypotheses:

H1. Text length is positively associated with social media engagement.  
H2. Question marks are positively associated with social media engagement.  
H3. Emotional valence is positively associated with social media engagement.  
H4. The number of hashtags is positively associated with social media engagement.

**中文摘要：**  
本研究提出四个主要假说。第一，较长的文字可能提供更多资讯与情境，因此能提升互动。第二，问号代表互动提示，会鼓励使用者回应。第三，较正向的情绪语气预期会带来更高 engagement。第四，hashtag 有助于提升可见度与话题连结，因此预期也会正向影响互动。

## Data

The study uses the cleaned dataset in [data/Final_Report_data_cleaned (2) (1).xlsx](/workspaces/mkt2026group/data/Final_Report_data_cleaned%20(2)%20(1).xlsx). The dataset contains 766 posts from Booking.com's official X account. Based on the timestamp field, the observed period runs from November 1, 2021 to November 21, 2022. The dataset includes the original post text, engagement counts, media-related indicators, and multiple preprocessed text fields generated for text analysis.

The dependent variable is a combined engagement measure defined as the sum of likes, comments, and shares. This definition is consistent with the group's current research design and is grounded in the idea that engagement reflects multiple forms of observable user interaction. In the present sample, engagement is highly right-skewed: the median combined engagement is 4, the maximum is 2,474, and 104 posts receive zero combined engagement. This pattern is typical for social media data and has implications for model choice.

The dataset is suitable for the proposed analysis because it already includes the main textual and control variables required for the study, including length, question marks, hashtags, emotional valence, pictures, URLs, at-mentions, and emoji counts.

**中文摘要：**  
本研究使用 [data/Final_Report_data_cleaned (2) (1).xlsx](/workspaces/mkt2026group/data/Final_Report_data_cleaned%20(2)%20(1).xlsx) 作为主资料集，包含 Booking.com 官方 X 帐号的 766 笔贴文，期间约为 2021 年 11 月 1 日至 2022 年 11 月 21 日。依变量设计，DV 为 likes、comments 与 shares 的加总。该资料集已包含主要自变量与控制变量，适合直接用于后续模型分析。

## Measurement of Variables

This study operationalizes all variables using fields that already exist in the cleaned dataset and the preprocessing logic documented in [py_export/single/final_report_full.py](/workspaces/mkt2026group/py_export/single/final_report_full.py). The main variables are defined as follows.

| Construct | Role | Operational definition | Dataset field |
| --- | --- | --- | --- |
| Social media engagement | Dependent variable | Sum of likes, comments, and shares for each post | Derived from `like`, `comment`, `share` |
| Text length | Main independent variable | Number of cleaned English words after removing URLs, mentions, hashtags, and non-letter symbols, then filtering to recognized English words | `length` |
| Question mark | Main independent variable | Number of question marks in the post after removing URLs | `question` |
| Emotional valence | Main independent variable | Lexicon-based sentiment score centered around neutral tone; higher values indicate more positive wording | `valence` |
| Hashtag | Main independent variable | Number of hashtags contained in the post | `hashtag` |
| Picture | Control variable | Number of pictures or visual media items attached to the post | `picture` |
| URL | Control variable | Number of URLs contained in the post | `url` |
| At-mention | Control variable | Number of `@account` mentions contained in the post | `at_mention` |
| Emoji | Extension variable | Number of emoji characters contained in the post | `emoji` |

The variable definitions are theoretically motivated and empirically grounded in the data preparation workflow. Text length captures how much verbal information a post provides. The `length` field is based on cleaned text rather than raw character count, which is appropriate because it better reflects the substantive amount of textual content available to readers. The question-mark variable captures a direct interactive cue and is measured as a count rather than a simple dummy, allowing the analysis to reflect different degrees of interrogative wording.

Emotional valence is measured with the existing `valence` field, which is generated through lexicon matching on the cleaned tokens and expresses the positivity or negativity of the language used in each post. This proposal treats valence as a continuous sentiment measure rather than splitting sentiment into separate positive and negative variables at this stage. Hashtags are measured as counts because the number of hashtags may reflect stronger discoverability or stronger topic signaling. The control variables capture non-textual or structural post elements that may affect engagement independently of writing style. Emoji is retained as an extension variable because prior literature suggests that emoji can increase engagement, but this study prioritizes a cleaner four-hypothesis core model in the main analysis.

**中文摘要：**  
本研究所有变量都直接对应现有资料栏位。DV 为 `like + comment + share`。`length` 代表清理后的英文词数，`question` 为问号数量，`valence` 为情绪正负向程度，`hashtag` 为 hashtag 数量。控制变量包括 `picture`、`url` 与 `at_mention`。`emoji` 保留为延伸模型使用，不纳入主要假说。这样的定义同时兼顾理论意义与现有资料的可操作性。

## Proposed Model Specification

The baseline empirical model examines how the four focal textual features relate to social media engagement while controlling for other post characteristics:

`Engagement_i = beta_0 + beta_1 TextLength_i + beta_2 Question_i + beta_3 Valence_i + beta_4 Hashtag_i + beta_5 Picture_i + beta_6 URL_i + beta_7 AtMention_i + error_i`

Conceptually, this specification tests whether the proposed textual features explain variation in engagement above and beyond visual or structural elements in the post. Because the dependent variable is a non-negative count-based sum and the sample shows substantial right skew, the main analysis may use `log(1 + Engagement)` as the modeled dependent variable to reduce the influence of extreme observations and improve interpretability. The conceptual definition of engagement, however, remains the raw sum of likes, comments, and shares.

To extend the model, a secondary specification will add emoji as an additional explanatory variable:

`Engagement_i = beta_0 + beta_1 TextLength_i + beta_2 Question_i + beta_3 Valence_i + beta_4 Hashtag_i + beta_5 Picture_i + beta_6 URL_i + beta_7 AtMention_i + beta_8 Emoji_i + error_i`

This second model is not intended to replace the main hypothesis structure. Instead, it functions as an extension analysis that explores whether emoji contributes explanatory value beyond the four core textual features.

**中文摘要：**  
主模型将以 engagement 为应变量，检验 `text length`、`question`、`valence` 与 `hashtag` 的影响，并控制 `picture`、`url` 与 `at_mention`。由于 engagement 分布明显右偏，实证分析时可使用 `log(1 + engagement)` 作为模型中的应变量。延伸模型再加入 `emoji`，观察其是否提供额外解释力。

## Expected Contributions and Managerial Implications

This study is expected to contribute to the literature on social media content strategy by applying content-feature theory to a travel platform brand. Much of the prior work demonstrates that content design matters, but the effects may vary across industries and brand contexts. By focusing on Booking.com, this study can show how textual features operate in a tourism-related, information-rich, and experience-oriented setting. The proposal therefore contributes both by testing established ideas in a new context and by linking theory more closely to platform-level content decisions.

From a managerial perspective, the results are expected to help Booking.com refine how it writes posts on X. If the proposed relationships are supported, managers may be encouraged to use more informative text, strategically include questions that invite response, maintain a more positive emotional tone, and use hashtags in ways that improve discoverability. The extension analysis on emoji may also indicate whether visual-linguistic cues are worth incorporating more systematically into social media copy. Overall, the project aims to turn textual features into actionable content guidelines rather than treating engagement as a purely descriptive metric.

**中文摘要：**  
本研究的贡献在于把社群内容特征理论应用到旅游平台品牌情境，并将抽象的文字设计问题转化为可执行的管理建议。若假说获得支持，Booking.com 可进一步优化贴文写法，例如写得更有资讯量、适度使用提问句、维持较正向的语气，并策略性使用 hashtag。延伸模型也可帮助判断 emoji 是否值得纳入常规内容设计。

## Limitations and Next Steps

Several limitations should be acknowledged at the proposal stage. First, the dependent variable combines likes, comments, and shares using equal weights. This is analytically convenient and consistent with the current project design, but the three actions may not reflect identical levels of user involvement. Second, the study focuses on a single brand, which improves contextual consistency but limits generalizability. Third, the text-cleaning process may introduce some language bias because non-English or mixed-language expressions can be simplified or excluded during preprocessing. Fourth, the proposal is theory-driven and measurement-driven; it does not claim empirical confirmation before the statistical analysis is completed.

The next step is to estimate the proposed models, assess whether the hypothesized signs are supported, and compare the baseline model with the emoji extension model. After that, the final report can expand the descriptive statistics, present regression results, discuss robustness checks, and translate the findings into more specific managerial recommendations.

**中文摘要：**  
本研究也有几项限制。第一，DV 以 likes、comments 与 shares 等权加总，但三者未必代表相同程度的参与。第二，仅分析 Booking.com 单一品牌，因此外部推广性有限。第三，文字清理流程可能对非英文内容产生偏误。第四，目前 proposal 仅提出理论与测量架构，不代表已获得实证结果。下一步将是正式跑模型、比较主模型与 emoji 延伸模型，并在 final report 中补上结果与稳健性检验。

## References (Selected)

De Vries, L., Gensler, S. and Leeflang, P.S.H. (2012). Popularity of brand posts on brand fan pages: An investigation of the effects of social media marketing. *Journal of Interactive Marketing*, 26(2), 83-91.

Gkikas, D. C., Tzafilkou, K., Theodoridis, P. K., Garmpis, A. and Gkikas, M. C. (2022). How do text characteristics impact user engagement in social media posts? Modeling content readability, length, and hashtags number in Facebook. *International Journal of Information Management Data Insights*, 2, 100067.

Ko, E.E., Kim, D. and Kim, G. (2022). Influence of emojis on user engagement in brand-related user-generated content. *Computers in Human Behavior*.

Kumar, N., Qiu, L. and Kumar, S. (2022). A hashtag is worth a thousand words: An empirical investigation of social media strategies in trademarking hashtags. *Information Systems Research*, 33(4), 1403-1427.

Li, Y. and Xie, Y. (2020). Is a picture worth a thousand words? An empirical study of image content and social media engagement. *Journal of Marketing Research*, 57(1), 1-19.

Mohammad, A.A., Elshaer, I.A., Azazz, A.M., Kooli, C., Algezawy, M. and Fayyad, S. (2024). The influence of social commerce dynamics on sustainable hotel brand image, customer engagement, and booking intentions. *Sustainability*, 16(14), 6050.

Moran, G., Muzellec, L. and Johnson, D. (2019). Message content features and social media engagement: evidence from the media industry. *Journal of Product and Brand Management*, 29(5), 533-545.

Reddy, M.A.S. and Prakash, C. (2024). Sentiment Analysis of Social Media Networking Sites: A Comparative Study on User Engagement and Public Opinion.

van der Harst, J.P. and Angelopoulos, S. (2024). Less is more: Engagement with the content of social media influencers. *Journal of Business Research*, 181, 114746.
