"""
sna_visualize.py -- Publication figures for the EO 14405 conflict-of-interest graph.

Two outputs:

  figures/sna_full.png + .pdf
      Full graph, ~150 nodes. Nodes sized by eigenvector centrality, colored
      by Louvain community (heritage palette). Edges colored by kind.

  figures/sna_nexus.png + .pdf
      Induced subgraph on the Trump-Fed-Stablecoin "conflict-of-interest
      spine". Hand-picked seed set; one-hop expansion within the seed kinds.

Both figures sit on the Parchment background defined in src/style.py and use
the heritage palette: Carolina Navy, Carolina Blue, Old Gold, BSE Teal,
Indiana Crimson, Slate.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import networkx as nx
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sna import (build_graph, compute_centrality, NODES, EDGES, FIG_DIR)
from style import (apply_defaults,
                   CAROLINA_NAVY, CAROLINA_BLUE, OLD_GOLD,
                   BSE_TEAL, INDIANA_CRIMSON, PARCHMENT,
                   SLATE, MIST)

apply_defaults()

# --------------------------------------------------------------------------
# Color schemes
# --------------------------------------------------------------------------

# Six-community palette for the full graph (top 6 by size are
# colored heritage; smaller communities collapse to SLATE).
# Order is BY RANK (largest community first). Labels in fig_full() must match.
COMMUNITY_PALETTE = [
    CAROLINA_NAVY,    # rank 1: Trump-WLFI + admin core
    OLD_GOLD,         # rank 2: Fairshake / a16z / industry-Congress
    INDIANA_CRIMSON,  # rank 3: Fed Board + Custodia + skeptics
    CAROLINA_BLUE,    # rank 4: BlackRock-Circle-BNY-Goldman
    BSE_TEAL,         # rank 5: Custodian nexus
    "#6a5acd",        # rank 6: Tether-Cantor-Lutnick
]

# Edge kind colors
EDGE_KIND_COLOR = {
    "employment":      SLATE,
    "family":          INDIANA_CRIMSON,
    "kinship":         INDIANA_CRIMSON,
    "board":           CAROLINA_NAVY,
    "donation":        OLD_GOLD,
    "investment":      OLD_GOLD,
    "ownership":       CAROLINA_NAVY,
    "custody":         BSE_TEAL,
    "regulator":       BSE_TEAL,
    "revolving_door":  INDIANA_CRIMSON,
    "policy_authority": CAROLINA_BLUE,
    "litigation":      INDIANA_CRIMSON,
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def to_undirected(G: nx.MultiDiGraph) -> nx.Graph:
    UG = nx.Graph()
    for u, v, data in G.edges(data=True):
        w = float(data.get("weight", 1.0))
        if UG.has_edge(u, v):
            UG[u][v]["weight"] += w
            UG[u][v]["kinds"].add(data.get("kind", ""))
        else:
            UG.add_edge(u, v, weight=w,
                        kinds={data.get("kind", "")},
                        primary_kind=data.get("kind", "employment"))
    for n in G.nodes:
        if n not in UG:
            UG.add_node(n)
    return UG


def community_colors(communities: list[set[str]]) -> dict[str, str]:
    """
    Six top communities get heritage colors. Remaining communities all map
    to SLATE so the figure stays readable.
    """
    # Sort communities by size descending
    sorted_comms = sorted(enumerate(communities), key=lambda kc: -len(kc[1]))
    color_for_comm = {}
    for rank, (orig_id, comm) in enumerate(sorted_comms):
        color = COMMUNITY_PALETTE[rank] if rank < len(COMMUNITY_PALETTE) else SLATE
        color_for_comm[orig_id] = color
    node_color = {}
    for orig_id, comm in enumerate(communities):
        c = color_for_comm[orig_id]
        for node in comm:
            node_color[node] = c
    return node_color


def node_sizes(eig: dict[str, float], priority: dict[str, str],
               base=80.0, scale=1900.0) -> dict[str, float]:
    """Size = (priority floor) + scale * eigenvector centrality."""
    floor = {"high": 200, "medium": 110, "low": 70}
    return {n: floor.get(priority.get(n, "low"), 70) + scale * eig.get(n, 0.0)
            for n in eig}


def edge_color_for(data: dict) -> str:
    kind = data.get("primary_kind") or next(iter(data.get("kinds", [""])))
    return EDGE_KIND_COLOR.get(kind, SLATE)


# --------------------------------------------------------------------------
# Figure 1: full SNA graph
# --------------------------------------------------------------------------


def fig_full(G: nx.MultiDiGraph, out: dict, save=True):
    UG = to_undirected(G)
    eig = {row["node"]: row["value"] for row in out["eigenvector"]}
    priority = {n.name: n.priority for n in NODES}
    communities_list = [set(c["members"]) for c in out["communities"]]
    node_color = community_colors(communities_list)
    sizes = node_sizes(eig, priority)

    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_facecolor(PARCHMENT)
    fig.patch.set_facecolor(PARCHMENT)

    # Layout: spring with eigenvector-weighted pull, fixed seed for reproducibility
    pos = nx.spring_layout(UG, k=0.55, iterations=180, seed=14405,
                           weight="weight")

    # Edges: bundle by kind for cleaner legend
    for u, v, data in UG.edges(data=True):
        color = edge_color_for(data)
        # Find the primary kind among the kinds set
        kinds = data.get("kinds", set())
        # Pick the highest-precedence kind for color
        precedence = ["ownership", "family", "kinship", "board", "donation",
                      "investment", "custody", "regulator", "revolving_door",
                      "policy_authority", "litigation", "employment"]
        kind = next((k for k in precedence if k in kinds), "employment")
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                color=EDGE_KIND_COLOR.get(kind, SLATE),
                alpha=0.32, linewidth=0.7 * data.get("weight", 1.0),
                zorder=1)

    # Nodes
    xs = np.array([pos[n][0] for n in UG.nodes])
    ys = np.array([pos[n][1] for n in UG.nodes])
    cs = [node_color.get(n, SLATE) for n in UG.nodes]
    ss = [sizes.get(n, 70) for n in UG.nodes]
    ax.scatter(xs, ys, s=ss, c=cs, alpha=0.92,
               edgecolors=CAROLINA_NAVY, linewidths=0.6, zorder=2)

    # Labels: top 28 by eigenvector + the 8 highest-priority
    top_for_label = {row["node"] for row in out["eigenvector"][:28]}
    top_for_label.update({n.name for n in NODES if n.priority == "high"})
    # Also always label EO 14405 and the institutional pivots
    must_label = {"EO 14405", "Federal Reserve Board", "Kansas City Fed",
                  "Senate Banking Committee", "House Financial Services Committee"}
    top_for_label.update(must_label)

    for node in UG.nodes:
        if node in top_for_label:
            x, y = pos[node]
            ax.text(x, y + 0.025, node, fontsize=7.4, ha="center", va="bottom",
                    color=CAROLINA_NAVY, zorder=3,
                    bbox=dict(facecolor=PARCHMENT, edgecolor="none",
                              alpha=0.78, pad=0.5))

    ax.set_axis_off()

    # Title and subtitle
    ax.set_title(
        "EO 14405 conflict-of-interest network\n"
        "Nodes sized by eigenvector centrality, colored by Louvain community",
        fontsize=14, color=CAROLINA_NAVY, loc="left", pad=14)

    # Legends
    sorted_comms = sorted(enumerate(communities_list), key=lambda kc: -len(kc[1]))
    community_labels = [
        "Trump-WLFI + admin core",
        "Fairshake / a16z / industry-Congress",
        "Fed Board + Custodia + skeptics",
        "BlackRock-Circle-BNY-Goldman",
        "Custodian nexus (Anchorage, BitGo, Brooks)",
        "Tether-Cantor-Lutnick",
    ]
    com_handles = []
    for rank, (orig_id, comm) in enumerate(sorted_comms[:6]):
        color = COMMUNITY_PALETTE[rank]
        label = community_labels[rank] if rank < len(community_labels) else f"Community {orig_id}"
        com_handles.append(mpatches.Patch(
            color=color, label=f"{label} (n={len(comm)})"))

    leg1 = ax.legend(handles=com_handles, loc="lower left",
                     bbox_to_anchor=(0.0, 0.0), fontsize=8.5, frameon=True,
                     framealpha=0.85, facecolor=PARCHMENT, edgecolor=MIST,
                     title="Communities", title_fontsize=9)
    leg1.get_title().set_color(CAROLINA_NAVY)
    ax.add_artist(leg1)

    edge_handles = []
    edge_kinds_legend = [
        ("ownership / board", CAROLINA_NAVY),
        ("donation / investment", OLD_GOLD),
        ("custody / regulator", BSE_TEAL),
        ("family / kinship / litigation", INDIANA_CRIMSON),
        ("policy authority", CAROLINA_BLUE),
        ("employment", SLATE),
    ]
    for label, color in edge_kinds_legend:
        edge_handles.append(mlines.Line2D([], [], color=color, linewidth=2,
                                          label=label, alpha=0.85))
    leg2 = ax.legend(handles=edge_handles, loc="lower right",
                     bbox_to_anchor=(1.0, 0.0), fontsize=8.5, frameon=True,
                     framealpha=0.85, facecolor=PARCHMENT, edgecolor=MIST,
                     title="Edge kind", title_fontsize=9)
    leg2.get_title().set_color(CAROLINA_NAVY)

    # Caption / source note
    fig.text(0.02, 0.013,
             "Source: hand-encoded from the eleven dossiers in dossiers/. "
             "Centrality computed on the undirected projection; communities by "
             "Louvain (seed 14405, weighted). Labels on top 28 by eigenvector "
             "centrality plus high-priority nodes.",
             fontsize=7.5, color=SLATE)

    if save:
        png = FIG_DIR / "sna_full.png"
        pdf = FIG_DIR / "sna_full.pdf"
        fig.savefig(png, dpi=300, bbox_inches="tight",
                    facecolor=PARCHMENT)
        fig.savefig(pdf, bbox_inches="tight", facecolor=PARCHMENT)
        print(f"  saved {png}")
        print(f"  saved {pdf}")
    return fig


# --------------------------------------------------------------------------
# Figure 2: Trump-Fed-Stablecoin nexus subgraph
# --------------------------------------------------------------------------


# Seed set: the spine. Trump family, Fed Board + KC Fed, key stablecoin issuers
# + custodians, plus the cabinet-level conflict pivots.
NEXUS_SEEDS = {
    # Trump family + WLFI
    "Donald Trump", "Donald Trump Jr.", "Eric Trump",
    "DT Marks DEFI LLC", "World Liberty Financial", "USD1",
    "Trump Media (DJT)", "American Bitcoin (ABTC)",
    "BitGo Trust", "BitGo",
    # Cabinet pivots
    "Howard Lutnick", "Brandon Lutnick", "Cantor Fitzgerald",
    "Scott Bessent", "Treasury", "Kevin Hassett",
    "Stephen Miran", "David Sacks",
    "William Pulte", "Paul Atkins", "Brian Quintenz",
    # Tether stack
    "Tether (USDT)", "iFinex", "USAT", "Anchorage Digital",
    "Twenty One Capital",
    # Circle stack
    "Circle Internet Group", "USDC", "Heath Tarbert",
    "BlackRock", "BNY Mellon",
    # Fed (decision authority)
    "Federal Reserve Board", "Kansas City Fed",
    "Kevin Warsh", "Christopher Waller", "Michelle Bowman",
    "Stephen Miran", "Jeffrey Schmid", "Kraken Financial",
    # The EO itself
    "EO 14405",
}


def induced_nexus_subgraph(G: nx.MultiDiGraph) -> nx.MultiDiGraph:
    nodes = [n for n in G.nodes if n in NEXUS_SEEDS]
    return G.subgraph(nodes).copy()


def fig_nexus(G: nx.MultiDiGraph, out: dict, save=True):
    sub = induced_nexus_subgraph(G)
    USub = to_undirected(sub)
    eig_all = {row["node"]: row["value"] for row in out["eigenvector"]}
    priority = {n.name: n.priority for n in NODES}

    # Recolor by functional role rather than Louvain on the subgraph:
    # Carolina Navy   = primary structural (EO, Fed Board)
    # Indiana Crimson = highest-risk individuals (Warsh, Schmid, Trump,
    #                   Lutnick, Hassett, Pulte, etc.)
    # Old Gold        = individuals with documented financial conflicts
    # BSE Teal        = regulators / Fed officials without direct conflict
    # Carolina Blue   = firms and institutions
    # Parchment / Slate = supporting actors
    high_risk = {
        "Donald Trump", "Kevin Warsh", "Jeffrey Schmid",
        "Howard Lutnick", "Brandon Lutnick", "Kevin Hassett",
        "William Pulte", "Stephen Miran", "Brian Quintenz",
        "Heath Tarbert", "David Sacks",
    }
    documented_conflict = {
        "Donald Trump Jr.", "Eric Trump", "Scott Bessent",
        "Paul Atkins", "Christopher Waller", "Michelle Bowman",
    }
    regulators = {
        "Federal Reserve Board", "Kansas City Fed", "Treasury",
    }
    firms = {
        "World Liberty Financial", "USD1", "DT Marks DEFI LLC",
        "Trump Media (DJT)", "American Bitcoin (ABTC)",
        "BitGo Trust", "BitGo", "Cantor Fitzgerald",
        "Tether (USDT)", "iFinex", "USAT", "Anchorage Digital",
        "Circle Internet Group", "USDC", "BlackRock", "BNY Mellon",
        "Twenty One Capital", "Kraken Financial",
    }

    def color_for(node):
        if node == "EO 14405":
            return CAROLINA_NAVY
        if node in high_risk:
            return INDIANA_CRIMSON
        if node in documented_conflict:
            return OLD_GOLD
        if node in regulators:
            return BSE_TEAL
        if node in firms:
            return CAROLINA_BLUE
        return SLATE

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_facecolor(PARCHMENT)
    fig.patch.set_facecolor(PARCHMENT)

    # Layout: kamada-kawai gives cleaner small-graph structure
    pos = nx.kamada_kawai_layout(USub, weight="weight")

    # Edges
    for u, v, data in USub.edges(data=True):
        kinds = data.get("kinds", set())
        precedence = ["ownership", "family", "kinship", "board", "donation",
                      "investment", "custody", "regulator", "revolving_door",
                      "policy_authority", "litigation", "employment"]
        kind = next((k for k in precedence if k in kinds), "employment")
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                color=EDGE_KIND_COLOR.get(kind, SLATE),
                alpha=0.55, linewidth=1.0 + 0.5 * data.get("weight", 1.0),
                zorder=1)

    # Nodes
    xs = np.array([pos[n][0] for n in USub.nodes])
    ys = np.array([pos[n][1] for n in USub.nodes])
    cs = [color_for(n) for n in USub.nodes]
    sizes = {n: 250 + 2400 * eig_all.get(n, 0.05) for n in USub.nodes}
    # Hard-boost EO 14405 visually
    if "EO 14405" in sizes:
        sizes["EO 14405"] = max(sizes["EO 14405"], 1400)
    ss = [sizes[n] for n in USub.nodes]
    ax.scatter(xs, ys, s=ss, c=cs, alpha=0.92,
               edgecolors=CAROLINA_NAVY, linewidths=0.9, zorder=2)

    # Labels for ALL nodes (this is a small subgraph, every node matters)
    for node in USub.nodes:
        x, y = pos[node]
        ax.text(x, y + 0.045, node, fontsize=8.2, ha="center", va="bottom",
                color=CAROLINA_NAVY,
                fontweight="bold" if node in high_risk or node == "EO 14405"
                else "normal",
                zorder=3,
                bbox=dict(facecolor=PARCHMENT, edgecolor="none",
                          alpha=0.85, pad=1.0))

    ax.set_axis_off()
    ax.set_title(
        "Trump-Fed-Stablecoin spine\n"
        "Induced subgraph of the conflict-of-interest perimeter "
        "documented in dossiers/",
        fontsize=14, color=CAROLINA_NAVY, loc="left", pad=14)

    role_handles = [
        mpatches.Patch(color=CAROLINA_NAVY, label="EO 14405 / primary"),
        mpatches.Patch(color=INDIANA_CRIMSON, label="Highest-risk individual"),
        mpatches.Patch(color=OLD_GOLD, label="Documented financial conflict"),
        mpatches.Patch(color=BSE_TEAL, label="Regulator / institution"),
        mpatches.Patch(color=CAROLINA_BLUE, label="Firm / stablecoin / custodian"),
        mpatches.Patch(color=SLATE, label="Supporting actor"),
    ]
    leg1 = ax.legend(handles=role_handles, loc="lower left",
                     bbox_to_anchor=(0.0, 0.0), fontsize=9, frameon=True,
                     framealpha=0.9, facecolor=PARCHMENT, edgecolor=MIST,
                     title="Role coloring", title_fontsize=9.5)
    leg1.get_title().set_color(CAROLINA_NAVY)
    ax.add_artist(leg1)

    edge_handles = []
    for label, color in [
        ("ownership / board", CAROLINA_NAVY),
        ("donation / investment", OLD_GOLD),
        ("custody / regulator", BSE_TEAL),
        ("family / kinship", INDIANA_CRIMSON),
        ("policy authority", CAROLINA_BLUE),
        ("employment", SLATE),
    ]:
        edge_handles.append(mlines.Line2D([], [], color=color, linewidth=2,
                                          label=label, alpha=0.85))
    leg2 = ax.legend(handles=edge_handles, loc="lower right",
                     bbox_to_anchor=(1.0, 0.0), fontsize=9, frameon=True,
                     framealpha=0.9, facecolor=PARCHMENT, edgecolor=MIST,
                     title="Edge kind", title_fontsize=9.5)
    leg2.get_title().set_color(CAROLINA_NAVY)

    fig.text(0.02, 0.013,
             "Subgraph induced on Trump-family entities, Fed Board, Reserve "
             "Banks, named stablecoin issuers, and the cabinet pivots that "
             "connect them. Layout: Kamada-Kawai (weighted). Source: dossiers/.",
             fontsize=7.5, color=SLATE)

    if save:
        png = FIG_DIR / "sna_nexus.png"
        pdf = FIG_DIR / "sna_nexus.pdf"
        fig.savefig(png, dpi=300, bbox_inches="tight",
                    facecolor=PARCHMENT)
        fig.savefig(pdf, bbox_inches="tight", facecolor=PARCHMENT)
        print(f"  saved {png}")
        print(f"  saved {pdf}")
    return fig


# --------------------------------------------------------------------------


def main():
    G = build_graph()
    out = compute_centrality(G)
    fig_full(G, out)
    fig_nexus(G, out)


if __name__ == "__main__":
    main()
