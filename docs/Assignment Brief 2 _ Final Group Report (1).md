# Assignment Brief 2: Social Media Engagement Analytics

*BMAN74042 Marketing Analytics (2025-26)*

## Assignment Details

- **Assignment Type:** Group Report (5-6 students per group)
- **Assignment Weighting:** 50% of total course marks
- **Report Length:** At most 2,500 words
- **Submission Deadline:** Friday, 15th May, 14:00

**Assignment Overview:** Focus on a single brand. Identify the text content features of interest and discuss how each feature is expected to influence the brand's social media engagement. Collect historical social media data, measure the relevant content features, and apply appropriate statistical models and analytical techniques to examine how these features affect engagement. Based on your findings, provide concrete and actionable recommendations for managers of the focal brand.

## Step-by-Step Guidance

### 1. Background

Select a focal brand that aligns with your interests (e.g., a brand you aspire to work in, or one you actively follow on social media). Provide a brief introduction to the brand, including what it does, its market positioning, its current situation and/or challenges, and your reasons for selecting it.

You should also briefly explain why social media engagement matters for this brand and why it is valuable to understand what drives it. Clearly define your engagement outcome. Engagement can be likes, shares, comments, or a combined measure (e.g., likes + shares, or likes + shares + comments).

For example, if you focus on Adidas and choose likes only as the engagement outcome, you need to briefly explain why likes are meaningful for Adidas (e.g., visibility, brand resonance, algorithmic reach, campaign evaluation).

### 2. Content Features and Hypotheses

To enhance social media engagement levels, you now consider which content features are likely to influence audience interaction on social media. The effects of these features may be either positive or negative, depending on the context (e.g., brand characteristics or norms).

At a minimum, you should analyse at least three textual features from the focal brand data. You can include more content features if relevant.

In this section, clearly introduce and discuss the content features you intend to examine. For each feature, provide a clear and precise definition and explain why it is theoretically expected to influence engagement, including the anticipated direction of the effect (for example, whether it is expected to increase or decrease engagement).

Your definitions and justifications should draw on relevant prior literature whenever possible, as incorporating existing research will strengthen your report. If prior literature is limited or unavailable, you may rely on well-developed theoretical reasoning and clearly articulated predictions (e.g., based on your own predictions).

**Example:** Suppose you select Adidas as your focal brand and focus on "likes" as your engagement metric. Based on prior literature and your own reasoning, you identify text length, emotionality, and emotional valence as three relevant textual features (you may examine more features in your actual report).

You might write something like this:

> In this study, we examine three textual content features that may influence the number of likes received by Adidas' social media posts: text length, emotionality, and emotional valence.
>
> Text length is defined as the number of recognized English words contained in a post (Citation 1). Prior research suggests that longer textual content can enhance perceived informativeness and content richness, which may, in turn, increase audience engagement (Citation 2). Accordingly, text length is expected to have a positive impact on the number of likes received by Adidas' social media posts. Hence, we propose the following hypothesis:
>
> **H1:** Text length has a positive impact on the number of likes received by Adidas' social media posts.

[After this, define and theoretically justify the remaining features in a similar manner, and then list H2 and H3.]

### 3. Data

Next, collect social media data from your focal brand. A dataset containing Twitter (now X) data for several hundred brands will be provided by the lecturer. The data were scraped using the Twitter (now X) API with Academic Research access on January 1, 2023; therefore, the most recent observations in the dataset are dated December 31, 2022.

In addition, the data were collected using the "most recent 3,200 tweets" retrieval method. Replies and retweets were removed after scraping to retain only original posts. As a result, each brand may have only several hundred tweets available for analysis. If you use this dataset, you should clearly describe how the data were collected in your report. Since you did not personally collect the data, this description could be written in the passive voice. You may write something like the following:

> The data used in this study were obtained from a publicly available dataset containing Twitter (now X) posts from [Brand's Name]. The dataset was scraped using the Twitter API with Academic Research access on February 8, 2023. Data collection followed the "most recent 3,200 tweets" retrieval method, which represents the maximum number of tweets retrievable per brand account under the API constraints. After scraping, replies and retweets were removed to ensure that only original posts were retained. Tweets containing videos were excluded, as video-based content is not the focus of this study. The final dataset for [Brand's Name] consists of [e.g., 500] tweets available for further analysis.

