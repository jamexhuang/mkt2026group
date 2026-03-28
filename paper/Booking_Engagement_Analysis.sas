OPTIONS NODATE NONUMBER LS=120 PS=60;

/* ============================================================
   Booking_Engagement_Analysis.sas
   Booking.com Social Media Engagement Study
   2026-03-28

   Purpose:
     Run the paper's descriptive statistics, correlations,
     OLS models, and diagnostics in SAS without CSV type issues.

   Workflow:
     1. Run paper/run_statistics.py locally to generate sas_ready.csv
     2. Upload sas_ready.csv to SAS Studio
     3. Update %LET datapath below to the uploaded file path
   ============================================================ */

/* CHANGE this path in SAS Studio to where you uploaded sas_ready.csv */
%LET datapath = /home/u59551696/sasuser.v94/sas_ready.csv;

/* Optional ODS output folder. Leave blank to suppress file output. */
%LET outpath  = ;

/* ── 1. Import the analysis-ready CSV with explicit types ───────────── */
DATA work.engage;
    infile "&datapath"
        dsd
        firstobs=2
        truncover
        lrecl=32767
        termstr=lf
        encoding='utf-8';

    length id $32;

    informat
        obs         best32.
        id          $32.
        like        best32.
        comment     best32.
        share       best32.
        engagement  best32.
        log_engage  best32.
        length      best32.
        question    best32.
        valence     best32.
        hashtag     best32.
        picture     best32.
        url         best32.
        at_mention  best32.
        emoji       best32.;

    format
        obs         best12.
        id          $32.
        like        best12.
        comment     best12.
        share       best12.
        engagement  best12.
        log_engage  12.6
        length      best12.
        question    best12.
        valence     12.6
        hashtag     best12.
        picture     best12.
        url         best12.
        at_mention  best12.
        emoji       best12.;

    input
        obs
        id :$32.
        like
        comment
        share
        engagement
        log_engage
        length
        question
        valence
        hashtag
        picture
        url
        at_mention
        emoji;
RUN;

TITLE "Data Preview — First 10 Observations";
PROC PRINT DATA=work.engage(OBS=10); RUN;
TITLE;

/* ── 2. Descriptive Statistics ──────────────────────────────────────── */
TITLE "Table 1. Descriptive Statistics";
PROC MEANS DATA=work.engage
    N MEAN STD MIN P25 MEDIAN P75 MAX SKEWNESS KURTOSIS
    MAXDEC=4;
    VAR engagement log_engage length question valence
        hashtag picture url at_mention emoji;
    LABEL
        engagement   = "Engagement (raw)"
        log_engage   = "log(1+Engagement)"
        length       = "Text Length (words)"
        question     = "Question Mark (0/1)"
        valence      = "Emotional Valence"
        hashtag      = "Hashtag Count"
        picture      = "Picture Count"
        url          = "URL Count"
        at_mention   = "At-Mention Count"
        emoji        = "Emoji Count";
RUN;
TITLE;

TITLE "Table 1b. Question Mark — Frequency Distribution";
PROC FREQ DATA=work.engage;
    TABLES question / NOCUM;
    LABEL question = "Question Mark (0=No, 1=Yes)";
RUN;
TITLE;

/* ── 3. Pearson Correlation Matrix ──────────────────────────────────── */
TITLE "Table 2. Pearson Correlation Matrix";
PROC CORR DATA=work.engage NOSIMPLE NOPROB;
    VAR log_engage length question valence hashtag
        picture url at_mention emoji;
    LABEL
        log_engage   = "log(1+Engagement)"
        length       = "Text Length"
        question     = "Question Mark"
        valence      = "Emotional Valence"
        hashtag      = "Hashtag"
        picture      = "Picture"
        url          = "URL"
        at_mention   = "At-Mention"
        emoji        = "Emoji";
RUN;
TITLE;

TITLE "Table 2b. Pearson Correlation Matrix (with p-values)";
PROC CORR DATA=work.engage NOSIMPLE;
    VAR log_engage length question valence hashtag
        picture url at_mention emoji;
