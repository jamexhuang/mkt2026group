from __future__ import annotations

import pandas as pd
from nltk.stem import PorterStemmer


def tokenize_and_stem(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["tweet_tokenized"] = df["text_clean6"].apply(lambda x: str(x).split())

    ps = PorterStemmer()
    df["tweet_stemmed"] = df["tweet_tokenized"].apply(lambda tokens: [ps.stem(t) for t in tokens])

    df["three_gram"] = df["tweet_tokenized"].apply(
        lambda tokens: [tuple(tokens[i : i + 3]) for i in range(len(tokens) - 2)]
    )
    df["two_gram"] = df["tweet_tokenized"].apply(
        lambda tokens: [tuple(tokens[i : i + 2]) for i in range(len(tokens) - 1)]
    )
    df["one_gram"] = df["tweet_tokenized"].apply(lambda tokens: tokens)
    return df