If this free dataset does not contain the brand you would like to study, or if you prefer not to use Twitter data, you may collect the data yourself using other feasible methods (e.g., using an online paid service such as Apify.com). Regardless of the data source, your report must clearly describe how the data were collected and any inclusion or exclusion criteria applied. The dataset should contain a sufficient number of posts (e.g., more than 100 posts) to ensure meaningful analysis.

### 4. Measurement of Variables

In this section, clearly describe how all variables used in your analysis are measured. Your dependent variable (DV) is social media engagement, based on the engagement metric you selected (e.g., number of likes, number of comments, or a composite measure such as the sum of multiple engagement indicators). Clearly explain how the engagement variable is captured and/or calculated.

In addition, clearly describe the measurement of all independent variables (IVs), namely the content features introduced in Section 2. For each feature, explain precisely how it is measured. Specifically, detail the procedures used to transform raw social media data into measurable variables. For example, to measure text length, you should describe how the text was preprocessed using a programming language (e.g., Python) and relevant text-processing tools. This may include cleaning the text content by removing emojis, URLs, and punctuation. You should then explain how recognized English words were identified and how the total word count for each post was computed. Be sure to clearly state the specific tools, packages, dictionaries, or methods used for detection and counting to ensure transparency and replicability.

If control variables (CVs) are included, such as the number of images in a post, a weekend dummy variable, time of day, or other content features that are not the primary focus but may confound the effects of the main variables (e.g., number of @mentions, number of hashtags, or number of URLs), you should briefly describe how these variables are measured/coded.

After presenting your measurement procedures, report the descriptive statistics for the DV, IVs, and CVs. At a minimum, you should report the number of observations (N), mean, standard deviation (SD), minimum, median, and maximum of each variable. If you observe any anomalies (e.g., extreme values, skewed distributions, or unusually large engagement counts), briefly note and explain why they may occur, and discuss whether they are likely to meaningfully bias your results.

### 5. Model Specifications

Before estimating the regression models, potential multicollinearity among the IVs and CVs should be assessed by calculating Variance Inflation Factors (VIFs). A VIF value of 10 should be used as a practical threshold indicating serious multicollinearity. If multicollinearity is detected (e.g., VIF >= 10), the model may be adjusted by simply removing the variable(s) contributing to the issue.

Next, an appropriate statistical technique should be selected based on the nature and distribution of the dependent variable. For count-based engagement measures (e.g., number of likes or comments), suitable models may include log-linear regression, negative binomial regression, or zero-inflated negative binomial regression. The choice of model should be explicitly justified with reference to the distributional properties of the engagement variable, such as a highly skewed distribution, overdispersion (i.e., variance exceeding the mean), or the presence of excess zeros.

Notably, prior to finalizing the specification, different combinations of CVs may be tested (e.g., by adding or removing certain control variables) and model fit statistics compared. Depending on the model type, appropriate fit measures may include $R^2$ (for log-linear regression) or pseudo-$R^2$ (for negative binomial or zero-inflated negative binomial regressions). It is not necessary to report all these intermediate model specifications in detail. For example, you can briefly note in the main text that multiple model specifications were evaluated and that the final model was selected based on superior overall model fit (i.e., the highest among the compared models) and acceptable multicollinearity levels (all VIF values below 10). This procedure should transparently guide and justify the selection of the final regression equation.

After that, the regression equation may be presented to formally specify the model (reporting only the primary equation is sufficient).

For example, if you use a log-linear method (i.e., the dependent variable is log-transformed and estimated using ordinary least squares), the equation is typically written as:

$$
\log_{10}(\mathrm{Engagement}_i + 1) = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \cdots + \beta_n X_{ni} + \varepsilon_i
$$

If a negative binomial (NB) or zero-inflated negative binomial (ZINB) regression is used, the primary equation (i.e., the mean structure) is specified a little differently from the log-linear regression equation. In this case, the left-hand side is not the observed outcome (the engagement level), but rather the logarithm of its conditional mean, $\mu_i = E(Y_i \mid X_i)$. The model is therefore written as:

$$
\log(\mu_i) = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \cdots + \beta_n X_{ni}
$$

