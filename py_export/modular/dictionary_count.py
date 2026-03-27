from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_sincerity_dictionary(path: Path, sheet_name: str = "sincerity") -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name)


def apply_sincerity_scores(df: pd.DataFrame, sincerity_df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    sincerity_terms = set(sincerity_df["term"].astype(str))

    def match_terms(row: pd.Series) -> list[str]:
        matches: list[str] = []
        for grams in [row["three_gram"], row["two_gram"], row["one_gram"]]:
            for g in grams:
                term = " ".join(g) if isinstance(g, tuple) else g
                if term in sincerity_terms:
                    matches.append(term)
        return matches

    df["matched_sincerity_terms"] = df.apply(match_terms, axis=1)
    df["matched_sincerity_count"] = df["matched_sincerity_terms"].apply(len)
    df["sincerity"] = df.apply(
        lambda r: r["matched_sincerity_count"] / len(r["tweet_tokenized"]) if len(r["tweet_tokenized"]) > 0 else 0,
        axis=1,
    )
    return df
