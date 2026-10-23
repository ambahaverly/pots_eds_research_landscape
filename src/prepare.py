"""Clean PubMed records and create analysis-ready features."""
import json
import re
from pathlib import Path

import pandas as pd

from .config import (
    CONDITION_KEYWORDS,
    PROCESSED_DIR,
    RAW_DIR,
    TOPIC_KEYWORDS,
)


def extract_year(value: str):
    match = re.search(r"(19|20)\d{2}", str(value))
    return int(match.group(0)) if match else None

def contains_any(text: str, terms: list[str]) -> bool:
    text = text.lower()

    for term in terms:
        pattern = r"\b" + re.escape(term.lower()) + r"\b"
        if re.search(pattern, text):
            return True

    return False

def evidence_level(types: list[str]) -> str:
    t = {x.lower() for x in types}
    if any("randomized controlled trial" in x for x in t):
        return "Randomized controlled trial"
    if any(x in t for x in {"controlled clinical trial", "clinical trial"}):
        return "Clinical/controlled trial"
    if "systematic review" in t or "meta-analysis" in t:
        return "Systematic review/meta-analysis"
    if "observational study" in t:
        return "Observational study"
    if "case reports" in t:
        return "Case report"
    if "review" in t:
        return "Review"
    return "Other/unclear"


def main() -> Path:
    source = RAW_DIR / "pubmed_records.jsonl"
    rows = [json.loads(line) for line in source.open(encoding="utf-8")]
    df = pd.DataFrame(rows).drop_duplicates("pmid")
    for col in ["publication_types", "mesh_terms", "authors", "query_families"]:
        df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])
    df["year"] = df["publication_date_raw"].map(extract_year)
    df["text"] = (df["title"].fillna("") + ". " + df["abstract"].fillna("")).str.strip()
    df["has_abstract"] = df["abstract"].fillna("").str.len().gt(20)
    df["evidence_level"] = df["publication_types"].map(evidence_level)
    concept_phrases = {
        "POTS": [
            "postural orthostatic tachycardia syndrome",
        ],
        "EDS": [
            "ehlers-danlos syndrome",
        ],
        "hEDS": [
            "hypermobile ehlers-danlos syndrome",
        ],
        "MCAS": [
            "mast cell activation syndrome",
        ],
    }

    for concept, phrases in concept_phrases.items():
        df[f"query_{concept}"] = df["query_families"].map(
            lambda families: concept in families
        )
        df[f"mention_{concept}"] = df["text"].map(
            lambda text: contains_any(text, phrases)
        )

    for topic, terms in TOPIC_KEYWORDS.items():
        df[f"topic_{topic}"] = df["text"].map(lambda x: contains_any(x, terms))
        
    for condition, terms in CONDITION_KEYWORDS.items():
        df[f"condition_{condition}"] = df["text"].map(
            lambda x: contains_any(x, terms)
        )

    out = PROCESSED_DIR / "papers.parquet"
    df.to_parquet(out, index=False)
    print(f"Saved {len(df):,} papers to {out}")
    return out

if __name__ == "__main__":
    main()