Regardless of the method used, in these regression equations, $X_{1i}, X_{2i}, \ldots, X_{ni}$ denote the set of predictors, which may include both independent variables of substantive interest and control variables. In your report, these "Xs" symbols had better be replaced with the actual variable names.

### 6. Results

Present your regression results clearly in a well-formatted table. Ensure that all relevant statistics (e.g., coefficients, standard errors, significance levels) are accurately reported. Interpret the results carefully and avoid overly certain or causal language. Because the analysis is observational, use cautious and correlational wording such as "is associated with," "is positively related to," "tends to increase," or "is linked to," rather than implying causation. Provide an objective interpretation of the findings, clearly explaining what the estimated coefficients indicate in substantive terms. Statistically non-significant results are acceptable. However, all findings must be reported accurately and transparently. Clearly state whether each hypothesis is supported or not supported based on the statistical results.

**Example wording:**

> The regression coefficient for emotionality is positive and statistically significant ($\beta = 0.275$, $p < 0.001$), indicating that higher levels of textual emotionality are associated with a greater number of likes on Adidas' social media posts. Thus, H2 is supported.

Where appropriate, you may also include figures to visualize key relationships (e.g., regression-based predicted values illustrating how engagement changes as each content feature varies).

### 7. Managerial Suggestions

Articulate the managerial implications of your findings. Discuss whether the observed relationships align with prior literature and/or your initial expectations, and highlight any results that are surprising or counterintuitive.

More importantly, translate your results into actionable takeaways for marketers or content creators in your focal brand. Explain how they might adjust future content design to improve engagement, and provide clear, practical recommendations. Consider including concrete sample social media posts for the brand, or identifying several underperforming posts and, based on your analysis, offering specific examples of how they could be improved.

(Think about this section thoroughly, as you may want to share your findings and recommendations in a LinkedIn post targeted at the brand. Doing so could significantly enhance your professional profile.)

### 8. Limitations and Possible Improvements

Discuss the limitations of both your conclusions and your methodology. For example, a content feature that increases engagement may have negative implications for brand equity (e.g., highly emotional content may harm perceptions of competence or authenticity in the long term). Also, briefly address methodological limitations, such as limited generalisability (e.g., one platform, a short time period, etc.) and the non-experimental design (i.e., unobserved confounding may remain). Conclude by suggesting realistic improvements for future research, such as broader data coverage, additional platforms, improved measurement, or stronger research designs.

## Submission Instructions

Each student should submit one PDF document (the experiment report containing all required components) and one Excel dataset. Both files must be submitted via Canvas before the stated deadline. Late submissions will be penalized in accordance with the policies outlined in your student handbook.

When submitting your report and data, please follow the specific file-naming format. Use the course number and your student ID in the filename. The required formats are:

- `74042_Group[group-ID]_Report.pdf`
  - Example: `74042_Group5_Report.pdf`
- `74042_Group[group-ID]_Data.xlsx`
  - Example: `74042_Group5_Data.xlsx`

## Final Presentation Guidelines

Each group should deliver a project pitch presentation during the final week. The presentation should include, at a minimum:

- The research topic and research question
- The theoretical argument and proposed hypothesis(es)
- An overview of the dataset and the measurement approach (intended or implemented)
- Expected outcomes (actual results may be presented if available)
- Managerial or research suggestions, if results are already obtained

The presentation does not need to be final or perfect. The lecture will provide feedback and suggestions for improvement to help strengthen the final report.

## Marking Rubric

### 1. Background (5%)

- **Excellent (70+):** Brand is introduced concisely but with rich context (what they do, positioning, audience, current situation, and why chosen). Engagement outcome is explicitly defined (likes, shares, comments, or a combined measure) and the report persuasively explains why this metric matters in this context (visibility, resonance, algorithmic reach, campaign evaluation).
- **Good (60-69):** Background is clear and specific, but the rationale for the chosen engagement metric is somewhat general or not fully tied to the brand context.
- **Satisfactory (50-59):** Brand is introduced, but context is thin or generic. Engagement outcome is stated but importance is underdeveloped.
- **Weak (<50):** Background is unclear or minimal. Engagement outcome is not clearly defined and/or not justified.

### 2. Content Features and Hypotheses (15%)

