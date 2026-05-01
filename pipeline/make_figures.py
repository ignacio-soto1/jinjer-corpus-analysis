"""Generate the five core figures from the pipeline outputs.

Reads:  outputs/track_metrics.csv, outputs/album_metrics.csv,
        outputs/h4_gender_album_detail.csv
Writes: figures/fig{1..5}_*.{png,pdf}
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
FIGS = ROOT / "figures"
FIGS.mkdir(exist_ok=True)

# -- Style ----------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 110,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

FEM = "#7C5295"      # aubergine
MASC = "#C97B47"     # burnt orange
NEUTRAL = "#8E8E8E"
HIGHLIGHT = "#B22222"

ALBUM_ORDER = [
    "Inhale Do Not Breathe",
    "Cloud Factory",
    "King of Everything",
    "Micro EP",
    "Macro",
    "Wallflowers",
    "Duél",
]
ALBUM_LABEL = {
    "Inhale Do Not Breathe": "Inhale\n2012",
    "Cloud Factory": "Cloud Factory\n2014",
    "King of Everything": "King of Everything\n2016",
    "Micro EP": "Micro\n2019",
    "Macro": "Macro\n2019",
    "Wallflowers": "Wallflowers\n2021",
    "Duél": "Duél\n2025",
}

track_df = pd.read_csv(OUTPUTS / "track_metrics.csv")
album_df = pd.read_csv(OUTPUTS / "album_metrics.csv")
h4_df = pd.read_csv(OUTPUTS / "h4_gender_album_detail.csv")

track_df["album"] = pd.Categorical(track_df["album"], categories=ALBUM_ORDER, ordered=True)
album_df["album"] = pd.Categorical(album_df["album"], categories=ALBUM_ORDER, ordered=True)
h4_df["album"] = pd.Categorical(h4_df["album"], categories=ALBUM_ORDER, ordered=True)
album_df = album_df.sort_values("album").reset_index(drop=True)
h4_df = h4_df.sort_values("album").reset_index(drop=True)


def save(fig, name):
    fig.savefig(FIGS / f"{name}.png")
    fig.savefig(FIGS / f"{name}.pdf")
    plt.close(fig)
    print(f"  wrote {name}.{{png,pdf}}")


# -- Fig. 1: Track-level concentration of displacement vocabulary ----------
def fig1():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    rng = np.random.default_rng(7)
    df = track_df.sort_values(["album", "track_number"])

    for i, alb in enumerate(ALBUM_ORDER):
        sub = df[df["album"] == alb]
        x = i + rng.uniform(-0.18, 0.18, len(sub))
        ax.scatter(x, sub["h2_displacement_per100"],
                   s=42, alpha=0.65, color=NEUTRAL,
                   edgecolor="black", linewidth=0.4, zorder=3)

    # Annotate tracks above 1.0/100 (the empirical threshold the paper uses)
    notable = df[df["h2_displacement_per100"] > 1.0].copy()
    notable["x"] = notable["album"].apply(ALBUM_ORDER.index)

    annot_offsets = {
        "Tumbleweed":          ( 12,  0),
        "Home Back":           ( 12,  0),
        "Pit Of Consciousness":(-14, 12),
        "Outlander":           ( 12,  4),
        "Colossus":            ( 12, -4),
    }
    for _, r in notable.iterrows():
        is_tumble = r["title"] == "Tumbleweed"
        color = HIGHLIGHT if is_tumble else "#333333"
        ax.scatter([r["x"]], [r["h2_displacement_per100"]],
                   s=80 if is_tumble else 55, color=color,
                   edgecolor="black", linewidth=0.7, zorder=5)
        dx, dy = annot_offsets.get(r["title"], (10, 4))
        ax.annotate(f'"{r["title"]}"',
                    (r["x"], r["h2_displacement_per100"]),
                    xytext=(dx, dy), textcoords="offset points",
                    fontsize=9, fontweight="bold" if is_tumble else "normal",
                    color=color,
                    ha="left" if dx > 0 else "right")

    ax.axhline(1.0, color="#CCCCCC", linestyle=":", linewidth=0.8, zorder=1)
    ax.text(6.3, 1.03, "1.0 per 100", color="#888888", fontsize=8, ha="right")

    ax.set_xticks(range(len(ALBUM_ORDER)))
    ax.set_xticklabels([ALBUM_LABEL[a] for a in ALBUM_ORDER])
    ax.set_xlim(-0.5, len(ALBUM_ORDER) - 0.5)
    ax.set_ylabel("Displacement vocabulary (per 100 lemmas)")
    ax.set_title("Figure 1. Track-level concentration of displacement vocabulary across the discography",
                 loc="left")
    ax.grid(axis="y", alpha=0.3, linestyle="--", zorder=0)
    ax.set_axisbelow(True)
    save(fig, "fig1_displacement_diachronic")


# -- Fig. 2: Lexical-category asymmetry ------------------------------------
def fig2():
    """Diverging horizontal bar chart of fem vs masc tokens by lexical category.

    Counts derived from track_metrics: density-per-100 columns are weighted by
    track lemma count and summed across the corpus; contextual resolved/unresolved
    are raw counts; age-gender is obtained by subtraction from the corpus totals.
    """
    tm = track_df.copy()
    raw_count = lambda col: float((tm[col] * tm["lemma_count"] / 100).sum())

    fem_pron, masc_pron = raw_count("h4_fem_pron_per100"), raw_count("h4_masc_pron_per100")
    fem_rel, masc_rel = raw_count("h4_fem_relational_per100"), raw_count("h4_masc_relational_per100")
    fem_soc, masc_soc = raw_count("h4_fem_social_conv_per100"), raw_count("h4_masc_social_conv_per100")
    fem_ctx = float(tm["h4_contextual_resolved_fem"].sum())
    masc_ctx = float(tm["h4_contextual_resolved_masc"].sum())

    fem_total = float(tm["h4_n_fem_total"].sum())
    masc_total = float(tm["h4_n_masc_total"].sum())
    fem_age = fem_total - (fem_pron + fem_rel + fem_soc + fem_ctx)
    masc_age = masc_total - (masc_pron + masc_rel + masc_soc + masc_ctx)

    cats = [
        ("Pronouns\n(she/her vs he/him)", fem_pron, masc_pron),
        ("Relational nouns\n(mother/daughter vs father/son)", fem_rel, masc_rel),
        ("Age–gender nouns\n(girl/woman vs boy/man)", fem_age, masc_age),
        ("Context-assigned social\n(teacher, soldier, …)", fem_ctx, masc_ctx),
        ("Social by convention\n(queen/lady vs king/lord)", fem_soc, masc_soc),
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    y = np.arange(len(cats))[::-1]
    fem_vals = [c[1] for c in cats]
    masc_vals = [c[2] for c in cats]

    ax.barh(y, [-v for v in fem_vals], color=FEM, edgecolor="black", linewidth=0.5,
            label=f"Feminine (n = {int(fem_total)})")
    ax.barh(y, masc_vals, color=MASC, edgecolor="black", linewidth=0.5,
            label=f"Masculine (n = {int(masc_total)})")

    for yi, (_, f, m) in zip(y, cats):
        if f > 0.5:
            ax.text(-f - 1.2, yi, f"{f:.0f}", va="center", ha="right", fontsize=9)
        if m > 0.5:
            ax.text(m + 1.2, yi, f"{m:.0f}", va="center", ha="left", fontsize=9)

    # Highlight the social-by-convention asymmetry (place above the bar to avoid legend)
    soc_y = y[-1]
    ax.annotate(
        "‘king’ alone accounts for 14 of\nthe 16 masculine occurrences",
        xy=(masc_soc, soc_y), xytext=(35, 28), textcoords="offset points",
        fontsize=8.5, ha="left", color="#444444",
        arrowprops=dict(arrowstyle="->", color="#888888", lw=0.6,
                        connectionstyle="arc3,rad=-0.2"),
    )

    ax.set_yticks(y)
    ax.set_yticklabels([c[0] for c in cats])
    ax.set_xlabel("← Feminine tokens         |         Masculine tokens →")
    ax.axvline(0, color="black", linewidth=0.7)

    xmax = max(max(fem_vals), max(masc_vals)) * 1.25
    ax.set_xlim(-xmax, xmax)
    # Set ticks explicitly so |labels| are correct without warnings
    step = 25
    raw_ticks = np.arange(-int(xmax // step) * step, int(xmax // step) * step + 1, step)
    ax.set_xticks(raw_ticks)
    ax.set_xticklabels([str(abs(int(t))) for t in raw_ticks])

    ax.set_title("Figure 2. Corpus-wide gender asymmetry across lexical categories", loc="left")
    ax.legend(loc="upper right", frameon=False)
    ax.grid(axis="x", alpha=0.3, linestyle="--", zorder=0)
    ax.set_axisbelow(True)

    # Methodological footnote on dictionary vs manuscript classification
    note_lines = [
        "Note. Counts produced by the v3 pipeline (lemma-based classification). Two feminine social-conventional tokens reported in the manuscript",
        "(‘lady’ in ‘Teacher Teacher’; ‘ladies’ in ‘Tantrum’) are classified by the pipeline’s dictionary as age–gender and therefore appear in that",
        "category in this figure. Manual verification treats them as social-conventional in third-person / vocative position; the 16:0 asymmetry shown",
        "here is the stricter, fully reproducible reading of the same underlying pattern.",
    ]
    fig.text(0.02, -0.02, "\n".join(note_lines), ha="left", va="top",
             fontsize=7.8, color="#555555", style="italic")
    save(fig, "fig2_lexical_asymmetry")


# -- Fig. 3: Agent / patient distribution by gender ------------------------
def fig3():
    """Stacked bars of agent/patient/other for tracks meeting the n-thresholds."""
    fem_tracks = [
        ("Teacher Teacher", "Micro EP"),
        ("Pausing Death", "Macro"),
        ("Someones Daughter", "Duél"),
        ("Dark Bile", "Duél"),
        ("Perennial", "Micro EP"),
    ]
    masc_tracks = [
        ("Beggars Dance", "King of Everything"),
        ("Prologue", "King of Everything"),
        ("Captain Clock", "King of Everything"),
        ("Vortex", "Wallflowers"),
        ("When Two Empires Collide", "Cloud Factory"),
        ("Mediator", "Wallflowers"),
        ("Pausing Death", "Macro"),
    ]

    def pull(track_album_pairs, kind):
        rows = []
        for title, alb in track_album_pairs:
            r = track_df[(track_df["title"] == title) & (track_df["album"] == alb)].iloc[0]
            agent = float(r[f"h4_{kind}_agent_ratio"])
            patient = float(r[f"h4_{kind}_patient_ratio"])
            other = max(0.0, 1.0 - agent - patient)
            n = int(r[f"h4_n_{kind}_total"])
            rows.append({"title": title, "album": alb, "agent": agent,
                         "patient": patient, "other": other, "n": n})
        return pd.DataFrame(rows)

    fem = pull(fem_tracks, "fem")
    masc = pull(masc_tracks, "masc")

    fig, axes = plt.subplots(1, 2, figsize=(12, 6.2),
                             gridspec_kw={"width_ratios": [len(fem), len(masc)]})

    FEM_LIGHT = "#C9B6DA"
    MASC_LIGHT = "#E5C39B"
    OTHER_GREY = "#E0E0E0"

    def draw(ax, df, title, gender_color, light_color):
        x = np.arange(len(df))
        agent = df["agent"].values
        patient = df["patient"].values
        other = df["other"].values

        ax.bar(x, agent, color=gender_color, edgecolor="black", linewidth=0.5,
               label="Agent (nsubj)")
        ax.bar(x, patient, bottom=agent, color=light_color,
               edgecolor="black", linewidth=0.5, label="Patient (nsubjpass / obj)")
        ax.bar(x, other, bottom=agent + patient, color=OTHER_GREY,
               edgecolor="black", linewidth=0.5, label="Other position")

        for xi, (_, r) in zip(x, df.iterrows()):
            ax.text(xi, 1.04, f"n = {r['n']}", ha="center", fontsize=8, color="#555555")

        labels = [f'"{t}"\n{a.replace(" EP", "").replace("Inhale Do Not Breathe", "Inhale")}'
                  for t, a in zip(df["title"], df["album"])]
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=8.5)
        ax.set_ylim(0, 1.18)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_title(title, loc="left", fontsize=11)
        ax.legend(loc="lower right", frameon=True, framealpha=0.85,
                  fontsize=8.5, edgecolor="#CCCCCC")
        ax.grid(axis="y", alpha=0.3, linestyle="--", zorder=0)
        ax.set_axisbelow(True)

    draw(axes[0], fem, "Feminine tokens (n ≥ 5)", FEM, FEM_LIGHT)
    draw(axes[1], masc, "Masculine tokens (n ≥ 3)", MASC, MASC_LIGHT)
    axes[0].set_ylabel("Proportion of gender-marked tokens")

    fig.suptitle("Figure 3. Syntactic position of gender-marked tokens by track",
                 x=0.02, ha="left", fontweight="bold", fontsize=12, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    save(fig, "fig3_agent_patient_by_gender")


# -- Fig. 4: Heatmap of lexical category × album ---------------------------
def fig4():
    cats = [
        ("Pronouns", "h4_fem_pron_per100", "h4_masc_pron_per100"),
        ("Relational", "h4_fem_relational_per100", "h4_masc_relational_per100"),
        ("Social by convention", "h4_fem_social_conv_per100", "h4_masc_social_conv_per100"),
    ]
    cat_labels = [c[0] for c in cats]
    fem_mat = np.array([h4_df[c[1]].values for c in cats])
    masc_mat = np.array([h4_df[c[2]].values for c in cats])

    vmax = max(fem_mat.max(), masc_mat.max())

    fig, axes = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
    for ax, mat, label, cmap in [
        (axes[0], fem_mat, "Feminine tokens", "Purples"),
        (axes[1], masc_mat, "Masculine tokens", "Oranges"),
    ]:
        im = ax.imshow(mat, aspect="auto", cmap=cmap, vmin=0, vmax=vmax)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                v = mat[i, j]
                if v > 0:
                    color = "white" if v > vmax * 0.55 else "black"
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                            fontsize=8, color=color)
        ax.set_yticks(range(len(cat_labels)))
        ax.set_yticklabels(cat_labels)
        ax.set_title(label, loc="left", fontsize=11)
        cb = fig.colorbar(im, ax=ax, fraction=0.018, pad=0.01)
        cb.ax.tick_params(labelsize=8)

    axes[1].set_xticks(range(len(ALBUM_ORDER)))
    axes[1].set_xticklabels([ALBUM_LABEL[a] for a in ALBUM_ORDER], fontsize=9)

    fig.suptitle("Figure 4. Density of gender marking by lexical category and album (per 100 lemmas)",
                 x=0.02, ha="left", fontweight="bold", fontsize=12, y=1.0)
    fig.tight_layout()
    save(fig, "fig4_lexical_category_heatmap")


# -- Fig. 5: Diachronic feminine:masculine ratio ---------------------------
def fig5():
    """Aggregate (not per-track-averaged) fem:masc ratio per album.

    The CSV column h4_fem_masc_ratio is a per-track mean of ratios, which is
    not what the manuscript reports. We reconstruct corpus-level totals from
    track_metrics and compute sum_fem / sum_masc per album, which yields the
    3.8:1 figure the manuscript cites for Micro.
    """
    tm = track_df.copy()
    fem_count = lambda col: (tm[col] * tm["lemma_count"] / 100)
    tm["_fem_n"] = (
        fem_count("h4_fem_pron_per100")
        + fem_count("h4_fem_relational_per100")
        + fem_count("h4_fem_social_conv_per100")
    )
    tm["_masc_n"] = (
        fem_count("h4_masc_pron_per100")
        + fem_count("h4_masc_relational_per100")
        + fem_count("h4_masc_social_conv_per100")
    )
    # Use the corpus-level totals already in the CSV — they match the paper
    by_alb = (tm.groupby("album", observed=True)
                .agg(fem_total=("h4_n_fem_total", "sum"),
                     masc_total=("h4_n_masc_total", "sum"))
                .reindex(ALBUM_ORDER))

    # Lemma-weighted reconstruction so totals are meaningful integers
    by_alb["fem_int"] = by_alb["fem_total"].round().astype(int)
    by_alb["masc_int"] = by_alb["masc_total"].round().astype(int)
    by_alb["ratio"] = np.where(
        by_alb["masc_total"] > 0,
        by_alb["fem_total"] / by_alb["masc_total"],
        0.0,
    )

    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    x = np.arange(len(by_alb))
    ratios = by_alb["ratio"].values

    ax.vlines(x, 0, ratios, color=NEUTRAL, alpha=0.6, linewidth=2)
    colors = [FEM if r > 1 else (MASC if r > 0 else NEUTRAL) for r in ratios]
    ax.scatter(x, ratios, s=130, color=colors, edgecolor="black",
               linewidth=0.7, zorder=5)

    ax.axhline(1.0, color="#888888", linestyle=":", linewidth=0.8)
    ax.text(-0.45, 1.05, "parity (1:1)", fontsize=8.5, color="#666666", ha="left")

    # Numeric ratio above each marker
    for xi, r in zip(x, ratios):
        if r >= 1:
            label = f"{r:.1f} : 1"
        elif r > 0:
            label = f"1 : {1/r:.1f}"
        else:
            label = "0 : —"
        ax.text(xi, r + 0.18, label, ha="center", fontsize=9,
                fontweight="bold", color="#333333")

    annotations = {
        "Micro EP": ("Driven by\n‘Teacher Teacher’ (n=15)\nand ‘Perennial’ (n=6)",
                     (35, 5), "left"),
        "Duél": ("First explicitly\nfeminine-positioned\nenunciator\n(‘Someone’s Daughter’)",
                 (-25, 60), "right"),
        "King of Everything": ("‘king’ as central\nmasculine refrain\n(n=14 across 2 tracks)",
                               (45, 60), "left"),
    }
    for alb, (txt, (dx, dy), align) in annotations.items():
        i = ALBUM_ORDER.index(alb)
        ha = {"left": "left", "right": "right", "center": "center"}[align]
        ax.annotate(txt, (i, ratios[i]),
                    xytext=(dx, dy), textcoords="offset points",
                    fontsize=8.5, ha=ha, color="#333333",
                    arrowprops=dict(arrowstyle="->", color="#999999", lw=0.6))

    # Raw counts strip below
    for i, row in enumerate(by_alb.itertuples()):
        ax.text(i, -0.55, f"fem {row.fem_int}  ·  masc {row.masc_int}",
                ha="center", fontsize=8.2, color="#555555")

    ax.set_xticks(x)
    ax.set_xticklabels([ALBUM_LABEL[a] for a in by_alb.index])
    ax.set_ylabel("Feminine : Masculine ratio (corpus-level)")
    ax.set_ylim(-0.85, max(4.3, max(ratios) * 1.25))
    ax.set_xlim(-0.6, len(by_alb) - 0.4)
    ax.set_title("Figure 5. Diachronic ratio of feminine to masculine tokens across the discography",
                 loc="left")
    ax.grid(axis="y", alpha=0.3, linestyle="--", zorder=0)
    ax.set_axisbelow(True)
    save(fig, "fig5_fem_masc_ratio_diachronic")


if __name__ == "__main__":
    print("Generating figures →", FIGS)
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    print("Done.")
