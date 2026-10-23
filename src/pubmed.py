"""Download PubMed metadata via NCBI E-utilities using Biopython Entrez."""
import argparse
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from Bio import Entrez, Medline

from .config import (
    BATCH_SIZE, CONCEPT_QUERIES, DEFAULT_END_YEAR, DEFAULT_MAX_RECORDS,
    DEFAULT_START_YEAR, NCBI_API_KEY, NCBI_EMAIL, NCBI_TOOL, RAW_DIR,
)


def configure_entrez() -> None:
    if not NCBI_EMAIL:
        raise SystemExit("Set NCBI_EMAIL before collecting PubMed records.")
    Entrez.email = NCBI_EMAIL
    Entrez.tool = NCBI_TOOL
    if NCBI_API_KEY:
        Entrez.api_key = NCBI_API_KEY


def year_query(base_query: str, start_year: int, end_year: int) -> str:
    return f"{base_query} AND ({start_year}[Date - Publication] : {end_year}[Date - Publication])"


def search_ids(query: str, max_records: int) -> list[str]:
    with Entrez.esearch(db="pubmed", term=query, retmax=max_records, retmode="xml", usehistory="n") as handle:
        result = Entrez.read(handle)
    return list(result["IdList"])


def parse_records(xml_handle, query_label: str) -> Iterable[dict]:
    for record in Medline.parse(xml_handle):
        title = record.get("TI", "")
        abstract = record.get("AB", "")
        pubtypes = record.get("PT", [])
        mesh = record.get("MH", [])
        dates = record.get("DP", "")
        # GeneReviews/book chapters can retain the series year in DP
        # (e.g. "1993") even when the current chapter was published much later.
        # Prefer the publisher/publication-history date when available.
        if record.get("CTDT"):
            dates = str(record["CTDT"][0])
        elif record.get("EDAT"):
            dates = str(record["EDAT"]).split()[0]
        authors = record.get("AU", [])
        journal = record.get("JT", "")
        pmid = str(record.get("PMID", ""))
        doi = ""
        for aid in record.get("AID", []):
            if "[doi]" in aid.lower():
                doi = aid.split(" ")[0]
                break
        yield {
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "publication_types": pubtypes if isinstance(pubtypes, list) else [pubtypes],
            "mesh_terms": mesh if isinstance(mesh, list) else [mesh],
            "publication_date_raw": dates,
            "authors": authors if isinstance(authors, list) else [authors],
            "journal": journal,
            "doi": doi,
            "query_family": query_label,
            "retrieved_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        }


def fetch_ids(ids: list[str], query_label: str) -> list[dict]:
    rows: list[dict] = []
    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i : i + BATCH_SIZE]
        with Entrez.efetch(db="pubmed", id=batch, rettype="medline", retmode="text") as handle:
            rows.extend(parse_records(handle, query_label))
        time.sleep(0.11 if NCBI_API_KEY else 0.35)
    return rows


def collect(start_year: int, end_year: int, max_records: int) -> Path:
    configure_entrez()
    out = RAW_DIR / "pubmed_records.jsonl"
    all_rows: list[dict] = []
    for label, base_query in CONCEPT_QUERIES.items():
        query = year_query(base_query, start_year, end_year)
        ids = search_ids(query, max_records)
        print(f"{label}: {len(ids):,} IDs")
        all_rows.extend(fetch_ids(ids, label))
    # Keep all query memberships but de-duplicate records by PMID for the canonical table.
    merged: dict[str, dict] = {}
    memberships: dict[str, set[str]] = {}
    for row in all_rows:
        pmid = row["pmid"]
        if not pmid:
            continue
        merged.setdefault(pmid, row)
        memberships.setdefault(pmid, set()).add(row["query_family"])
    with out.open("w", encoding="utf-8") as f:
        for pmid, row in merged.items():
            row["query_families"] = sorted(memberships[pmid])
            row.pop("query_family", None)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Saved {len(merged):,} unique records to {out}")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs=2, type=int, default=[DEFAULT_START_YEAR, DEFAULT_END_YEAR])
    parser.add_argument("--max-records", type=int, default=DEFAULT_MAX_RECORDS)
    args = parser.parse_args()
    collect(args.years[0], args.years[1], args.max_records)
