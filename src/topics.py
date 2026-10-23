"""Semantic topic modelling: embeddings -> UMAP -> HDBSCAN.

BERTopic is optional here. The core output is intentionally simple and auditable:
embedding coordinates, cluster IDs and representative terms.
"""
import argparse
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
from sklearn.feature_extraction.text import TfidfVectorizer

from .config import PROCESSED_DIR


def run(model_name: str, min_cluster_size: int = 20, sample_size: int | None = None):
    path = PROCESSED_DIR / "papers.parquet"
    df = pd.read_parquet(path)
    if sample_size and len(df) > sample_size:
        work = df.sample(sample_size, random_state=42).copy()
    else:
        work = df.copy()
    texts = work["text"].fillna("").tolist()
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True, normalize_embeddings=True)
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=42)
    coords = reducer.fit_transform(embeddings)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric="euclidean", prediction_data=True)
    labels = clusterer.fit_predict(coords)
    work["cluster"] = labels
    work["umap_x"] = coords[:, 0]
    work["umap_y"] = coords[:, 1]
    out = PROCESSED_DIR / "papers_topics.parquet"
    work.to_parquet(out, index=False)
    np.save(PROCESSED_DIR / "embeddings.npy", embeddings)

    vectorizer = TfidfVectorizer(stop_words="english", min_df=3, max_df=0.95, ngram_range=(1, 2), max_features=10000)
    X = vectorizer.fit_transform(texts)
    vocab = np.array(vectorizer.get_feature_names_out())
    topic_rows = []
    for cluster in sorted(set(labels)):
        if cluster == -1:
            continue
        idx = np.where(labels == cluster)[0]
        scores = np.asarray(X[idx].mean(axis=0)).ravel()
        terms = vocab[scores.argsort()[::-1][:10]].tolist()
        topic_rows.append({"cluster": int(cluster), "papers": int(len(idx)), "representative_terms": terms})
    pd.DataFrame(topic_rows).to_json(PROCESSED_DIR / "topic_summary.json", orient="records", indent=2)
    print(f"Saved topic dataset to {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--min-cluster-size", type=int, default=20)
    parser.add_argument("--sample-size", type=int, default=None)
    args = parser.parse_args()
    run(args.model, args.min_cluster_size, args.sample_size)
