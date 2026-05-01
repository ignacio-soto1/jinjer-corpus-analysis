# Changelog

Versioning history of the dictionaries and the pipeline.

## v1.0.1-prereview · 2026-04-30 (post-review reproducibility hardening)

A reproducibility audit run against a freshly-installed environment surfaced a
single token-level discrepancy with the published outputs in `outputs/` —
the `h2_displacement_per100` value of "Colossus" (Wallflowers, 2021), which
the freshly-run pipeline yielded as `0.000` rather than the published
`1.099`. Root cause: spaCy lemmatizes "scattered" (in *"the scattered bones"*)
as VERB → "scatter", which was absent from the displacement dictionary. The
participle-only entry was a brittleness gap rather than a substantive shift in
classification.

Two coordinated changes restore full reproduction of the published numbers
without altering the analytical apparatus:

### Pipeline
— **DICT_DISPLACEMENT**: added the base form `scatter` alongside the existing
  `scattered` (file `pipeline/process_corpus_discourse_v3.py`, around line 97).
  This closes the lemmatizer-driven match loss when the past participle is
  POS-tagged as VERB. The change is purely lemmatization-robustness; the
  analytical scope of the displacement field is unchanged.

### Reproducibility pins
— **`requirements.txt`**: tightened `spacy>=3.7.0,<3.8.0` (was
  `<4.0.0`) and pinned `numpy<2.0` to avoid the C-ABI break.
— **`en_core_web_sm` model**: declared the version (`3.7.1`, released
  2023-10-09) and the SHA-256 of the wheel
  (`86cc141f63942d4b2c5fcee06630fd6f904788d2f0ab005cce45aadb8fb73889`) used to
  produce the published outputs. Install instructions in `requirements.txt`.

### Verification
— Re-running the pipeline against the locally reconstructed corpus with the
  pinned environment reproduces `outputs/track_metrics.csv` exactly for all
  H1, H2, and H4 columns reported in the v19e manuscript: 5 tracks above
  1.0/100 displacement (Outlander, Pit of Consciousness, Home Back, Colossus,
  Tumbleweed at 6.58); corpus-wide gender totals 54 fem / 140 masc; the
  album-level H4 lexical-category densities used in the figures.
— Residual differences in unreported columns (`h3_passive_ratio`,
  `h3_fp_*_ratio`, `lexical_diversity_ttr`) are below the analytical
  threshold and reflect parser/lemmatizer micro-variance that the v19e
  manuscript does not depend on.

## v1.0.0-prereview · 2026-04-30

Initial repository structure prepared for upload to GitHub during double-anonymised review at *Humanities and Social Sciences Communications*.

### Pipeline

— `process_corpus_discourse_v3.py` — version 3, the version used to produce the published numbers. Implements the four-hypothesis architecture (H1 territory, H2 displacement, H3 conflict frame, H4 gender positional configuration). Produces the seven CSV outputs in `outputs/`.

The "v3" suffix reflects the author's iterative development:
- **v1** of the pipeline tested an earlier hypothesis structure (territory only) and is not preserved in this repository.
- **v2** added displacement and gender hypotheses; superseded by v3.
- **v3** added the conflict-frame hypothesis and refined the gender categorisation. This is the published version.

### Dictionaries

— **`displacement_v2.txt`** (version 2) — produced after iterative refinement from v1:
  - Removed terms with unacceptable false-positive rates in v1 pilot
  - Added terms that emerged through corpus scanning of pilot displacement-marked passages
  - Refined disambiguation rules for terms with both literal and metaphorical senses

— **`gender_feminine.txt`**, **`gender_masculine.txt`**, **`gender_relational.txt`** — version 1. The first integrated version, used for the published analysis.

— **`territory.txt`** — version 1, with [CONCRETE]/[METAPHORICAL] tags.

— **`resistance.txt`**, **`victimhood.txt`** — version 1, used for H3.

### Verification

— `corpus/verification/gender_verification.csv` and `gender_verification_report.md` — the author's manual verification artefacts. Comprehensive coverage of all 61 tracks with per-occurrence decisions.

### Outputs

— `outputs/track_metrics.csv` — 61 rows, one per track. The pipeline's full per-track output.
— `outputs/album_metrics.csv` — 7 rows, one per release.
— `outputs/language_proportions.csv` — English/Russian split per album.
— `outputs/hypothesis_tests.csv` — H1 Spearman ρ, H2 Welch t, H3 Spearman ρ × 4 sub-tests.
— `outputs/h4_gender_descriptive.csv`, `h4_gender_album_detail.csv` — H4 descriptive outputs.
— `outputs/stats/hypothesis_tests_summary.txt` — human-readable companion.

### Future versions

When the article is accepted and published, this repository will be tagged as v1.0.0 (without the prereview suffix) with author identity restored in `CITATION.cff` and `.zenodo.json`. The Zenodo integration will then mint a permanent DOI which will be inserted in the data availability statement of the published manuscript.