RUN;
TITLE;

/* ── 4. OLS Regression ──────────────────────────────────────────────── */
TITLE "Table 3. OLS Regression — Model 1: Baseline";
PROC REG DATA=work.engage PLOTS=NONE;
    MODEL log_engage = length question valence hashtag
                       picture url at_mention
             / STB VIF CLB TOL;
    LABEL
        log_engage = "DV: log(1+Engagement)"
        length     = "H1: Text Length"
        question   = "H2: Question Mark"
        valence    = "H3: Emotional Valence"
        hashtag    = "H4: Hashtag Count"
        picture    = "Picture (control)"
        url        = "URL (control)"
        at_mention = "At-Mention (control)";
    OUTPUT OUT=work.resid1
           PREDICTED=yhat1 RESIDUAL=e1 RSTUDENT=rstud1 H=leverage1;
RUN;
QUIT;
TITLE;

TITLE "Table 4. OLS Regression — Model 2: Extension (+Emoji)";
PROC REG DATA=work.engage PLOTS=NONE;
    MODEL log_engage = length question valence hashtag
                       picture url at_mention emoji
             / STB VIF CLB TOL;
    LABEL
        log_engage = "DV: log(1+Engagement)"
        length     = "H1: Text Length"
        question   = "H2: Question Mark"
        valence    = "H3: Emotional Valence"
        hashtag    = "H4: Hashtag Count"
        picture    = "Picture (control)"
        url        = "URL (control)"
        at_mention = "At-Mention (control)"
        emoji      = "Emoji (extension)";
    OUTPUT OUT=work.resid2
           PREDICTED=yhat2 RESIDUAL=e2 RSTUDENT=rstud2 H=leverage2;
RUN;
QUIT;
TITLE;

/* ── 5. Residual Diagnostics (Model 1) ─────────────────────────────── */
TITLE "Table 5. Residual Normality Test — Model 1 (Shapiro-Wilk)";
PROC UNIVARIATE DATA=work.resid1 NORMAL;
    VAR e1;
    HISTOGRAM e1 / NORMAL;
    QQPLOT    e1 / NORMAL(MU=EST SIGMA=EST);
RUN;
TITLE;

DATA work.resid1_sq;
    SET work.resid1;
    e1_sq = e1**2;
RUN;

TITLE "Table 5b. Heteroscedasticity Check — Breusch-Pagan Approximation";
PROC REG DATA=work.resid1_sq PLOTS=NONE;
    MODEL e1_sq = length question valence hashtag picture url at_mention;
RUN;
QUIT;
TITLE;

/* ── 6. Robust Standard Errors ─────────────────────────────────────── */
TITLE "Table 6. Robust OLS — Model 1";
PROC SURVEYREG DATA=work.engage VARMETHOD=TAYLOR;
    MODEL log_engage = length question valence hashtag
                       picture url at_mention / SOLUTION;
RUN;
TITLE;

TITLE "Table 6b. Robust OLS — Model 2";
PROC SURVEYREG DATA=work.engage VARMETHOD=TAYLOR;
    MODEL log_engage = length question valence hashtag
                       picture url at_mention emoji / SOLUTION;
RUN;
TITLE;

/* ── 7. Model Comparison ───────────────────────────────────────────── */
TITLE "Supplementary: Model Comparison — Model 1 vs Model 2";
PROC REG DATA=work.engage PLOTS=NONE;
    M1: MODEL log_engage = length question valence hashtag
                           picture url at_mention;
    M2: MODEL log_engage = length question valence hashtag
                           picture url at_mention emoji;
RUN;
QUIT;
TITLE;

/* ── 8. Mean comparison by question dummy ──────────────────────────── */
TITLE "Table 7. Mean Engagement by Question Mark (t-test)";
PROC TTEST DATA=work.engage;
    CLASS question;
    VAR log_engage engagement;
RUN;
TITLE;

%PUT ==================================================;
%PUT Booking.com Engagement Analysis DONE.;
%PUT Check tables above for coefficients, fit, and diagnostics.;
%PUT ==================================================;