- **Excellent (70+):** At least three textual features are clearly introduced and strongly justified. Each feature has (1) a precise definition and (2) a well-developed theoretical rationale grounded in relevant prior literature and/or rigorous independent reasoning. The expected direction of the effect (positive or negative) is clearly articulated. Formal hypotheses (H1, H2, H3, etc.) are explicitly stated and logically derived from the discussion. Scope (brand-specific) is clearly defined.
- **Good (60-69):** At least three textual features are introduced and generally appropriate. Most definitions are clear, though one may lack precision. Theoretical justification is present but may rely more on reasoning than literature, or vice versa. Directional expectations are stated but may lack depth. Hypotheses are presented but could be more tightly linked to theory.
- **Satisfactory (50-59):** Fewer than three textual features, or features are loosely justified. Definitions may be vague or not clearly operational. Theoretical reasoning is brief, underdeveloped, or weakly connected to engagement. Directional expectations are unclear or inconsistently stated. Hypotheses may be missing, poorly specified, or not logically derived.
- **Weak (<50):** Feature section is missing, unclear, or conceptually weak. Features are not clearly defined, not measurable, or not linked to engagement. No theoretical justification or hypotheses are provided. The section does not meet the minimum requirement of three textual features.

### 3. Data (15%)

- **Excellent (70+):** Data source is clearly documented (platform, brand, time window, unit of analysis, engagement variables). Data collection is transparent (provided dataset vs own collection). Cleaning steps are clearly described and justified (duplicates, missing values, irrelevant observations, language filtering, outliers if applicable). Dataset is appropriate for the research goal and described well enough to enable replication.
- **Good (60-69):** Data description is mostly clear and usable, but one or two key details are missing (time window, inclusion rules, or specific cleaning decisions) or briefly justified.
- **Satisfactory (50-59):** Basic data description is provided, but key details are unclear (how collected, what was filtered, time period). Cleaning is poorly described, reducing credibility and replicability.
- **Weak (<50):** Data source and collection are unclear or inappropriate. Cleaning and inclusion rules are missing. Dataset cannot be evaluated or is not suitable for the analysis.

### 4. Measurement of Variables (15%)

- **Excellent (70+):** DV is clearly defined and/or constructed (e.g., likes, comments, shares, composite engagement) with justification. All IVs and CVs are precisely operationalised and all CVs are theoretically justified. Measurement procedures and tools are valid, clear, and transparent. Data anomalies are discussed. Full descriptive statistics (N, mean, SD, min, median, max) are reported for DV, IVs, and CVs.
- **Good (60-69):** DV, IVs, and CVs are appropriate and reasonably measured, but some operational details, tools, or descriptives are incomplete. Justification for CVs may be limited.
- **Satisfactory (50-59):** Measurement is basic. Variables exist but are weakly defined or justified. Operationalisation is unclear. Descriptives are minimal or incomplete.
- **Weak (<50):** Variables are incorrectly defined or misaligned with the study goal. Key measurement information is missing. Descriptives are missing or incorrect.

### 5. Model Specifications (15%)

- **Excellent (70+):** Model choice is fully appropriate and rigorously justified based on the distributional characteristics of the DV (e.g., skewness, overdispersion, excess zeros). Clear explanation of why the selected technique (e.g., log-linear, negative binomial, zero-inflated NB) fits the engagement outcome. Multicollinearity is systematically assessed using VIF, threshold (10) is explicitly stated, and corrective actions are properly implemented. Model equation is clearly specified. Alternative specifications (e.g., different CV combinations) are tested and model fit statistics ($R^2$ or pseudo-$R^2$, as appropriate) are compared. Final model selection is logically justified.
- **Good (60-69):** Model is appropriate and generally justified, though distributional reasoning may lack depth. VIF is reported but discussion of threshold or corrective action may be brief. Some alternative specifications are tested, but model comparison or explanation of final selection is limited. Model equation may be presented but not fully discussed.
- **Satisfactory (50-59):** A regression model is estimated, but justification is generic or loosely linked to DV distribution. Limited discussion of overdispersion or zero inflation when relevant. VIF may be mentioned but not clearly interpreted. Model selection process is unclear, and there is little evidence of systematic comparison of alternative specifications.
- **Weak (<50):** Model choice is inappropriate for the DV distribution or incorrectly implemented. No meaningful justification is provided. Multicollinearity is not assessed or ignored. No explanation of model selection process. Major specification flaws undermine the credibility of the results.

