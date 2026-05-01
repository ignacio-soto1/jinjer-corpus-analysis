# outputs/

The aggregated quantitative outputs of the pipeline. The CSV files in this directory are the actual outputs produced by `pipeline/process_corpus_discourse_v3.py` against the corpus of 61 tracks, and they correspond directly to the numbers reported in the article.

These outputs are committed to the repository as a reference. Running the pipeline against a freshly-reconstructed local corpus should reproduce these tables. If reproduction yields different numbers, the discrepancy should be investigated and reported via GitHub Issues.

## Files

| File                              | Pipeline produces it from | What it contains                                         |
|-----------------------------------|---------------------------|----------------------------------------------------------|
| `track_metrics.csv`               | per-track aggregation     | One row per track (61 rows): char count, lemma count, TTR, and per-100-lemma metrics for H1, H2, H3, H4 |
| `album_metrics.csv`               | per-album aggregation     | One row per release (7 rows): mean per-100-lemma metrics |
| `language_proportions.csv`        | language detection        | English/Russian proportion per album                     |
| `hypothesis_tests.csv`            | inferential diagnostics   | H1 (Spearman), H2 (Welch t-test), H3 (Spearman) release-level diagnostic results — descriptive, not confirmatory; filename retained for backwards compatibility |
| `h4_gender_descriptive.csv`       | descriptive aggregation   | H4 cross-album means/min/max for gender metrics          |
| `h4_gender_album_detail.csv`      | per-album detail          | H4 detail per album                                      |
| `stats/hypothesis_tests_summary.txt` | human-readable summary | Narrative companion to `hypothesis_tests.csv`            |

## Mapping to article tables

The current manuscript v19e reports a subset of the pipeline's full output. The mapping is:

— **Article Table 1 (corpus overview)** ←→ first three columns of `album_metrics.csv` (lemma_count, ttr) plus track counts from `track_metrics.csv`.
— **Article Table 2 (displacement density)** ←→ `h2_displacement_per100` column from `album_metrics.csv` and `track_metrics.csv`.
— **Article Table 3 (gender density)** ←→ `h4_total_gendered_per100`, `h4_fem_pron_per100`, `h4_masc_pron_per100` columns.
— **Article Table 4 (lexical categories)** ←→ relational + social-conventional columns of `h4_gender_album_detail.csv`, aggregated.
— **Article Table 5a (feminine syntactic)** ←→ `h4_fem_agent_ratio`, `h4_fem_patient_ratio` from `track_metrics.csv`, filtered to tracks with substantive feminine token presence.
— **Article Table 5b (masculine syntactic)** ←→ idem with masculine columns.

The pipeline computes additional diagnostic dimensions (H1 territory, H3 conflict-frame markers) that are not developed in the v19e manuscript but are preserved here for transparency. The labels H1–H4 are pipeline-internal identifiers; the manuscript develops H2 and H4 as research questions RQ1 and RQ2 respectively, within a framework of small-corpus computational hermeneutics.

## Note on lyric content

These CSV files do not contain lyric content. They contain only aggregated counts, ratios, and metadata. No verbatim text from the corpus is reproduced.

## Determinism

Re-running the pipeline against the same corpus should reproduce identical numerical outputs. The only sources of non-determinism would be:

— A change in the spaCy model version (the requirements pin to en_core_web_sm of a specific spaCy version)
— A change in the dictionaries (versioned in `dictionaries/`)
— A change in the corpus itself (depends on the user's reconstruction)

Any deviation from these three should be reported as a bug via GitHub Issues.
