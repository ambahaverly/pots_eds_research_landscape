"""Descriptive analysis helpers used by the Streamlit dashboard."""
from pathlib import Path
import pandas as pd

from .config import (
    CONDITION_KEYWORDS,
    EXTERNAL_CONDITIONS,
    INTRINSIC_CONCEPTS,
    MECHANISM_CONCEPTS,
    SYMPTOM_FEATURE_CONCEPTS,
)


def yearly_counts(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=["year"]).groupby("year").size().reset_index(name="papers")


def topic_year(df: pd.DataFrame, topic_columns: list[str]) -> pd.DataFrame:
    rows = []
    for col in topic_columns:
        topic = col.removeprefix("topic_")
        x = df.groupby("year")[col].sum().reset_index(name="papers")
        x["topic"] = topic
        rows.append(x)
    return pd.concat(rows, ignore_index=True)


def concept_overlap(df: pd.DataFrame) -> pd.DataFrame:
    concepts = ["POTS", "EDS", "hEDS", "MCAS"]
    rows = []
    for a in concepts:
        for b in concepts:
            if a < b:
                rows.append({"concept_a": a, "concept_b": b, "papers": int((df[f"concept_{a}"] & df[f"concept_{b}"]).sum())})
    return pd.DataFrame(rows)

def concept_connections(
    df: pd.DataFrame,
) -> dict[str, dict[str, pd.DataFrame]]:
    core = {
        "EDS": "mention_EDS",
        "hEDS": "mention_hEDS",
        "POTS": "mention_POTS",
        "MCAS": "mention_MCAS",
    }

    categories = {
        "external_conditions": EXTERNAL_CONDITIONS,
        "symptoms_features": SYMPTOM_FEATURE_CONCEPTS,
        "mechanisms": MECHANISM_CONCEPTS,
    }

    results = {}

    for label, core_col in core.items():
        mask = df[core_col]
        results[label] = {}

        for category_name, concepts in categories.items():
            rows = []

            for condition in concepts:
                col = f"condition_{condition}"
                count = int(df.loc[mask, col].sum())

                rows.append({
                    "concept": condition,
                    "papers": count,
                })

            results[label][category_name] = (
                pd.DataFrame(rows)
                .sort_values("papers", ascending=False)
                .reset_index(drop=True)
            )

    return results

def evidence_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df["evidence_level"].value_counts().rename_axis("evidence_level").reset_index(name="papers")
