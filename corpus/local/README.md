# corpus/local/

**This directory is gitignored.** It is the destination of the corpus reconstruction script (`corpus/build_corpus.py`) and is intended to contain the user's locally-reconstructed lyric files.

## Do not commit anything to this directory

The `.gitignore` at the repository root excludes the entire `corpus/local/` directory except for this README. **Do not** override the gitignore to commit lyric files. The lyrics are intellectual property of the band Jinjer and their publishers.

## Expected structure after reconstruction

After running `python corpus/build_corpus.py --sources-dir /path/to/your/sources`, this directory should contain **seven subdirectories** with **61 lyric files total**:

```
local/
├── 01_inhale_2012/                 (8 .txt files)
├── 02_cloud_factory_2014/          (8 .txt files)
├── 03_king_of_everything_2016/    (10 .txt files)
├── 04_micro_2019/                  (4 .txt files)
├── 05_macro_2019/                  (9 .txt files)
├── 06_wallflowers_2021/           (11 .txt files)
└── 07_duel_2025/                  (11 .txt files)
```

Each `.txt` file contains the lyrics of one track in plain UTF-8 text. The pipeline reads from this directory using the filenames declared in `corpus/metadata.csv`.

## When to delete this directory

When the user is finished with their analysis and is uploading the repository to GitHub or Zenodo, they should:

1. Confirm that `git status` does not show any tracked files under `corpus/local/` (only this README should be tracked).
2. The directory itself can safely be deleted before sharing the repository archive — the gitignore preserves only this README.
