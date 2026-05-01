# jinjer-corpus-analysis

Computational analysis of the lyrical corpus of the Ukrainian metal band Jinjer (2012–2025), supporting the article "Beyond Female-Fronted: Allegorical Agency and Symbolic Vacancy in Jinjer's Lyrical Corpus (2012–2025)" submitted to *Humanities and Social Sciences Communications* (Springer Nature).

> **Note on copyright.** This repository does **not** distribute lyrics. Lyrics are the intellectual property of the band Jinjer and their publishers. The repository distributes (1) track metadata, (2) the analysis pipeline (with embedded thematic dictionaries), (3) aggregated quantitative outputs, (4) verification artefacts, and (5) a reconstruction script (`corpus/build_corpus.py`) that builds the local corpus from sources the user themselves licenses.

## Citation

If you use this repository, please cite the article and the repository:

```
[Author]. (Forthcoming). Beyond Female-Fronted: Allegorical Agency and Symbolic
Vacancy in Jinjer's Lyrical Corpus (2012-2025). Humanities and Social Sciences
Communications. [DOI to be inserted upon acceptance]

[Author]. (2026). jinjer-corpus-analysis (Version 1.0). [Zenodo DOI to be inserted upon publication]
```

A `CITATION.cff` file is provided for automated citation generation. Authorship metadata is left as placeholder during double-anonymised review.

## Repository structure

```
jinjer-corpus-analysis/
├── README.md                  This file
├── CITATION.cff               Citation metadata (placeholder during review)
├── LICENSE                    MIT for code, CC-BY 4.0 for derived data
├── .gitignore
├── .zenodo.json               Zenodo metadata (placeholder during review)
├── requirements.txt           Pinned dependencies
│
├── corpus/
│   ├── README.md              How to reconstruct the corpus locally
│   ├── metadata.csv           61 tracks with metadata · NO LYRICS
│   ├── build_corpus.py        Reconstruction script (source-agnostic)
│   ├── local/
│   │   └── README.md          Placeholder for user's locally-reconstructed corpus
│   └── verification/
│       ├── README.md
│       ├── gender_verification.csv          Per-occurrence verification log
│       └── gender_verification_report.md    Narrative verification report
│
├── pipeline/
│   ├── README.md
│   ├── process_corpus_discourse_v3.py       Single-script pipeline (dictionaries embedded)
│   └── make_figures.py                       Figure generation from outputs CSVs
│
├── dictionaries/
│   └── README.md              Pointer to embedded dictionaries in pipeline script
│
├── outputs/
│   ├── README.md
│   ├── track_metrics.csv          per-track output (61 rows)
│   ├── album_metrics.csv          per-album output (7 rows)
│   ├── language_proportions.csv   English/Russian per album
│   ├── hypothesis_tests.csv       H1, H2, H3 inferential tests
│   ├── h4_gender_descriptive.csv  H4 descriptive cross-album
│   ├── h4_gender_album_detail.csv H4 per-album detail
│   └── stats/
│       └── hypothesis_tests_summary.txt   Human-readable companion
│
├── figures/
│   ├── README.md                              What each figure shows
│   ├── fig1_displacement_diachronic.{png,pdf}
│   ├── fig2_lexical_asymmetry.{png,pdf}
│   ├── fig3_agent_patient_by_gender.{png,pdf}
│   ├── fig4_lexical_category_heatmap.{png,pdf}
│   └── fig5_fem_masc_ratio_diachronic.{png,pdf}
│
└── docs/
    ├── methodology.md         Methodological summary
    └── changelog.md           Pipeline and dictionary version history (see v1.0.1 for the
                               reproducibility-hardening pin and DICT_DISPLACEMENT patch)
```

## What this repository contains

— **Track metadata** for 61 tracks across 7 studio releases (Inhale 2012, Cloud Factory 2014, King of Everything 2016, Micro 2019, Macro 2019, Wallflowers 2021, Duél 2025). Distribution: 8 + 8 + 10 + 4 + 9 + 11 + 11.

— **The analysis pipeline** as a single Python script that computes four diagnostic dimensions of the lyrical archive, with thematic dictionaries embedded as Python sets:
  - **H1 (pipeline label)** Progressive delocalization (territory: concrete vs metaphorical) — diagnostic dimension, not developed in the manuscript
  - **H2 (pipeline label)** Post-2022 reactivation of displacement vocabulary — addressed in the manuscript as **RQ1** (track-level concentration)
  - **H3 (pipeline label)** Conflict frame transformation (passive ratio, resistance, victimhood, first-person agency) — diagnostic dimension, not developed in the manuscript
  - **H4 (pipeline label)** Gender positional configuration (cross-tabulation of feminine and masculine tokens across five lexical categories with agent/patient ratios via spaCy dependency parsing) — addressed in the manuscript as **RQ2** (gender configuration)

The labels H1–H4 are pipeline-internal identifiers tied to the column prefixes (`h1_*`, `h2_*`, `h3_*`, `h4_*`) in the output CSVs. The manuscript develops two of these dimensions as research questions (RQ1 and RQ2) within a framework of *small-corpus computational hermeneutics*.

