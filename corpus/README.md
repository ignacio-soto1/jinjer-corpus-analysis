# corpus/

Track metadata, the reconstruction script, and verification artefacts for the local lyrical corpus.

## Contents

— **`metadata.csv`** — metadata for the 61 tracks across 7 studio releases (2012–2025) in the format the pipeline directly consumes. Columns: filename, album, year, track_number, title, language. **No lyrics are stored here.**

— **`build_corpus.py`** — reconstruction script. Reads `metadata.csv` and a user-provided sources directory containing the user's own legal copies of lyrics, and produces the local corpus structure that the pipeline expects.

— **`local/`** — destination of the reconstruction script. Gitignored. Will contain 61 .txt files in seven subdirectories after reconstruction.

— **`verification/`** — manual verification logs from the author's analytical pass. The `gender_verification.csv` records per-occurrence decisions; the `gender_verification_report.md` is the narrative report.

## Why no lyrics are distributed

Lyrics are intellectual property of the band Jinjer and their publishers. This repository distributes only what is the author's own intellectual contribution: track metadata, the analysis pipeline, the embedded dictionaries, the aggregated quantitative outputs, and the verification artefacts. Reconstructing the local corpus requires the user to assemble lyric files from sources they themselves license.

## Filename convention

The pipeline expects this directory layout:

```
corpus/
└── local/
    ├── 01_inhale_2012/
    │   ├── 01_until_the_end.txt
    │   ├── 02_waltz.txt
    │   ├── 03_scissors.txt
    │   ├── 04_exposed_as_a_liar.txt
    │   ├── 05_my_lost_chance.txt
    │   ├── 06_hypocrites_critics.txt
    │   ├── 07_objects_in_mirror_are_closer_than_they_appear.txt
    │   └── 08_destroy_live.txt
    ├── 02_cloud_factory_2014/
    │   └── ... (8 tracks)
    ├── 03_king_of_everything_2016/
    │   └── ... (10 tracks)
    ├── 04_micro_2019/
    │   └── ... (4 tracks)
    ├── 05_macro_2019/
    │   └── ... (9 tracks)
    ├── 06_wallflowers_2021/
    │   └── ... (11 tracks)
    └── 07_duel_2025/
        └── ... (11 tracks)
```

Total: **61 tracks**. The full mapping (filename → metadata) is in `metadata.csv`.

## How to assemble your sources

The `build_corpus.py` script accepts a directory containing `.txt` files in any subdirectory structure. The script searches recursively for `.txt` files and matches each candidate to a metadata entry by:

1. Exact filename match (e.g., `01_until_the_end.txt`)
2. Stem match (the part before `.txt`)
3. Normalised title match (lowercased, alphanumeric-only, normalised whitespace)

Sources from which lyrics can be legally obtained include, but are not limited to:

— Lyrics websites that hold appropriate licensing (LyricFind, Musixmatch). Most provide programmatic access only via paid API.
— Genius.com — community-contributed transcriptions, accessible programmatically with their API. Review Genius's terms for analytical reuse.
— Official band channels — physical CD/LP album booklets and Bandcamp digital releases the user has purchased.
— Streaming platforms with synced-lyrics support (Spotify, Apple Music) when the user has an active subscription. Note these typically do not permit bulk export.

The repository takes no position on which source the user chooses. The reconstruction script is source-agnostic.

## A note on Cloud Factory 2018 reissue

The 2018 reissue of Cloud Factory by Napalm Records contains two additional bonus tracks ("A Plus or a Minus (Live from Sentrum)" and "Who Is Gonna Be the One (Live from Atlas)") which are live versions of tracks already in the studio corpus. These live versions are **not included** in the 61-track corpus because they are re-performances, not original lyrical content.

## A note on language

60 of the 61 tracks are primarily in English. Cloud Factory 2014 track 8, "Zhelayu Znachit Poluchu" (Желаю значит получу), is in Russian. The pipeline records this in `outputs/language_proportions.csv` as Cloud Factory being 87.5% English and 12.5% Russian. The Russian track is excluded from the English lemma analysis but counts in the corpus aggregate.

## After reconstruction

After running `build_corpus.py`, the directory `corpus/local/` should contain 61 `.txt` files distributed across the 7 album subdirectories. The pipeline will warn about any missing files and still process the available tracks.
