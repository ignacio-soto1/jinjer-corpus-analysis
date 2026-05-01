# dictionaries/

The thematic dictionaries used by the pipeline are **embedded as Python sets in the analysis script** at `pipeline/process_corpus_discourse_v3.py` (lines 71–168 of the script). This is a deliberate design decision: the dictionaries are part of the pipeline's analytical apparatus and version with the code, not as separate data files.

## Where to find each dictionary

Open `pipeline/process_corpus_discourse_v3.py` and search for the relevant constant:

| Constant                          | Used by               | Article reference                    |
|----------------------------------|-----------------------|--------------------------------------|
| `DICT_TERRITORY_CONCRETE`        | H1                    | not developed in v19e manuscript    |
| `DICT_TERRITORY_METAPHORICAL`    | H1                    | not developed in v19e manuscript    |
| `DICT_DISPLACEMENT`              | H2                    | §3.2, §4.2 of manuscript            |
| `DICT_RESISTANCE`                | H3                    | not developed in v19e manuscript    |
| `DICT_VICTIMHOOD`                | H3                    | not developed in v19e manuscript    |
| `PRONOUNS_FEM`                   | H4 (a)                | §3.5, §4.1                          |
| `PRONOUNS_MASC`                  | H4 (a)                | §3.5, §4.1                          |
| `NOUNS_RELATIONAL_FEM`           | H4 (b)                | §3.5, Table 4                       |
| `NOUNS_RELATIONAL_MASC`          | H4 (b)                | §3.5, Table 4                       |
| `NOUNS_RELATIONAL_NEUTRAL`       | H4 (b)                | §3.5                                |
| `NOUNS_AGE_GENDER_FEM`           | H4 (c)                | §3.5                                |
| `NOUNS_AGE_GENDER_MASC`          | H4 (c)                | §3.5                                |
| `NOUNS_SOCIAL_FEM_BY_CONVENTION` | H4 (d)                | §3.5, §4.1 (queen vs king asymmetry)|
| `NOUNS_SOCIAL_MASC_BY_CONVENTION`| H4 (d)                | §3.5, §4.1                          |
| `NOUNS_SOCIAL_CONTEXTUAL`        | H4 (e)                | §3.5, contextually resolved by coreference heuristic |

## Why dictionaries are embedded in the script

Three reasons:

1. **Provenance.** The pipeline's published numbers were produced by exactly these dictionaries as embedded. Maintaining them as separate `.txt` files would risk drift between what the script reads and what the article reports.

2. **Atomic versioning.** `process_corpus_discourse_v3.py` can be cited as a single object (file, line range) that includes both the algorithm and the dictionaries.

3. **Replication clarity.** A user who clones the repository runs one script and gets the published outputs. No file-loading boilerplate, no risk of missing dictionary files.

## How the dictionaries were constructed

Each dictionary was constructed through a five-step iterative process documented in §2.3 of the article:

**Step 1 · Seed list from analytical question.** Drawn from the relevant analytical literature.

**Step 2 · Expansion via thesaurus and corpus.** General-language thesauri, scanning the corpus for adjacent terms, domain-specific glossaries.

**Step 3 · Pruning of overgeneralisations.** Terms with unacceptable false-positive rates removed or paired with disambiguation rules. The `NOUNS_SOCIAL_CONTEXTUAL` set is the operationalisation of this step for context-dependent gender markers — the script uses a coreference heuristic (gendered pronoun in the same or following sentence) to resolve these contextually.

**Step 4 · Manual verification.** All hits manually verified. The verification log is in `corpus/verification/`.

**Step 5 · Author re-review.** Dictionaries re-reviewed line by line for analytical coherence.

## Modifying the dictionaries

If you want to test alternative dictionary specifications:

1. Edit the relevant constant directly in `pipeline/process_corpus_discourse_v3.py`.
2. Re-run the pipeline.
3. Compare your new outputs with `outputs/` (the published numbers).

For systematic ablation studies, we recommend you fork the repository, modify the script, and document the changes in your fork's CHANGELOG.

## Limitations

— **English-only.** The pipeline applies these dictionaries only to tracks declared as English in `corpus/metadata.csv`. The single Russian track ("Zhelayu Znachit Poluchu", Cloud Factory 2014 track 8) is excluded from English lemma analysis.

— **Constructivist nature.** The dictionaries inscribe the author's analytical conventions for each category. Other analysts working on the same corpus may construct different dictionaries and arrive at different counts. The article addresses this in §2.3 and §4.4.

— **Personifications not lemma-captured.** Allegorical personifications of abstract nouns (Death, Madam Melancholy, Nature) are NOT captured by simple lemma matching. They are identified through manual verification and treated separately in the qualitative analysis. This is the basis of the AASV (allegorical agency and symbolic vacancy) category articulated in §4.1 of the article.

— **Lemmatizer-robustness.** Some inflected forms tagged as VERB by spaCy are reduced to base form, which means a participle-only dictionary entry (e.g. `scattered` without `scatter`) silently misses matches. The published `DICT_DISPLACEMENT` includes `scatter` alongside `scattered` for this reason; analogous gaps may exist in other dictionaries (e.g. `wilted` without `wilt`, `replanted` without `replant`). For full reproducibility against the published outputs, use the spaCy pin declared in `requirements.txt` (model `en_core_web_sm` 3.7.1, SHA-256 `86cc141f…`); see `docs/changelog.md` v1.0.1-prereview for context.
