# figures/

Five publication-ready figures generated from the pipeline outputs in `outputs/`. Each is provided as both PNG (300 DPI, for in-text use) and PDF (vector, for typesetting).

The figures are produced by `pipeline/make_figures.py`, which reads `outputs/track_metrics.csv`, `outputs/album_metrics.csv`, and `outputs/h4_gender_album_detail.csv` directly. Re-running the figure script after re-running the pipeline reproduces them.

## Figures

| File                                | Source columns                                                | Article reference          |
|-------------------------------------|---------------------------------------------------------------|----------------------------|
| `fig1_displacement_diachronic`      | `h2_displacement_per100` per track, by album                 | §3.2 (RQ1 in the manuscript; pipeline H2)          |
| `fig2_lexical_asymmetry`            | Corpus-wide totals across `h4_*_pron`, `_relational`, `_social_conv`, `_contextual_resolved`, plus age–gender by subtraction | §3.4, Table 4              |
| `fig3_agent_patient_by_gender`      | `h4_fem_agent_ratio`, `h4_fem_patient_ratio`, masculine equivalents, filtered to tracks with substantive token presence | §3.5, Tables 5a–5b         |
| `fig4_lexical_category_heatmap`     | `h4_*_pron_per100`, `_relational_per100`, `_social_conv_per100` from `h4_gender_album_detail.csv` | §3.4 (visualised diachronically) |
| `fig5_fem_masc_ratio_diachronic`    | Corpus-level `n_fem_total` / `n_masc_total` per album        | §3.3 (Table 3 visualisation) |

## Reproducing the figures

```bash
python pipeline/make_figures.py
```

The script reads the CSVs in `outputs/` and writes both `.png` and `.pdf` for each figure. It does not depend on the lyric corpus directly, only on the aggregated CSVs.

## Notes on Fig. 2

The figure displays the v3 pipeline's lemma-based classification, in which `lady` and `ladies` are placed in the age–gender category (per the `NOUNS_AGE_GENDER_FEM` set in the pipeline). The manuscript Section 3.4 treats those two tokens as social-conventional. The 16 : 0 asymmetry shown in the figure is therefore a stricter, fully reproducible reading of the same underlying pattern — see the in-figure note for details.

## Color palette

The palette is intentionally non-stereotypical: feminine tokens use aubergine (`#7C5295`), masculine use burnt orange (`#C97B47`). This avoids the conventional pink/blue mapping while keeping the two registers visually distinct.
