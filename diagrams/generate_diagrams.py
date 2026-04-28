"""Generates system diagram images for the BestMatchMusic project."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")


# ── colour palette ────────────────────────────────────────────────────────────
C_INPUT   = "#4A90D9"   # blue  – inputs
C_PROCESS = "#5BA85A"   # green – processing steps
C_OUTPUT  = "#E67E22"   # orange – output
C_TEST    = "#9B59B6"   # purple – testing / review
C_TEXT    = "#FFFFFF"
C_BG      = "#1E1E2E"
C_ARROW   = "#AAAAAA"


def box(ax, x, y, w, h, text, color, fontsize=9, radius=0.04):
    rect = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        linewidth=1.5, edgecolor="white", facecolor=color, zorder=3,
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            color=C_TEXT, fontweight="bold", zorder=4,
            multialignment="center", linespacing=1.5)


def arrow(ax, x1, y1, x2, y2):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=C_ARROW, lw=1.8),
        zorder=2,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 1 — Full data-flow
# ═══════════════════════════════════════════════════════════════════════════════
def make_dataflow():
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_aspect("equal")

    fig.suptitle(
        "BestMatchMusic — System Data Flow",
        color="white", fontsize=14, fontweight="bold", y=0.97,
    )

    # ── row 1: inputs ──────────────────────────────────────────────────────────
    box(ax, 3, 7.0, 4.2, 0.9,
        "[ USER INPUT ]\nfav_genre · fav_mood · target_energy\ntarget_tempo · target_danceability · target_acousticness",
        C_INPUT, fontsize=8)

    box(ax, 9, 7.0, 3.6, 0.9,
        "[ SONG CATALOG ]\ndata/songs.csv\n18 songs x 10 features",
        C_INPUT, fontsize=8)

    # ── row 2: load ────────────────────────────────────────────────────────────
    box(ax, 6, 5.6, 3.8, 0.75,
        "load_songs()\nParse CSV  |  cast strings -> float/int",
        C_PROCESS, fontsize=8.5)

    arrow(ax, 3, 6.55, 5.1, 5.97)
    arrow(ax, 9, 6.55, 6.9, 5.97)

    # ── row 3: score ───────────────────────────────────────────────────────────
    box(ax, 6, 4.2, 4.8, 0.9,
        "score_song()   [ runs once per song ]\nGenre +2.0  |  Mood +1.0  |  Energy +2.0\nTempo x1.5  |  Acousticness x1.0  |  Dance x0.75",
        C_PROCESS, fontsize=8)

    arrow(ax, 6, 5.22, 6, 4.65)

    # ── row 4: rank ────────────────────────────────────────────────────────────
    box(ax, 6, 2.9, 4.0, 0.75,
        "recommend_songs()\nSort all scores descending  |  return top-K",
        C_PROCESS, fontsize=8.5)

    arrow(ax, 6, 3.75, 6, 3.27)

    # ── row 5: output ──────────────────────────────────────────────────────────
    box(ax, 6, 1.75, 4.2, 0.75,
        "[ TERMINAL OUTPUT ]\nRanked songs  |  score / 8.25  |  reason string",
        C_OUTPUT, fontsize=8.5)

    arrow(ax, 6, 2.52, 6, 2.12)

    # ── row 6: evaluation forks ────────────────────────────────────────────────
    box(ax, 2.8, 0.55, 3.8, 0.75,
        "[ AUTOMATED TESTS ]\npytest  —  7 tests\ntests/test_recommender.py",
        C_TEST, fontsize=8.5)

    box(ax, 9.2, 0.55, 3.4, 0.75,
        "[ HUMAN REVIEW ]\nmodel_card.md\nspot-check quality",
        C_TEST, fontsize=8.5)

    arrow(ax, 4.5, 1.37, 3.3, 0.93)
    arrow(ax, 7.5, 1.37, 8.7, 0.93)

    # ── confidence label ───────────────────────────────────────────────────────
    ax.text(10.5, 4.2, "Score = confidence\n> 6.0  high\n< 4.0  low",
            color="#DDDDDD", fontsize=7.5, ha="center", va="center",
            bbox=dict(facecolor="#333355", edgecolor="#888888", boxstyle="round,pad=0.3"))

    plt.tight_layout()
    path = os.path.join(OUT, "data_flow.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"Saved {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — Scoring breakdown
# ═══════════════════════════════════════════════════════════════════════════════
def make_scoring():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    fig.suptitle(
        "BestMatchMusic — Scoring Algorithm Breakdown",
        color="white", fontsize=13, fontweight="bold", y=0.97,
    )

    features = [
        ("Genre Match",        "+2.00", "Exact string match — strongest signal.\nEncodes instrument palette & production style.", "#4A90D9"),
        ("Mood Match",         "+1.00", "Exact string match — secondary signal.\nMood varies widely within a genre.", "#5BA85A"),
        ("Energy Match",       "+2.00", "Within ±0.15 of target — categorical threshold.\nCaptures overall intensity feel.", "#E67E22"),
        ("Tempo Proximity",    "×1.50", "BPM normalized 0–1 before comparing.\nTop personal priority: how fast-paced.", "#9B59B6"),
        ("Acousticness Prox.", "×1.00", "Organic vs electronic production feel.\nProxy for 'instrumental similarity'.", "#E74C3C"),
        ("Danceability Prox.", "×0.75", "Beat regularity and rhythmic tightness.\nLowest weight — least dominant signal.", "#1ABC9C"),
    ]

    y_positions = [5.1, 4.3, 3.5, 2.7, 1.9, 1.1]

    for (name, pts, desc, color), y in zip(features, y_positions):
        # colour swatch
        swatch = FancyBboxPatch((0.2, y - 0.28), 0.5, 0.56,
                                boxstyle="round,pad=0.02",
                                facecolor=color, edgecolor="white", lw=1, zorder=3)
        ax.add_patch(swatch)
        ax.text(0.45, y, pts, ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", zorder=4)

        ax.text(0.9, y + 0.12, name, ha="left", va="center",
                fontsize=9.5, fontweight="bold", color="white")
        ax.text(0.9, y - 0.15, desc, ha="left", va="center",
                fontsize=7.8, color="#CCCCCC", linespacing=1.3)

        # bar showing relative weight
        weights = {"Genre Match": 2.0, "Mood Match": 1.0, "Energy Match": 2.0,
                   "Tempo Proximity": 1.5, "Acousticness Prox.": 1.0, "Danceability Prox.": 0.75}
        bar_w = weights[name] / 2.0 * 2.8
        bar = FancyBboxPatch((7.0, y - 0.18), bar_w, 0.36,
                             boxstyle="round,pad=0.01",
                             facecolor=color, edgecolor="none", alpha=0.7, zorder=3)
        ax.add_patch(bar)
        ax.text(7.0 + bar_w + 0.1, y, f"{weights[name]:.2f}", ha="left", va="center",
                fontsize=8.5, color="white", fontweight="bold")

    ax.text(8.5, 0.45, "Max total: 8.25",
            ha="center", va="center", fontsize=10, fontweight="bold", color="#FFD700",
            bbox=dict(facecolor="#333300", edgecolor="#FFD700", boxstyle="round,pad=0.3"))

    ax.text(7.0, 5.65, "Weight →", ha="left", va="center",
            fontsize=8, color="#AAAAAA")

    plt.tight_layout()
    path = os.path.join(OUT, "scoring_breakdown.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print(f"Saved {path}")


if __name__ == "__main__":
    make_dataflow()
    make_scoring()
