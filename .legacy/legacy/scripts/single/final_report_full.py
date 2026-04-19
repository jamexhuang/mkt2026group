from __future__ import annotations

# Open in Colab badge (original markdown cell)
# <a href="https://colab.research.google.com/github/jamexhuang/mkt2026group/blob/master/Final_report.ipynb" ...>

from pathlib import Path
import re

import contractions
import emoji
import nltk
import pandas as pd
from nltk.corpus import stopwords, words
from nltk.stem import PorterStemmer
from nltk.util import ngrams


def _pick_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def _load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame | None, Path]:
    repo_root = Path(__file__).resolve().parents[2]

    booking_path = _pick_existing(
        repo_root / "data" / "bookingcom.xlsx",
        repo_root / "data" / "bookingcom (1).xlsx",
    )
    if booking_path is None:
        raise FileNotFoundError("Cannot find booking data file in data/.")

    sincerity_path = repo_root / "data" / "brand_personality.xlsx"
    if not sincerity_path.exists():
        raise FileNotFoundError("Missing required file: data/brand_personality.xlsx")

    evaluative_path = repo_root / "data" / "evaluative_lexicon.xlsx"

    data = pd.read_excel(booking_path)
    sincerity = pd.read_excel(sincerity_path, sheet_name="sincerity")
    el = pd.read_excel(evaluative_path, sheet_name="Sheet1") if evaluative_path.exists() else None

    if el is None:
        print("[WARN] Missing data/evaluative_lexicon.xlsx, score-based metrics default to 0.")

    output_path = repo_root / "Final_Report_data_cleaned.xlsx"
    return data, sincerity, el, output_path