— **Real pipeline outputs** as committed CSVs that match the numbers reported in the article.

— **The manual verification artefacts** that ground the gender analysis (every occurrence verified pista by pista).

— **A reconstruction script** that lets the user build the local corpus from sources they themselves license.

## What this repository does NOT contain

— Lyrics. In any form. Not raw text, not JSON, not extracted KWIC concordance lines, not dependency-parsed sentences with verbatim text.

— Audio files.

— Author identity during double-anonymised review.

## Replicating the analysis

```bash
# Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install the pinned spaCy model (verify SHA-256 — see requirements.txt)
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Reconstruct the local corpus (user provides their own legal sources)
python corpus/build_corpus.py --sources-dir /path/to/your/sources

# Run the analysis pipeline
python pipeline/process_corpus_discourse_v3.py

# (Optional) Regenerate the five figures from the CSVs
python pipeline/make_figures.py
```

Pipeline outputs go to `outputs/`; figures go to `figures/`. Re-running the pipeline on the same corpus with the pinned environment is deterministic.

### Reproducibility note

Full reproducibility of the published numbers requires the pinned spaCy + model versions declared in `requirements.txt` (model `en_core_web_sm` 3.7.1, SHA-256 `86cc141f63942d4b2c5fcee06630fd6f904788d2f0ab005cce45aadb8fb73889`). Looser pins admit lemmatizer drift across model releases that changes a small number of token-level decisions; see `docs/changelog.md` v1.0.1-prereview for the audit, the dictionary patch, and a description of the residual non-published columns that still vary slightly with parser version.

## Diagnostic dimensions computed by the pipeline

The pipeline operates within a framework of *small-corpus computational hermeneutics*: rather than confirmatory hypothesis-testing, it computes four descriptive diagnostic dimensions of the lyrical archive. Inferential procedures (Spearman ρ, Welch t-test) are reported as **descriptive diagnostics** of release-level distributional properties, not as falsificatory tests. The two dimensions developed analytically in the manuscript are presented as **research questions (RQ1, RQ2)** rather than hypotheses.

| Dimension (pipeline label)                  | Diagnostic procedure       | Inferential result              | Manuscript treatment                                      |
|---------------------------------------------|----------------------------|---------------------------------|-----------------------------------------------------------|
| H1 · Progressive delocalization             | Spearman ρ vs year         | No monotonic trend (ρ = −0.09 / −0.45) | not developed in v19e                              |
| H2 · Post-2022 displacement reactivation    | Welch t-test (Duél vs rest)| No release-level mean shift (p = 0.398) | **RQ1** in §3.2: empirical anchor relocated to track-level concentration ('Tumbleweed' at 6.58/100 lemmas) |
| H3 · Conflict frame transformation          | Spearman ρ × 4 markers     | No monotonic trends             | not developed in v19e                                     |
| H4 · Gender positional configuration        | Descriptive (no inference) | n/a (descriptive)               | **RQ2** in §3.3–3.6 and §4.1 (AASV category)              |

The manuscript reports the H2 inferential null transparently and locates the empirical anchor at the track-level concentration documented in §3.2. For H4, the manuscript articulates the AASV (allegorical agency and symbolic vacancy) category from the descriptive distribution; AASV itself is offered prospectively in §5 as a testable configuration for other corpora.

The repository preserves the full pipeline output including H1 and H3 (the two diagnostic dimensions not developed in the current article) for transparency about what the pipeline computes and to support future analytical work.

## Tools and dependencies

— Python 3.9+ (tested with 3.9 and 3.12)
— spaCy `>=3.7.0,<3.8.0` with `en_core_web_sm` 3.7.1 (pinned; see `requirements.txt`)
— pandas, numpy (`<2.0`), scipy
— langdetect (with fixed seed for reproducibility)
— matplotlib (for `pipeline/make_figures.py`, optional)
— AntConc 4.x (used by the author for manual verification, not required for replication)

A `requirements.txt` pins the exact versions used.

## License

— **Code** (`pipeline/`, `corpus/build_corpus.py`): MIT License
— **Derived data** (`outputs/`, `corpus/metadata.csv`, `corpus/verification/`): Creative Commons Attribution 4.0 International
— **Documentation** (`README.md`, `docs/`): CC-BY 4.0

The lyrics themselves remain the property of their respective rights-holders and are not licensed by this repository.

## AI assistance

The pipeline was developed with LLM-collaborative coding assistance (per the `Author` line in `process_corpus_discourse_v3.py`). The dictionaries, analytical decisions, research-question specifications, and manual verification are the author's; the implementation of dictionary-search routines, dependency-parsing wrappers, and aggregation code was developed in an LLM-collaborative loop.

The article's AI disclosure (§2.3) discloses this and follows the methodological framework articulated in Karjus (2025) on machine-assisted quantitizing designs.

## Issues and contact

The author welcomes correction of methodological errors, bug reports against the pipeline code, and discussion of analytical extensions. During the double-anonymised review period, please use GitHub Issues for technical questions; do not attempt to identify or contact the author by other means.

After publication, contact information will be inserted in `CITATION.cff`.
