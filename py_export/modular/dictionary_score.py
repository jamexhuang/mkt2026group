from __future__ import annotations

from pathlib import Path

from nltk.util import ngrams
import pandas as pd


def load_evaluative_lexicon(path: Path, sheet_name: str = "Sheet1") -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name)


def _init_score_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["matched_valence_terms"] = [[] for _ in range(len(df))]
    df["matched_valence_scores"] = [[] for _ in range(len(df))]
    df["matched_extremity_terms"] = [[] for _ in range(len(df))]
    df["matched_extremity_scores"] = [[] for _ in range(len(df))]
    df["matched_emotionality_terms"] = [[] for _ in range(len(df))]
    df["matched_emotionality_scores"] = [[] for _ in range(len(df))]
    df["valence"] = 0.0
    df["extremity"] = 0.0
    df["emotionality"] = 0.0
    return df


def apply_score_based_metrics(df: pd.DataFrame, el_df: pd.DataFrame | None) -> pd.DataFrame:
    df = _init_score_columns(df)
    if el_df is None:
        return df

    el_df = el_df.copy()
    el_dict = dict(zip(el_df["term"].astype(str), el_df["valence"]))

    def match_valence(row: pd.Series) -> pd.Series:
        terms: list[str] = []
        scores: list[float] = []
        for grams in [row["two_gram"], row["one_gram"]]:
            for g in grams:
                term = " ".join(g) if isinstance(g, tuple) else g
                if term in el_dict:
                    terms.append(term)
                    scores.append(el_dict[term])
        return pd.Series([terms, scores])

    df[["matched_valence_terms", "matched_valence_scores"]] = df.apply(match_valence, axis=1)
    df["valence"] = df["matched_valence_scores"].apply(
        lambda x: sum([s - 4.5 for s in x]) / len(x) if len(x) > 0 else 0
    )

    term_col = el_df.columns[0]
    extremity_col = el_df.columns[2]
    emotionality_col = el_df.columns[3]

    extremity_dict = dict(zip(el_df[term_col].astype(str).str.lower(), el_df[extremity_col]))
    emotionality_dict = dict(zip(el_df[term_col].astype(str).str.lower(), el_df[emotionality_col]))

    def match_extremity(tokens: list[str]) -> pd.Series:
        token_list = [str(t).lower() for t in tokens]
        matched_terms: list[str] = []
        matched_scores: list[float] = []
        for n in [3, 2, 1]:
            for gram in ngrams(token_list, n):
                term = " ".join(gram)
                if term in extremity_dict:
                    matched_terms.append(term)
                    matched_scores.append(extremity_dict[term])
        return pd.Series([matched_terms, matched_scores])

    def match_emotionality(tokens: list[str]) -> pd.Series:
        token_list = [str(t).lower() for t in tokens]
        matched_terms: list[str] = []
        matched_scores: list[float] = []
        for n in [3, 2, 1]:
            for gram in ngrams(token_list, n):
                term = " ".join(gram)
                if term in emotionality_dict:
                    matched_terms.append(term)
                    matched_scores.append(emotionality_dict[term])
        return pd.Series([matched_terms, matched_scores])

    df[["matched_extremity_terms", "matched_extremity_scores"]] = df["tweet_tokenized"].apply(match_extremity)
    df[["matched_emotionality_terms", "matched_emotionality_scores"]] = df["tweet_tokenized"].apply(match_emotionality)

    df["extremity"] = df["matched_extremity_scores"].apply(
        lambda x: sum([score - 4.5 for score in x]) / len(x) if len(x) > 0 else 0
    )
    df["emotionality"] = df["matched_emotionality_scores"].apply(
        lambda x: sum([score - 4.5 for score in x]) / len(x) if len(x) > 0 else 0
    )
    return df
