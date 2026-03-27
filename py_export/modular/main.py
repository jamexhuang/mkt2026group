from __future__ import annotations

from pathlib import Path

from dictionary_count import apply_sincerity_scores, load_sincerity_dictionary
from dictionary_score import apply_score_based_metrics, load_evaluative_lexicon
from export import export_to_excel
from preprocess import add_cta_feature, add_surface_features, clean_text, load_base_data
from tokenize_stem import tokenize_and_stem


def _pick_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def run_pipeline() -> Path:
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
    evaluative_df = None
    if evaluative_path.exists():
        evaluative_df = load_evaluative_lexicon(evaluative_path)
    else:
        print("[WARN] Missing data/evaluative_lexicon.xlsx, score-based metrics default to 0.")

    output_path = repo_root / "Final_Report_data_cleaned.xlsx"

    data = load_base_data(booking_path)
    data = add_surface_features(data)
    data = clean_text(data)
    data = tokenize_and_stem(data)

    sincerity_df = load_sincerity_dictionary(sincerity_path, sheet_name="sincerity")
    data = apply_sincerity_scores(data, sincerity_df)
    data = apply_score_based_metrics(data, evaluative_df)
    data = add_cta_feature(data)

    export_to_excel(data, output_path)
    print(f"[OK] Wrote output: {output_path}")
    return output_path


if __name__ == "__main__":
    run_pipeline()
