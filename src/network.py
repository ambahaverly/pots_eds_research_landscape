"""Build an interpretable topic co-occurrence network from curated abstract signals."""
import itertools
import pandas as pd
import networkx as nx
import plotly.graph_objects as go


def topic_network(df: pd.DataFrame, topic_cols: list[str], min_weight: int = 5):
    labels = [c.removeprefix("topic_") for c in topic_cols]
    G = nx.Graph()
    for label in labels:
        G.add_node(label, weight=int(df[f"topic_{label}"].sum()))
    for a, b in itertools.combinations(labels, 2):
        weight = int((df[f"topic_{a}"] & df[f"topic_{b}"]).sum())
        if weight >= min_weight:
            G.add_edge(a, b, weight=weight)
    if not G.edges:
        return go.Figure().update_layout(title="No topic co-occurrences above the threshold")
    pos = nx.spring_layout(G, seed=42, weight="weight")
    edge_x, edge_y = [], []
    for a, b in G.edges:
        x0, y0 = pos[a]
        x1, y1 = pos[b]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", hoverinfo="none"))
    node_x = [pos[n][0] for n in G.nodes]
    node_y = [pos[n][1] for n in G.nodes]
    node_sizes = [8 + min(35, G.nodes[n]["weight"] ** 0.5) for n in G.nodes]
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers+text", text=list(G.nodes), textposition="top center",
        marker={"size": node_sizes},
        hovertemplate="%{text}<extra></extra>",
    ))
    fig.update_layout(title="Co-occurrence network of curated research themes", showlegend=False, xaxis_visible=False, yaxis_visible=False)
    return fig
