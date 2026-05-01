# Methodology summary

This document summarises the methodological architecture of the analysis. The full methodological discussion is in §2 of the article. This summary is provided so that the repository is self-contained for reproducibility purposes.

## The four-hypothesis pipeline

The analysis applies a four-hypothesis architecture to a corpus of 61 lyric texts spanning seven studio releases (2012–2025). The current manuscript v19e develops two of these hypotheses (H2 and H4) as published findings; the other two (H1 and H3) are computed by the pipeline and preserved in the outputs for transparency, but not developed in the article.

### H1 · Progressive delocalization

Tests whether territory vocabulary in the corpus shifts from concrete to metaphorical over the diachronic trajectory.

— Dictionary: `dictionaries/territory.txt` with [CONCRETE] and [METAPHORICAL] tags.
— Test: Spearman rank correlation between density and release year (n_albums = 7).
— Result: ρ = -0.09 (concrete) and -0.27 (metaphorical), p > 0.10. Not supported.
— Article reference: not developed in v19e.

### H2 · Post-2022 reactivation of displacement vocabulary

Tests whether Duél (2025), composed under conditions of active war, shows higher displacement vocabulary density than the rest of the corpus.

— Dictionary: `dictionaries/displacement_v2.txt`.
— Test: Welch's t-test (Duél vs rest of corpus, per-track densities, equal_var=False).
— Result: t = 0.881, p = 0.398. Not supported at the album level.
— Reformulation: the track-level outlier (Tumbleweed at 6.58 per 100 lemmas, with four unique displacement lemmas: uprooted, replanted, wilted, stranger) becomes the empirical anchor of the analysis.
— Article reference: §3.2, §4.2.

### H3 · Conflict frame transformation

Tests whether the rhetorical economy of conflict — passive ratio, resistance vocabulary, victimhood vocabulary, first-person agent ratio — transforms diachronically across the trajectory.

— Dictionaries: `dictionaries/resistance.txt`, `dictionaries/victimhood.txt`, plus syntactic-role detection from spaCy dependency parses.
— Test: Spearman rank correlation × four sub-tests vs release year.
— Result: ρ in the range -0.595 to 0.126, all p > 0.10. Not supported.
— Article reference: not developed in v19e.

### H4 · Gender positional configuration

Examines the descriptive distribution of gender-marked tokens across five lexical categories with agent/patient ratios from dependency parsing.

— Dictionaries: `dictionaries/gender_feminine.txt`, `gender_masculine.txt`, `gender_relational.txt`.
— Test: descriptive (no inferential test pre-registered).
— Five lexical categories: pronouns, relational nouns, social-conventional nouns, contextual social nouns, age-gender nouns.
— Three syntactic positions: agent (nsubj of active verb), patient (dobj/pobj/nsubjpass), other.
— Result: pista por pista distributions and per-album aggregates committed in `outputs/`.
— Article reference: §3.5, §4.1, §4.3 — articulated in the article through the AASV (allegorical agency and symbolic vacancy) category.

## Why this architecture

The four hypotheses target four distinct dimensions of the lyrical archive:

1. **Where is the world?** (H1, territory)
2. **What happens at the world's edge?** (H2, displacement)
3. **What is the rhetorical economy of conflict?** (H3, resistance vs victimhood)
4. **How are subjects gendered?** (H4, gender positional configuration)

The four can be computed independently and are not mutually constraining. The current article (v19e) develops H2 and H4 because those are the dimensions where the empirical findings most clearly support an articulable analytical claim. H1 and H3 produced null results that did not warrant a separate analytical thread in this paper.

## Why dictionary-based methods rather than embeddings

At the scale of this corpus (61 tracks, ~6,300 lemmas), word embedding methods and transformer-based topic modelling are not appropriate. These methods are calibrated for corpora typically above 100,000 tracks (cf. Betti, Abrate, & Kaltenbrunner 2023; Chen et al. 2024). At small corpus scale, dictionary-based methods with manual verification offer:

— Higher transparency of analytical decisions
— Better accuracy through manual verification of every flagged hit
— Direct interpretability — every hit can be traced back to a specific lemma in a specific track
— Replicability — the dictionaries are explicit and shared

This methodological choice is justified at length in §2.3 of the article and follows the precedent established by Werner & Ledermann (2024) for country music, by Karjus (2025) on machine-assisted quantitizing more generally, and by the corpus methodology tradition documented in Baker (2006) and Bednarek (2018).

## Manual verification

All KWIC hits flagged by the pipeline were manually verified by the author before inclusion in the analysis. The verification is documented in `corpus/verification/gender_verification_report.md` and the per-occurrence CSV. Manual verification is integral to the methodology — the published counts are the verified counts, not the raw pipeline output.

For tracks where the pipeline flagged hits and the manual review excluded them as false positives, the report records the exclusion decision. Notable example: the four occurrences of `virgin` in *Pisces* (King of Everything 2016) function as adjectival modifiers of `innocence` and were excluded from the social-conventional noun count.

## What this methodology cannot do

— Capture musical or sonic dimensions. The analysis is textual.
— Adjudicate questions of lyrical meaning that depend on metric, melodic, or vocal performance considerations.
— Determine the intentions of the songwriter or the band.
— Capture tokens in Russian or Ukrainian (~ 1.7% of the corpus). This limitation is addressed in §4.4 of the article.

## What this methodology CAN do

— Track quantitative trends across the diachronic trajectory.
— Identify lexical concentrations that constitute analytical anchors.
— Quantify syntactic role distributions for tokens marked by analytically-defined categories.
— Produce a textual surface that can be read against the band's public discourse and against external categorical framings.

## Inferential statistics

The analysis pre-registered an exploratory significance threshold of α = 0.10 (the rationale is given in §2.3 of the article). H1 and H3 used Spearman rank correlation between metric and year. H2 used Welch's t-test (Duél vs rest, per-track). H4 was descriptive.

Three of the four hypotheses tested as null (H1, H2, H3). The article reports H2's null result transparently and uses the track-level outlier as the empirical anchor of the analytical narrative. H1 and H3 are not developed in the current paper but their pipeline output is preserved.

## AI disclosure

The pipeline includes manual verification, dictionary construction, and analytical interpretation steps that depend on the author's expertise. Some pipeline-internal text processing operations (lemmatisation via spaCy, dependency parsing, syntactic role assignment) are deterministic computational operations. The article's AI disclosure (§2.3) discloses any LLM-assisted operations elsewhere in the analytical process and follows the methodological framework articulated in Karjus (2025).
