from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = REPO_ROOT / "data" / "research_data.csv"
OUTPUT_CSV = Path(__file__).resolve().with_name("sas_ready.csv")

NUMERIC_COLUMNS = [
    "like",
    "comment",
    "share",
    "length",
    "question",
    "valence",
    "hashtag",
    "picture",
    "url",
    "at_mention",
    "emoji",
]


def main() -> None:
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Missing source CSV: {SOURCE_CSV}")

    df = pd.read_csv(SOURCE_CSV)

    missing = [col for col in NUMERIC_COLUMNS if col not in df.columns]
    if missing:
        raise KeyError(f"Missing expected columns: {missing}")

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="raise")

    # Match the paper's measurement choices for SAS analysis.
    out = pd.DataFrame(
        {
            "obs": np.arange(1, len(df) + 1, dtype=int),
            "id": df["id"].astype(str),
            "like": df["like"].astype(int),
            "comment": df["comment"].astype(int),
            "share": df["share"].astype(int),
            "engagement": (df["like"] + df["comment"] + df["share"]).astype(int),
            "log_engage": np.log1p(df["like"] + df["comment"] + df["share"]),
            "length": df["length"].astype(int),
            "question": (df["question"] > 0).astype(int),
            "valence": df["valence"].astype(float),
            "hashtag": df["hashtag"].astype(int),
            "picture": df["picture"].astype(int),
            "url": df["url"].astype(int),
            "at_mention": df["at_mention"].astype(int),
            "emoji": df["emoji"].astype(int),
        }
    )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT_CSV, index=False, lineterminator="\n")

    print(f"[OK] wrote {OUTPUT_CSV}")
    print(f"[OK] rows={len(out)} cols={len(out.columns)}")
    print(out.head().to_string(index=False))


if __name__ == "__main__":
    main()
