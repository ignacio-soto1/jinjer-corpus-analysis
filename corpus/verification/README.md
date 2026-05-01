# corpus/verification/

Manual verification artefacts produced by the author during the analytical pass. These documents support the methodological transparency claim in §2.3 of the manuscript and substantiate the AI disclosure: every automatically flagged hit was reviewed by the author against the full track context before inclusion in the analysis.

## Files

— **`gender_verification.csv`** — table of every gender-related hit detected by the pipeline across the 61 tracks of the corpus, with manual verification decisions per occurrence. Columns include album, track, line number, lemma, automated classification, manual decision, and notes.

— **`gender_verification_report.md`** — narrative report of the verification process. Documents:
  - Which tracks contain feminine social-conventional nouns (only 2 hits across 61 tracks: `lady` in *Teacher Teacher*, `ladies` in *Tantrum*).
  - Which track contains an explicit first-person feminine enunciator (only *Someone's Daughter* in Duél 2025, via three uses of `daughter` and one general use of `woman`).
  - Which tracks contain explicit first-person masculine enunciators (none under strict criteria — the apparent masculine references function as third-person, vocative, addressee, generic question, or ambiguous figure, but never as unequivocal self-marking of the lyrical I).
  - Disambiguation decisions for ambiguous cases (e.g., the four occurrences of `virgin` in *Pisces* that function adjectivally as modifiers of `innocence` and are therefore excluded from the social-conventional noun count).
  - Per-track summary table covering all 61 tracks.

## Why this verification matters analytically

The verification report grounds three central claims of the manuscript:

1. **The 16 vs 2 asymmetry in social-conventional gendered nouns is empirically documented**, not asserted. The masculine count is dominated by `king` (14 of 16 occurrences) concentrated in two tracks of *King of Everything* (2016). The feminine count consists of `lady` and `ladies`, both peripheral.

2. **The unique status of *Someone's Daughter*** as the only track with an explicit first-person feminine enunciator across 13 years of discography. The verification confirms this finding pista by pista.

3. **The absence of self-marking masculine enunciators**. The verification shows that masculine references (`man`, `men`, `son`, `brother`) function consistently in non-self-marking grammatical positions — third-person, vocative, addressee, generic. This is the empirical counterpart of the article's claim about symbolic vacancy.

## Format

The CSV is the machine-readable record. The Markdown report is the narrative explanation, intended for human readers (referees, replicators) who want to understand the verification process without parsing the CSV.

Both documents preserve the no-lyrics policy of this repository: lemma occurrences are recorded with track and line number, never with verbatim lyric text.
