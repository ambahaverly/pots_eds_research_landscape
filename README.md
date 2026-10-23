# Mapping the POTS & EDS Research Landscape

A reproducible PubMed literature-mining project exploring **what research on postural orthostatic tachycardia syndrome (POTS), Ehlers-Danlos syndromes (EDS), hypermobile EDS (hEDS), and related conditions covers — and where the evidence appears thinner**.

## Why this project?

POTS and EDS/hEDS are clinically overlapping topics with rapidly changing research attention. This project asks:

1. How has publication volume changed over time?
2. Which research themes dominate the literature?
3. Where do POTS, hEDS/EDS and MCAS overlap, and where are they studied separately?
4. What types of evidence dominate — e.g. reviews, observational studies, RCTs, case reports?
5. Which topics appear comparatively under-represented?

> **Important:** This is a bibliometric/literature overview, not medical advice. Publication counts do not measure clinical importance, quality, or effectiveness. Search terms, PubMed indexing, missing abstracts and publication-type tagging can all bias the results.

## Architecture

```text
PubMed E-utilities
       |
       v
  01_collect.py  ----> data/raw/pubmed_records.jsonl
       |
       v
  02_prepare.py  ----> data/processed/papers.parquet
       |
       +------------------------+
       |                        |
       v                        v
03_topics.py              04_analysis.py
       |                        |
       +------------+-----------+
                    v
          data/processed/*.parquet
                    |
                    v
              app.py (Streamlit)
```

## Project structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── config.py
│   ├── pubmed.py
│   ├── prepare.py
│   ├── topics.py
│   ├── analysis.py
│   └── figures.py
├── data/
│   ├── raw/
│   └── processed/
├── tests/
└── docs/
    └── findings_template.md
```

## Quickstart

### 1. Create an environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set your PubMed contact details

NCBI asks automated users to identify themselves. Set:

```bash
export NCBI_EMAIL="your.email@example.com"
# Optional:
export NCBI_API_KEY="..."
```

### 3. Collect PubMed records

```bash
python -m src.pubmed --years 1990 2026 --max-records 20000
```

The collector uses separate concept queries and preserves the query label, allowing overlap analysis without silently collapsing POTS and EDS into one search.

### 4. Prepare the analytical dataset

```bash
python -m src.prepare
```

### 5. Create topic embeddings/clusters

```bash
python -m src.topics --model sentence-transformers/all-MiniLM-L6-v2
```

For a stronger biomedical model, substitute a PubMedBERT/SapBERT-compatible sentence-transformers model available in your environment. The code keeps the model configurable rather than hard-coding a heavyweight download.

### 6. Run the dashboard

```bash
streamlit run app.py
```

## Search strategy

The default concept families are intentionally explicit:

- **POTS:** `"postural orthostatic tachycardia syndrome" OR POTS[Title/Abstract]`
- **EDS:** `"Ehlers-Danlos syndrome" OR Ehlers-Danlos[Title/Abstract]`
- **hEDS:** `"hypermobile Ehlers-Danlos syndrome" OR hEDS[Title/Abstract]`
- **MCAS:** `"mast cell activation syndrome" OR MCAS[Title/Abstract]`

The project stores the originating query family and also derives concept flags from title/abstract/MeSH content. This makes it possible to distinguish **retrieval overlap** from **semantic co-mention**.

### Important search-design decision

Do **not** interpret a search result count as the number of all papers “about” a disease. PubMed indexing and terminology evolve, and abbreviations can introduce false positives. The report should always state the exact query strings and date range used.

## Topic modelling

The project uses two complementary layers:

1. **Interpretable feature layer:** MeSH terms, publication types, controlled keywords and curated concept dictionaries.
2. **Semantic layer:** sentence embeddings + UMAP + HDBSCAN. BERTopic can be added on top when installed.

This gives you a defensible explanation of a cluster rather than relying only on an automatically generated topic name.

## Evidence-level classification

The dashboard groups PubMed publication types into a simple descriptive hierarchy:

- Randomized controlled trial
- Controlled/clinical trial
- Observational study
- Systematic review/meta-analysis
- Narrative review
- Case report
- Other/unclear

This is **not** a formal risk-of-bias or evidence-quality assessment. A publication type is not enough to determine methodological quality.

## Suggested research questions for the final report

### Trend breakpoints

Compare publication trajectories around:

- **2017:** the revised International Classification of the Ehlers-Danlos Syndromes.
- **2020 onward:** increased attention to POTS/autonomic dysfunction in the broader post-COVID research landscape.

These are hypotheses for temporal interpretation, not causal claims.

### Potential gap metrics

A “gap” should never mean “few papers = clinically unimportant.” Instead, use several descriptive measures:

- publication count by topic/year;
- share of papers containing multiple concepts;
- share of intervention studies;
- share of RCTs;
- topic growth rate;
- proportion of papers with abstracts;
- persistence of topics over time.

## Reproducibility checklist

Before publishing a LinkedIn result, record:

- extraction date;
- exact PubMed query strings;
- date limits;
- number of records retrieved;
- deduplication rules;
- embedding model/version;
- UMAP/HDBSCAN parameters;
- cluster labelling process;
- excluded records;
- limitations.

## LinkedIn hook

A strong final post can start with the finding rather than the tooling:

> **I analyzed thousands of PubMed papers on POTS and EDS to ask a simple question: what is the research actually studying — and what is it barely studying at all?**
>
> I built a reproducible literature-mining pipeline using PubMed, embeddings and interactive visualisation, then mapped the research landscape across autonomic dysfunction, genetics, pain, GI symptoms, treatment and related conditions.

Replace “thousands” and every substantive finding with the actual refreshed dataset results.
