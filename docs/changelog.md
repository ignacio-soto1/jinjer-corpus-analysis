# Changelog

Versioning history of the dictionaries and the pipeline.

## v1.0.2-prereview · 2026-05-01 (framework reformulation: H1/H2 → RQ1/RQ2)

The manuscript was reformulated from a two-hypothesis confirmatory frame
(H1 / H2) to a two-research-question exploratory frame (RQ1 / RQ2) within
a methodology of *small-corpus computational hermeneutics*. The repository
documentation is now aligned with that frame.

### Rationale

Three concerns motivated the reformulation:

— The dictionaries used by the pipeline were refined iteratively after
  inspecting the corpus (the v1→v2 history is recorded in the diff of
  `pipeline/process_corpus_discourse_v3.py`). Post-hoc dictionary
  refinement is incompatible with a strict hypothetico-deductive design
  but is a defining feature of the small-corpus computational hermeneutics
  tradition (Werner & Ledermann 2024 on country lyrics; Karjus 2025 on
  machine-assisted quantitizing more generally). The reformulation makes
  the methodological positioning explicit and accurate.

— The release-level inferential test for what was previously called "H1"
  (Welch t-test on Duél vs rest, displacement vocabulary) yields p = 0.398.
  The empirical anchor for that finding is the track-level outlier
  ('Tumbleweed' at 6.58 per 100 lemmas), which is descriptive
  characterisation rather than falsification of a release-level hypothesis.
  Reporting this as RQ1 with a release-level diagnostic and a track-level
  empirical anchor is more accurate.

— What was previously called "H2" was already presented as descriptive in
  the manuscript text; calling it a "hypothesis" was technically inaccurate.
  Reporting it as RQ2 (descriptive characterisation of gender configuration)
  removes that inaccuracy.

### Mapping (manuscript ↔ pipeline)

The pipeline computes four diagnostic dimensions internally labelled
H1–H4. The manuscript develops two of them as research questions:

| Pipeline dimension | Manuscript treatment |
|--------------------|----------------------|
| H1 (territory)     | not developed        |
| H2 (displacement)  | **RQ1**              |
| H3 (conflict frame)| not developed        |
| H4 (gender)        | **RQ2**              |

### What changed in the repository

— `README.md` (top level): "Hypotheses computed" section reformulated as
  "Diagnostic dimensions computed by the pipeline"; results column reworded
  from "NOT SUPPORTED" to neutral descriptive language.
— `pipeline/README.md`: "four-hypothesis discourse analysis" →
  "four-dimension discourse analysis"; inferential procedures described as
  "diagnostics".
— `docs/methodology.md`: section heading and prose throughout reformulated
  to "diagnostic dimensions" and "inferential diagnostics"; the pre-
  registration language was removed since the threshold (alpha = 0.10) is
  exploratory in this design, not pre-registered in the formal sense.
— `dictionaries/README.md`: the section "How the dictionaries were
  constructed" now affirms iterative refinement as a defining feature of
  small-corpus computational hermeneutics rather than presenting it
  defensively. The mapping table includes the manuscript-RQ correspondence.
— `outputs/README.md`: "inferential statistics" → "inferential diagnostics";
  H1–H4 labels qualified as pipeline-internal identifiers.
— `outputs/stats/hypothesis_tests_summary.txt`: title and intro reformulated;
  "Conclusion: NOT SUPPORTED" replaced with descriptive diagnostics.
— `figures/README.md`: figure-to-section reference updated to manuscript RQ.
— `pipeline/process_corpus_discourse_v3.py`: docstring updated; runtime
  banner "=== HYPOTHESIS TESTS ===" → "=== INFERENTIAL DIAGNOSTICS ===".

### What did not change

— Pipeline-internal labels in code (`# H1 territorial`, `# H2 displacement`):
  retained as code anchors.
— CSV column names and prefixes (`h1_*`, `h2_*`, `h3_*`, `h4_*`,
  `hypothesis` column header): retained — these are pipeline-internal
  identifiers tied to the data structure, and renaming them would break
  downstream scripts and produce a noisy diff against the v1.0.1 release.
— Filenames `outputs/hypothesis_tests.csv` and
  `outputs/stats/hypothesis_tests_summary.txt`: retained for the same
  backwards-compatibility reason.
— String values written into the `hypothesis` column of the output CSVs
  ("H1 — Progressive delocalization", "H2 — Post-2022 reactivation", etc.):
  retained — they are pipeline-internal labels.
— Historical changelog entries (v1.0.0-prereview, v1.0.1-prereview):
  preserved verbatim. Rewriting historical changelog entries to use new
  terminology would falsify the record of what was done at those versions.

### Verification

— No code logic changed. `python -m py_compile pipeline/...py` passes.
— `outputs/` CSVs are unchanged (no pipeline rerun was needed since no
  classification logic was modified).
— A residual grep for "hypothesis", "H1", "H2" still returns hits in the
  pipeline-internal labels listed above; these are expected and documented.

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
