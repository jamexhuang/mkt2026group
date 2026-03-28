libname student "C:\NSTC\SAS";run;


data student.james01; set James1; run;

/**
 * a01 is the dataset in the work library.
 */
data a01; set student.james01; run;

/**
 * save the dataset "a01" to the "student" library.
 */
data student.a01_20250515; set a01; run;

/**
 * pour the data from the "student.a01_20250327" dataset
 * back to the "a01" dataset.
 */

data a01; set student.a01_20250515; run;


/*Sort data*/

proc sort data=a01 out=a01; by CODE year; run;


/*處理字*/
data a01;
  set a01;
  if TOT_HH = '-' then TOT_HH_NUM = .;
  else TOT_HH_NUM = input(TOT_HH, best12.);
  drop TOT_HH;
  rename TOT_HH_NUM = TOT_HH;
run;

/*Scale IE because too small*/
data a01;
  set a01;
  IE_scaled = ie * 10000;
run;


/*Add Dummy*/

data a01; set a01;
if Year =2016 then Y2016 = 1;  else Y2016 =0;
if Year =2017 then Y2017 = 1;  else Y2017 =0;
if Year =2018 then Y2018 = 1;  else Y2018 =0;
if Year =2019 then Y2019 = 1;  else Y2019 =0;
if Year =2020 then Y2020 = 1;  else Y2020 =0;
if Year =2021 then Y2021 = 1;  else Y2021 =0;
run;


data a01;
  set a01;
  array SIC[38] SIC1-SIC38;
  do i = 1 to 38;
    if INDUST = i then SIC[i] = 1; 
    else SIC[i] = 0;
  end;
  drop i;
run;



data a01; set a01;
 log_asset = Log(at)+1; run;

/*計算LOG*/
data a01;
    set a01;

    log_EMP = log(EMP / median_SIZE);
    log_BEH = log(BEH / median_SIZE);
    log_COM = log(COM / median_SIZE);
    log_TOT = log(TOT / median_SIZE);
    log_SIZE = log(SIZE);
run;

/*刪掉重算*/
data a01;
   set a01;
   drop log_EMP log_BEH log_COM log_TOT;
run;

/* 1. 算產業SIZE中位數 */
proc means data=a01 noprint nway;
   class INDUST YEAR;
   var SIZE;
   output out=median_table (keep=INDUST YEAR median_SIZE) median=median_SIZE;
run;

proc sql;
   create table a01 as
   select 
      a.*, 
      b.median_SIZE 
   from 
      a01 as a
   left join 
      median_table as b
   on 
      a.INDUST = b.INDUST and
      a.YEAR = b.YEAR;
quit;
/*以上算產業size中位數*/



PROC CONTENTS DATA=a01;
RUN;

/*********************** Descriptive Statistics ***********************/


ODS EXCEL FILE="C:\NSTC\SAS\Excel\Descriptive_Statistics.xlsx" 
    OPTIONS(SHEET_NAME="Descriptive Statistics" EMBEDDED_TITLES="YES");

PROC MEANS DATA=a01 N MEAN MEDIAN MAX MIN STD;
    VAR IE_Scaled RND_RATE RND PATENT_CNT log_BEH log_COM log_EMP log_TOT log_SIZE LEV
	INDUST FAMI GEND TUR log_TRANS ESG BEH_H COM_H EMP_H TOT_H TOT_HH;
    TITLE "Table 3 Descriptive Statistics";
RUN;

ODS EXCEL CLOSE;
TITLE;

/*********************** CORRELATION ***********************/


ODS EXCEL FILE="C:\NSTC\SAS\Excel\Correlation.xlsx" 
    OPTIONS(EMBEDDED_TITLES="YES");

PROC CORR DATA=a01 NOSIMPLE;
    VAR IE_Scaled RND_RATE RND PATENT_CNT log_BEH log_COM log_EMP log_TOT log_SIZE LEV
	INDUST FAMI GEND TUR log_TRANS ESG BEH_H COM_H EMP_H TOT_HH;
    TITLE "Correlation Analysis";
RUN;

ODS EXCEL CLOSE;

/*********************** T-TEST ***********************/
PROC SQL NOPRINT;
    SELECT MEAN(IE) INTO :mean_ie
    FROM a01;
QUIT;

DATA a01;
    SET a01;
    IF IE >= &mean_ie. THEN IE_D = 1;
    ELSE IE_D = 0;
RUN;


ods select none;                
ods output TTests = work.ttest_results;  

PROC ttest data=a01;
    class IE_D;
    var log_EMP log_BEH log_COM log_TOT
        log_TRANS
        log_SIZE LEV INDUST FAMI GEND TUR
        ESG BEH_H COM_H EMP_H TOT_H TOT_HH;
run;

ods select all;                 

proc print data=work.ttest_results noobs label;
    var Variable Method Variances DF tValue Probt; 
    label 
        Variable = "變數"
        Method   = "方法"
        Variances= "變異數假設"
        DF       = "自由度"
        tValue   = "t 值"
        Probt    = "Pr > |t|";
run;

/*********************** NPAR TEST ***********************/

ods select none;
ods output WilcoxonTest = work.wilcoxon_results;

PROC NPAR1WAY data=a01 WILCOXON;
    class IE_D;
    var log_EMP log_BEH log_COM log_TOT
        log_TRANS
        log_SIZE LEV INDUST FAMI GEND TUR
        ESG BEH_H COM_H EMP_H TOT_H TOT_HH;
run;

ods select all;

proc print data=work.wilcoxon_results noobs label;
    var Variable Statistic Z Prob2;  
    label 
        Variable  = "變數"
        Statistic = "Wilcoxon統計值"
        Z         = "Z"
        Prob2     = "Pr > |Z|";
run;


/*********************** Class Means ***********************/

%let variables = log_EMP log_BEH log_COM log_TOT
                 log_TRANS
                 log_SIZE LEV INDUST FAMI GEND TUR
                 ESG BEH_H COM_H EMP_H TOT_H TOT_HH;


proc means data=a01 mean noprint;
    class IE_D;
    var &variables.;
    output out=work.class_means (drop=_TYPE_ _FREQ_) 
           mean= 
           / autoname;
run;


proc print data=work.class_means noobs label;
    label IE_D = "Class";
    /* 設定變數標籤 */
    %macro set_labels;
        %local i var;
        %let i=1;
        %do %while (%scan(&variables.,&i) ne );
            %let var = %scan(&variables.,&i);
            label &var._Mean = "&var Means";
            %let i=%eval(&i+1);
        %end;
    %mend;
    %set_labels;
run;