### 6. Results (15%)

- **Excellent (70+):** Regression results are clearly presented in well-formatted tables. Coefficients, standard errors, significance levels are accurately reported. Interpretation is precise, objective, and appropriately cautious (e.g., "is associated with," "is positively related to"). No unwarranted causal claims are made. Both significant and non-significant findings are transparently discussed. Each hypothesis is explicitly evaluated (supported/not supported). Where appropriate, figures (e.g., predicted values or marginal effects plots) effectively illustrate key relationships and enhance interpretation.
- **Good (60-69):** Results are presented clearly with minor reporting or formatting issues. Interpretation is generally accurate, though wording may occasionally be slightly causal or imprecise. Most hypotheses are clearly addressed. Non-significant findings are reported but may receive limited discussion. Visualisations (if included) are relevant but may not strongly enhance interpretation.
- **Satisfactory (50-59):** Results table is present but may lack clarity, completeness, or consistency. Interpretation is basic, overly descriptive, or occasionally causal in tone. Hypotheses are not systematically evaluated. Limited discussion of non-significant results. Figures may be absent or not clearly explained.
- **Weak (<50):** Results are unclear, inaccurately reported, or poorly interpreted. Major errors in reporting coefficients or significance. Strong causal claims are made without justification. Hypotheses are not evaluated. Tables/figures are missing or misleading.

### 7. Managerial Suggestions (15%)

- **Excellent (70+):** Implications are specific, realistic, and directly derived from the findings. Recommendations are actionable for the focal brand (what to change in content, for whom, and why), and trade-offs are acknowledged where relevant (engagement vs longer-term brand equity). Evidence-based takeaways are clearly separated from speculation.
- **Good (60-69):** Implications are sensible and linked to findings but somewhat general or not fully tailored to the brand context.
- **Satisfactory (50-59):** Implications are generic, loosely connected to results, or not operational (hard to implement).
- **Weak (<50):** Implications are missing, unrealistic, or not supported by results.

### 8. Limitations and Possible Improvements (5%)

- **Excellent (70+):** Limitations are specific and thoughtful (observational design and confounding, platform-specificity, time window, measurement validity, selection and coverage issues). Improvements are realistic and well-motivated (broader platforms, longer coverage, improved feature extraction, stronger designs).
- **Good (60-69):** Limitations are relevant but brief or less specific. Improvements are reasonable but not well developed.
- **Satisfactory (50-59):** Limitations are generic and improvements are minimal.
- **Weak (<50):** Limitations are missing, incorrect, or trivial. No meaningful improvements are suggested.

**Important:** The main body of the report must not exceed 2,500 words. Any supplementary or supporting material may be included in an optional appendix. All cited sources must be listed in a reference section. The report should be presented in a professional manner, with consistent formatting throughout (e.g., uniform font, clearly structured headings, and clearly reported statistics). In the final week, each group will deliver a project pitch presentation. The quality and overall aesthetics of both the written report and the oral presentation may influence the final mark by up to +/-10%.

## Assessment Feedback and Marking

Coursework marks will be released to the AMBS assessment team within 15 working days after submission, unless you are informed otherwise.

Marks will be allocated according to the AMBS Reduced Scale Step Marking Grade Descriptors.

## Ethical Consideration

In case you conduct primary research, you need to ensure your project does not require formal University ethical approval. Normally, coursework tasks involving limited data collection are exempt, provided that:

- The topics are not sensitive or contentious
- Vulnerable subjects should not be included
- The data collected will not form the basis for a publication

In any case, and prior to commencing your research project, please email Dr Scalco and Dr Adam to receive confirmation to proceed with your project.

Additionally, please note that even if your project does not require formal ethical approval, you must still adhere to best practice guidelines:

- Guidance: <https://www.manchester.ac.uk/research/environment/governance/ethics/approval/>
- A GDPR-compliant participant information sheet and consent form
- Ethical consent must be obtained
- Audio transcripts must be anonymised, and original recordings deleted
- Data protection expectations regarding storage, confidentiality, and retention must be followed
