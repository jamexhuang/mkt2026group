from __future__ import annotations

from pathlib import Path
import re

import contractions
import emoji
import nltk
import pandas as pd
from nltk.corpus import stopwords, words


CTA_WORDS = [
    "check out",
    "learn more",
    "book now",
    "find out",
    "discover more",
    "explore now",
    "read more",
    "click here",
    "shop now",
    "sign up",
    "join us",
    "get started",
    "see more",
    "visit now",
    "plan your trip",
]
CTA_PATTERN = r"\\b(?:%s)\\b" % "|".join([re.escape(x) for x in CTA_WORDS])


def _ensure_nltk_resources() -> None:
    nltk.download("words", quiet=True)
    nltk.download("stopwords", quiet=True)


def load_base_data(path: Path) -> pd.DataFrame:
    return pd.read_excel(path)


def add_surface_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["url"] = df["tweet_content"].str.count(r"https://t\\.co/\\w+")
    df["hashtag"] = df["tweet_content"].str.count(r"#\\w+")
    df["emoji"] = df["tweet_content"].apply(lambda x: emoji.emoji_count(str(x)))
    df["question"] = df["tweet_content"].str.replace(r"https?://\\S+", "", regex=True).str.count(r"\\?")
    df["at_mention"] = df["tweet_content"].str.count(r"@\\w+")
    df["exclamation"] = df["tweet_content"].str.replace(r"https?://\\S+", "", regex=True).str.count(r"!")
    return df


def add_cta_feature(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cta"] = df["tweet_content"].str.lower().str.count(CTA_PATTERN)
    return df


def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    _ensure_nltk_resources()
    english_words = set(words.words())
    stop_words = set(stopwords.words("english"))

    df = df.copy()
    df["text_clean1"] = (
        df["tweet_content"]
        .str.replace(r"https?://\\S+", "", regex=True)
        .str.replace(r"@\\w+", "", regex=True)
        .str.replace(r"#\\w+", "", regex=True)
        .str.replace(r"[^\\w\\s,?.!]", "", regex=True)
    )
    df["text_clean2"] = df["text_clean1"].str.lower()
    df["text_clean3"] = df["text_clean2"].apply(lambda x: contractions.fix(str(x)))
    df["text_clean4"] = df["text_clean3"].str.replace(r"[^a-zA-Z\\s]", "", regex=True)
    df["text_clean5"] = df["text_clean4"].apply(
        lambda x: " ".join([w for w in str(x).split() if w.lower() in english_words])
    )
    df["length"] = df["text_clean5"].str.split().str.len()
    df["text_clean6"] = df["text_clean5"].apply(
        lambda x: " ".join([w for w in str(x).split() if w not in stop_words])
    )
    return df