def main() -> None:
    data, sincerity, el, output_path = _load_inputs()

    # CELL 03
    data["url"] = data["tweet_content"].str.count(r"https://t\\.co/\\w+")

    # CELL 04
    data["hashtag"] = data["tweet_content"].str.count(r"#\\w+")

    # CELL 05
    # NOTE: original notebook had `!pip install emoji`; kept as comment per requirement.
    data["emoji"] = data["tweet_content"].apply(lambda x: emoji.emoji_count(str(x)))

    # CELL 06
    data["question"] = data["tweet_content"].str.replace(r"https?://\\S+", "", regex=True).str.count(r"\\?")

    # CELL 07
    data["at_mention"] = data["tweet_content"].str.count(r"@\\w+")

    # CELL 08
    data["exclamation"] = data["tweet_content"].str.replace(r"https?://\\S+", "", regex=True).str.count(r"!")

    # CELL 09
    data["text_clean1"] = (
        data["tweet_content"]
        .str.replace(r"https?://\\S+", "", regex=True)
        .str.replace(r"@\\w+", "", regex=True)
        .str.replace(r"#\\w+", "", regex=True)
        .str.replace(r"[^\\w\\s,?.!]", "", regex=True)
    )

    # CELL 10
    data["text_clean2"] = data["text_clean1"].str.lower()

    # CELL 11
    # NOTE: original notebook had `!pip install contractions`; kept as comment per requirement.
    data["text_clean3"] = data["text_clean2"].apply(lambda x: contractions.fix(str(x)))

    # CELL 12
    data["text_clean4"] = data["text_clean3"].str.replace(r"[^a-zA-Z\\s]", "", regex=True)

    # CELL 13
    nltk.download("words", quiet=True)
    english_words = set(words.words())
    data["text_clean5"] = data["text_clean4"].apply(
        lambda x: " ".join([w for w in str(x).split() if w.lower() in english_words])
    )

    # CELL 14
    data["length"] = data["text_clean5"].str.split().str.len()

    # CELL 15
    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words("english"))
    data["text_clean6"] = data["text_clean5"].apply(
        lambda x: " ".join([w for w in str(x).split() if w not in stop_words])
    )

    # MARKDOWN: Tokenize and Stem the Words
    # CELL 17
    data["tweet_tokenized"] = data["text_clean6"].apply(lambda x: str(x).split())

    # CELL 18
    ps = PorterStemmer()
    data["tweet_stemmed"] = data["tweet_tokenized"].apply(lambda tokens: [ps.stem(t) for t in tokens])

    # MARKDOWN: Count-Based Dictionary Method
    # CELL 22
    data["three_gram"] = data["tweet_tokenized"].apply(
        lambda tokens: [tuple(tokens[i : i + 3]) for i in range(len(tokens) - 2)]
    )
    data["two_gram"] = data["tweet_tokenized"].apply(
        lambda tokens: [tuple(tokens[i : i + 2]) for i in range(len(tokens) - 1)]
    )
    data["one_gram"] = data["tweet_tokenized"].apply(lambda tokens: tokens)

    # CELL 23
    sincerity_terms = set(sincerity["term"].astype(str))

    def match_terms(row: pd.Series) -> list[str]:
        matches: list[str] = []
        for grams in [row["three_gram"], row["two_gram"], row["one_gram"]]:
            for g in grams:
                term = " ".join(g) if isinstance(g, tuple) else g
                if term in sincerity_terms:
                    matches.append(term)
        return matches

    data["matched_sincerity_terms"] = data.apply(match_terms, axis=1)
    data["matched_sincerity_count"] = data["matched_sincerity_terms"].apply(len)

    # CELL 24
    data["sincerity"] = data.apply(
        lambda r: r["matched_sincerity_count"] / len(r["tweet_tokenized"]) if len(r["tweet_tokenized"]) > 0 else 0,
        axis=1,
    )

    # MARKDOWN: Score-Based Dictionary
    data["matched_valence_terms"] = [[] for _ in range(len(data))]
    data["matched_valence_scores"] = [[] for _ in range(len(data))]
    data["matched_extremity_terms"] = [[] for _ in range(len(data))]
    data["matched_extremity_scores"] = [[] for _ in range(len(data))]
    data["matched_emotionality_terms"] = [[] for _ in range(len(data))]
    data["matched_emotionality_scores"] = [[] for _ in range(len(data))]
    data["valence"] = 0.0
    data["extremity"] = 0.0
    data["emotionality"] = 0.0

    if el is not None:
        # CELL 28-29
        el_dict = dict(zip(el["term"].astype(str), el["valence"]))

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

        data[["matched_valence_terms", "matched_valence_scores"]] = data.apply(match_valence, axis=1)
        data["valence"] = data["matched_valence_scores"].apply(
            lambda x: sum([s - 4.5 for s in x]) / len(x) if len(x) > 0 else 0
        )

        # CELL 31-32
        term_col = el.columns[0]
        extremity_col = el.columns[2]
        emotionality_col = el.columns[3]

        extremity_dict = dict(zip(el[term_col].astype(str).str.lower(), el[extremity_col]))
        emotionality_dict = dict(zip(el[term_col].astype(str).str.lower(), el[emotionality_col]))

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

        data[["matched_extremity_terms", "matched_extremity_scores"]] = data["tweet_tokenized"].apply(match_extremity)
        data[["matched_emotionality_terms", "matched_emotionality_scores"]] = data["tweet_tokenized"].apply(match_emotionality)

        data["extremity"] = data["matched_extremity_scores"].apply(
            lambda x: sum([score - 4.5 for score in x]) / len(x) if len(x) > 0 else 0
        )
        data["emotionality"] = data["matched_emotionality_scores"].apply(
            lambda x: sum([score - 4.5 for score in x]) / len(x) if len(x) > 0 else 0
        )

    # CELL 34
    cta_words = [
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
    pattern = r"\\b(?:%s)\\b" % "|".join([re.escape(x) for x in cta_words])
    data["cta"] = data["tweet_content"].str.lower().str.count(pattern)

    # CELL 37-38
    print(data.head(30))
    data.to_excel(output_path, index=False)
    print(f"[OK] Wrote output: {output_path}")


if __name__ == "__main__":
    main()
