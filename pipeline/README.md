# pipeline/

The single-script analysis pipeline: `process_corpus_discourse_v3.py`.

## What the script does

A single Python script that runs the four-dimension discourse analysis end-to-end:

1. Loads `corpus/metadata.csv` (61 tracks).
2. For each English track: reads the corresponding lyric file from `corpus/local/{filename}`, lemmatises with spaCy, computes per-track metrics for H1 (territory), H2 (displacement), H3 (conflict frame markers), and H4 (gender positional configuration). H1–H4 are pipeline-internal labels; the manuscript develops H2 and H4 as research questions RQ1 and RQ2.
3. Aggregates per-track metrics into per-album metrics.
4. Runs inferential diagnostics (Spearman ρ for H1 and H3; Welch t-test for H2; descriptive summary for H4). These are reported as descriptive characterisations of distributional properties at release level, not as confirmatory hypothesis tests.
5. Writes seven CSVs to `outputs/`.

## Embedded dictionaries

The thematic dictionaries are embedded as Python sets in this script (lines 71–168). See `dictionaries/README.md` for the rationale and the mapping of each set to the diagnostic dimension it supports.

## Inputs

— `corpus/metadata.csv` (61 rows, columns: filename, album, year, track_number, title, language)
— `corpus/local/{filename}` for each of the 61 lyric files (produced by `corpus/build_corpus.py`)

## Outputs

— `outputs/track_metrics.csv` (per-track output, 61 rows)
— `outputs/album_metrics.csv` (per-album aggregation, 7 rows)
— `outputs/language_proportions.csv` (English/Russian per album)
— `outputs/hypothesis_tests.csv` (H1, H2, H3 inferential diagnostics — filename retained for backwards compatibility with the v1.0.0 release; the file holds release-level descriptive diagnostics, not confirmatory tests)
— `outputs/h4_gender_descriptive.csv` (H4 descriptive cross-album)
— `outputs/h4_gender_album_detail.csv` (H4 per-album detail)

## Running

```bash
# After setting up venv and reconstructing corpus/local/
python pipeline/process_corpus_discourse_v3.py
```

The script must be run from the repository root.

## Determinism

— spaCy `en_core_web_sm` lemmatisation and dependency parsing are deterministic given the same model version.
— Frequency counts and dictionary matching are deterministic.
— The Welch t-test, Spearman ρ, and Mann-Whitney U from scipy are deterministic.
— No randomised sampling at any stage.
— `langdetect` uses a fixed random seed (`DetectorFactory.seed = 42`) for reproducibility.

## Manual verification step

The article reports that all KWIC hits were manually verified before inclusion in the analysis. This verification is documented in `corpus/verification/gender_verification_report.md` and the corresponding CSV. The verification is **not** automated by the pipeline. Pipeline output and verification results are aligned manually by the author.
