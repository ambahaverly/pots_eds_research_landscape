# Findings: Mapping the POTS & EDS Research Landscape

## Dataset

- Extraction date: YYYY-MM-DD
- PubMed records retrieved: N
- Unique PMIDs after deduplication: N
- Publication years: YYYY–YYYY
- Search families: POTS, EDS, hEDS, MCAS
- Embedding model: MODEL + VERSION
- Clustering: UMAP parameters + HDBSCAN parameters

## Finding 1 — publication volume

Describe the trajectory. Treat 2017 and 2020 as interpretive landmarks, not causal intervention points.

## Finding 2 — dominant themes

Rank the largest semantic clusters and verify them manually using representative abstracts.

## Finding 3 — overlap

Report POTS/EDS/hEDS/MCAS co-occurrence using both retrieval membership and text-derived concept flags.

## Finding 4 — evidence profile

Report descriptive proportions of RCTs, clinical trials, observational studies, reviews and case reports.

## Potential gaps

Frame these as **research under-representation signals**, not proof of clinical neglect.

Possible metrics:

- low absolute publication volume;
- low recent growth;
- few intervention studies;
- few randomized trials;
- low cross-condition overlap;
- themes present mainly in case reports rather than comparative studies.

## Limitations

1. PubMed is not the entire biomedical literature.
2. Search terms can miss synonyms and create false positives.
3. PubMed indexing and publication-type assignment vary over time.
4. Abstract-only analysis misses information in full text.
5. Publication count is not a measure of evidence quality or clinical importance.
6. Embedding clusters depend on model and hyperparameters.
7. Country inference is not included in the starter pipeline because author-affiliation parsing is noisy; add it only after validation.
