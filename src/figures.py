import pandas as pd
import plotly.express as px


def trend(df: pd.DataFrame):
    counts = df.dropna(subset=["year"]).groupby("year").size().reset_index(name="papers")
    fig = px.line(counts, x="year", y="papers", markers=True, title="PubMed publications over time")
    fig.add_vline(x=2017, line_dash="dash", annotation_text="2017 EDS classification")
    fig.add_vline(x=2020, line_dash="dash", annotation_text="2020")
    return fig


def topic_trends(df: pd.DataFrame, topic_cols: list[str]):
    rows = []
    for col in topic_cols:
        x = df.groupby("year")[col].sum().reset_index(name="papers")
        x["topic"] = col.removeprefix("topic_")
        rows.append(x)
    long = pd.concat(rows, ignore_index=True)
    return px.line(long, x="year", y="papers", color="topic", title="Curated topic signals over time")


def semantic_map(df: pd.DataFrame):
    plot = df.copy()
    plot["cluster_label"] = plot["cluster"].map(lambda x: f"Cluster {x}" if x >= 0 else "Unclustered")
    return px.scatter(
        plot,
        x="umap_x",
        y="umap_y",
        color="cluster_label",
        hover_name="title",
        hover_data={"year": True, "journal": True, "pmid": True, "umap_x": False, "umap_y": False},
        title="Semantic map of PubMed abstracts",
    )
