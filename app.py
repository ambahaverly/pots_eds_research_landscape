from pathlib import Path

import pandas as pd
import streamlit as st

from src.analysis import concept_overlap, evidence_summary
from src.figures import semantic_map, topic_trends, trend
from src.config import TOPIC_KEYWORDS
from src.network import topic_network
import numpy as np

st.set_page_config(page_title="POTS & EDS Research Landscape", page_icon="🧬", layout="wide")

st.title("🧬 Mapping the POTS & EDS Research Landscape")
st.caption("A PubMed-based literature-mining dashboard — descriptive research overview, not medical advice.")

path_topics = Path("data/processed/papers_topics.parquet")
path_basic = Path("data/processed/papers.parquet")
if path_topics.exists():
    df = pd.read_parquet(path_topics)
elif path_basic.exists():
    df = pd.read_parquet(path_basic)
else:
    st.error("No processed dataset found. Run `python -m src.pubmed`, then `python -m src.prepare`.")
    st.stop()

st.sidebar.header("Filters")
years = st.sidebar.slider("Publication year", int(df.year.min()), int(df.year.max()), (int(df.year.min()), int(df.year.max())))
concepts = st.sidebar.multiselect("Concepts", ["POTS", "EDS", "hEDS", "MCAS"])
evidence = st.sidebar.multiselect("Evidence type", sorted(df.evidence_level.dropna().unique()))

view = df[df.year.between(*years)].copy()
for concept in concepts:
    view = view[view[f"concept_{concept}"]]
if evidence:
    view = view[view.evidence_level.isin(evidence)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Papers", f"{len(view):,}")
c2.metric("With abstracts", f"{view.has_abstract.mean() * 100:.1f}%")
c3.metric("Journals", f"{view.journal.nunique():,}")
c4.metric("Years", f"{view.year.min():.0f}–{view.year.max():.0f}")

st.subheader("1. Publication volume")
st.plotly_chart(trend(view), use_container_width=True)

st.subheader("2. What is the literature about?")
topic_cols = [f"topic_{k}" for k in TOPIC_KEYWORDS if f"topic_{k}" in view.columns]
st.plotly_chart(topic_trends(view, topic_cols), use_container_width=True)

if "cluster" in view.columns:
    st.subheader("3. Semantic map")
    st.plotly_chart(semantic_map(view), use_container_width=True)
    st.caption("Clusters are computational groupings of abstract text, not clinical categories. Review representative papers before assigning a human-readable label.")

st.subheader("4. POTS / EDS / hEDS / MCAS overlap")
st.dataframe(concept_overlap(view), use_container_width=True, hide_index=True)

st.subheader("5. Theme co-occurrence")
st.plotly_chart(topic_network(view, topic_cols), use_container_width=True)
st.caption("Edges represent papers whose abstracts match both curated theme dictionaries; this is a descriptive signal, not a causal or clinical relationship.")

st.subheader("6. Evidence profile")
import plotly.express as px
st.plotly_chart(px.bar(evidence_summary(view), x="evidence_level", y="papers", title="Publication types / study-design signals"), use_container_width=True)

st.subheader("7. Explore papers")
search_mode = st.radio("Search mode", ["Keyword", "Semantic"], horizontal=True)
search = st.text_input("Search title or abstract", placeholder="e.g. exercise intolerance")
results = view
if search and search_mode == "Keyword":
    mask = results["text"].str.contains(search, case=False, na=False)
    results = results[mask]
elif search and search_mode == "Semantic":
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        @st.cache_resource
        def load_search_model():
            return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        model = load_search_model()
        query_vec = model.encode([search], normalize_embeddings=True)
        paper_vec = model.encode(results["text"].fillna("").tolist(), batch_size=32, normalize_embeddings=True, show_progress_bar=False)
        scores = cosine_similarity(query_vec, paper_vec)[0]
        results = results.copy()
        results["semantic_score"] = scores
        results = results.sort_values("semantic_score", ascending=False)
    except Exception as exc:
        st.warning(f"Semantic search unavailable; falling back to keyword search ({exc}).")
        results = results[results["text"].str.contains(search, case=False, na=False)]
display_cols = [c for c in ["pmid", "year", "title", "journal", "evidence_level", "semantic_score"] if c in results.columns]
st.dataframe(results[display_cols].sort_values("year", ascending=False).head(100), use_container_width=True, hide_index=True)

st.divider()
st.markdown("**Interpretation caution:** low publication volume can reflect terminology, indexing, funding patterns, study feasibility, or search design. It does not by itself establish that a clinical area is neglected or unimportant.")
