#!/usr/bin/env python3
"""
build_corpus.py

Reconstruction script for the local lyrical corpus required by the analysis
pipeline. This script does NOT contain or distribute lyrics. It expects the
user to have prepared a directory of lyric files from sources they themselves
licence, and produces the canonical filename layout that the pipeline expects.

Filename convention required by the pipeline:
    corpus/local/{NN_album_YYYY}/{NN_track_title.txt}

Example:
    corpus/local/01_inhale_2012/01_until_the_end.txt
    corpus/local/07_duel_2025/05_tumbleweed.txt

The full mapping is in corpus/metadata.csv.

Usage:
    python corpus/build_corpus.py --sources-dir /path/to/your/sources

The user is fully responsible for the legality of their sources directory
under their own jurisdiction's copyright law.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = REPO_ROOT / "corpus"
METADATA_PATH = CORPUS_DIR / "metadata.csv"
LOCAL_CORPUS_DIR = CORPUS_DIR / "local"


@dataclass
class Track:
    filename: str       # e.g. "01_inhale_2012/01_until_the_end.txt" — pipeline expects this
    album: str
    year: int
    track_number: int
    title: str
    language: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Track":
        return cls(
            filename=row["filename"],
            album=row["album"],
            year=int(row["year"]),
            track_number=int(row["track_number"]),
            title=row["title"],
            language=row["language"],
        )


def load_metadata(path: Path) -> list[Track]:
    if not path.exists():
        sys.exit(f"ERROR: metadata not found at {path}")
    tracks: list[Track] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            tracks.append(Track.from_row(row))
    if len(tracks) != 61:
        print(
            f"WARNING: metadata contains {len(tracks)} tracks; "
            f"the analysis was conducted on a corpus of 61 tracks.",
            file=sys.stderr,
        )
    return tracks


def normalise_title(title: str) -> str:
    """Normalise a title for matching against filenames."""
    title = title.lower()
    title = re.sub(r"[^a-z0-9 ]+", " ", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def find_match(track: Track, candidates: list[Path]) -> Path | None:
    """Find a source file for a given track in the user's sources directory.

    Matching strategy is permissive: tries to match by canonical filename
    first, then by track_number-album combination, then by normalised title.
    """
    target_canonical = Path(track.filename).name  # e.g. "01_until_the_end.txt"
    target_title = normalise_title(track.title)
    target_basename = Path(track.filename).stem  # e.g. "01_until_the_end"

    # Strategy 1: filename matches the canonical form already
    canonical_matches = [c for c in candidates if c.name == target_canonical]
    if len(canonical_matches) == 1:
        return canonical_matches[0]

    # Strategy 2: stem of file matches canonical stem
    stem_matches = [c for c in candidates if c.stem == target_basename]
    if len(stem_matches) == 1:
        return stem_matches[0]

    # Strategy 3: normalised title in filename
    title_matches = [
        c for c in candidates if target_title in normalise_title(c.stem)
    ]
    if len(title_matches) == 1:
        return title_matches[0]
    if len(title_matches) > 1:
        print(
            f"  AMBIGUOUS: multiple files match title for '{track.title}' "
            f"({', '.join(p.name for p in title_matches)}). Skipping.",
            file=sys.stderr,
        )
        return None

    return None


def reconstruct_corpus(
    tracks: list[Track],
    sources_dir: Path,
    target_dir: Path,
    *,
    dry_run: bool = False,
) -> tuple[int, list[Track]]:
    """Reconstruct the local corpus from the user's sources directory.

    Returns: (n_matched, missing_tracks)
    """
    if not sources_dir.is_dir():
        sys.exit(f"ERROR: sources directory not found: {sources_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)

    candidate_files = sorted(
        p for p in sources_dir.rglob("*.txt") if p.is_file()
    )
    if not candidate_files:
        sys.exit(
            f"ERROR: no .txt files found in {sources_dir}. "
            f"Place one .txt per track in this directory before running."
        )

    print(f"Found {len(candidate_files)} candidate .txt files in {sources_dir}")
    print(f"Matching against {len(tracks)} tracks from metadata.csv ...")
    print()

    matched = 0
    missing: list[Track] = []
    for track in tracks:
        match = find_match(track, candidate_files)
        if match is None:
            missing.append(track)
            print(f"  [{track.filename}] MISSING: '{track.title}'")
            continue

        # Construct target path: LOCAL_CORPUS_DIR / track.filename
        target = target_dir / track.filename
        target.parent.mkdir(parents=True, exist_ok=True)

        if dry_run:
            print(f"  [{track.filename}] would copy {match.name} -> {track.filename}")
        else:
            shutil.copy2(match, target)
            print(f"  [{track.filename}] {match.name} -> {track.filename}")
        matched += 1

    return matched, missing


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct the local lyrical corpus from user-provided sources. "
            "Does not download or distribute lyrics."
        )
    )
    parser.add_argument(
        "--sources-dir",
        required=True,
        type=Path,
        help="Directory containing one .txt file per track (user-licensed).",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=LOCAL_CORPUS_DIR,
        help=f"Target directory for the reconstructed corpus (default: {LOCAL_CORPUS_DIR}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report matches without copying any files.",
    )
    args = parser.parse_args(argv)

    print(f"Metadata: {METADATA_PATH}")
    print(f"Sources: {args.sources_dir}")
    print(f"Target: {args.target_dir}")
    print(f"Dry run: {args.dry_run}")
    print()

    tracks = load_metadata(METADATA_PATH)
    matched, missing = reconstruct_corpus(
        tracks, args.sources_dir, args.target_dir, dry_run=args.dry_run
    )

    print()
    print(f"Result: {matched} of {len(tracks)} tracks reconstructed.")
    if missing:
        print(f"Missing {len(missing)} tracks. The pipeline will warn but continue.")
        print("Add these source files and re-run if you want full coverage:")
        for t in missing:
            print(f"  - {t.filename}: '{t.title}' ({t.album}, {t.year})")
        return 1
    print("Local corpus is complete. Pipeline can now be run:")
    print("  python pipeline/process_corpus_discourse_v3.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
