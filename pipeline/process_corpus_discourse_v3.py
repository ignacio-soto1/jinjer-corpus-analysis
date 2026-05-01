"""
Jinjer Lyrical Corpus — Discourse Analysis Pipeline (v3)
=========================================================

Author: [Author name and affiliation removed for double-anonymised peer review]
        With AI-assisted code development (LLM-collaborative implementation
        of dictionary search, dependency parsing, and aggregation routines).
Version: 3.0 — Adds gender layer (H4) on top of v2 dictionaries.

CHANGES FROM v2
---------------
v2 calibrated five lexical dictionaries to the actual vocabulary of the corpus.
v3 adds a fourth analytical dimension (H4) operationalized through:

  (a) Lexical categories of gender-marked subjects:
      - pronouns (she/her vs he/him)
      - relational nouns (mother/daughter vs father/son)
      - age-gender nouns (woman/girl vs man/boy)
      - social nouns by lexical convention (queen, lady vs king, gentleman)
      - social nouns assigned contextually via coreference heuristic
        (teacher, soldier, leader: assigned gender if a coreferent gendered
         pronoun appears in the same or following sentence; otherwise
         tagged 'unknown')

  (b) Syntactic position of each gendered mention:
      - agent (nsubj)
      - patient (nsubjpass, dobj, pobj, iobj)
      - other (remaining grammatical roles)

  (c) Track- and album-level metrics:
      - total gender-marking density (per 100 lemmas)
      - proportions feminine vs masculine vs unknown
      - agent ratio per gender
      - patient ratio per gender

H4 is exploratory (no directional prediction). It documents how gender-marked
subjects distribute across the discography, in dialogue with Burns (2023)
which addressed female subjectivities in Jinjer videoclips through
multimodal-qualitative analysis. The present analysis offers a corpus-wide
quantitative complement.
"""

import re
from pathlib import Path
from collections import Counter
from typing import Dict, List, Optional

import pandas as pd
import numpy as np
import spacy
from langdetect import detect, DetectorFactory
from scipy import stats

DetectorFactory.seed = 42

# =============================================================================
# CONFIGURATION
# =============================================================================
# Paths assume the script is run from the repository root:
#     python pipeline/process_corpus_discourse_v3.py
# The local corpus is reconstructed by the user via corpus/build_corpus.py.

CORPUS_ROOT = Path("./corpus")
LYRICS_DIR = CORPUS_ROOT / "local"
METADATA_PATH = CORPUS_ROOT / "metadata.csv"
OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / "stats").mkdir(exist_ok=True)

nlp = spacy.load("en_core_web_sm")


# =============================================================================
# DICTIONARIES v2 (unchanged from v2)
# =============================================================================

DICT_TERRITORY_CONCRETE = {
    "border", "frontier", "country", "nation", "state", "empire",
    "land", "soil", "ground", "earth", "territory", "region",
    "factory", "mine", "field", "city", "town", "village",
    "east", "west", "north", "south",
    "flag", "anthem", "passport",
    "motherland", "home", "house", "shack", "shelter", "roof",
    "world", "street", "yard",
}

DICT_TERRITORY_METAPHORICAL = {
    "void", "emptiness", "nowhere", "elsewhere",
    "hollow", "abyss", "depth", "shadow",
    "dream", "memory", "mirror", "reflection",
    "within", "inside", "inner", "deep",
}

DICT_DISPLACEMENT = {
    "refugee", "exile", "exiled", "displaced", "displacement",
    "fleeing", "flee", "fled", "escape", "escaped",
    "scatter", "scattered", "diaspora",
    "uprooted", "uproot", "replanted", "wilted", "debris",
    "homeless", "tumbleweed", "rolling", "roaming",
    "stranger", "stateless", "wandering", "wanderer",
}
# v3.1: 'scatter' added alongside 'scattered' to close a lemmatizer-driven
# brittleness. spaCy ≥3.5 lemmatizes 'scattered' (used adjectivally) to
# 'scatter' as VERB. Without the base form, the Colossus match
# ('the scattered bones') is lost. Earlier runs that produced the published
# Colossus density of 1.099/100 used a less aggressive POS-aware lemmatizer.

DICT_RESISTANCE = {
    "stand", "standing", "rise", "rising", "fight", "fighting",
    "resist", "resisting", "refuse", "refusing",
    "hold", "won't",
    "alive", "strong", "strength", "last", "tall",
}

DICT_VICTIMHOOD = {
    "broken", "shattered", "crushed", "destroyed",
    "helpless", "powerless", "weak", "fragile",
    "fall", "falling", "fallen", "drown", "drowning",
    "suffer", "suffering", "pain", "wound", "wounded", "scarred",
    "bleed", "bleeding", "die", "dying", "dead",
    "agony", "bile", "blood",
}


# =============================================================================
# H4: GENDER MARKING — lexical categories
# =============================================================================

PRONOUNS_FEM = {"she", "her", "hers", "herself"}
PRONOUNS_MASC = {"he", "him", "his", "himself"}

NOUNS_RELATIONAL_FEM = {
    "mother", "daughter", "sister", "wife",
    "mom", "mommy", "mama", "grandma", "grandmother",
    "aunt", "niece",
}
NOUNS_RELATIONAL_MASC = {
    "father", "son", "brother", "husband",
    "dad", "daddy", "papa", "grandpa", "grandfather",
    "uncle", "nephew",
}
NOUNS_RELATIONAL_NEUTRAL = {
    "child", "children", "parent", "parents", "sibling", "siblings",
    "spouse", "partner",
}

NOUNS_AGE_GENDER_FEM = {"girl", "woman", "women", "lady", "ladies"}
NOUNS_AGE_GENDER_MASC = {"boy", "man", "men", "gentleman", "gentlemen", "guy", "guys"}

NOUNS_SOCIAL_FEM_BY_CONVENTION = {
    "queen", "princess", "duchess", "mistress",
    "witch", "goddess", "heroine", "empress",
    "nun", "priestess",
}
NOUNS_SOCIAL_MASC_BY_CONVENTION = {
    "king", "prince", "duke", "master",
    "wizard", "god", "hero", "emperor",
    "monk", "priest", "lord",
}

# Social/professional nouns whose gender depends on context (coreference)
NOUNS_SOCIAL_CONTEXTUAL = {
    "teacher", "soldier", "doctor", "nurse",
    "leader", "ruler", "president", "minister",
    "judge", "captain", "warrior", "fighter",
    "preacher", "saint", "stranger",
    "outsider", "outlander",
    "friend", "enemy",
}

# All gender-marking lemmas (for total density)
ALL_GENDERED = (
    PRONOUNS_FEM | PRONOUNS_MASC
    | NOUNS_RELATIONAL_FEM | NOUNS_RELATIONAL_MASC | NOUNS_RELATIONAL_NEUTRAL
    | NOUNS_AGE_GENDER_FEM | NOUNS_AGE_GENDER_MASC
    | NOUNS_SOCIAL_FEM_BY_CONVENTION | NOUNS_SOCIAL_MASC_BY_CONVENTION
    | NOUNS_SOCIAL_CONTEXTUAL
)


# =============================================================================
# CORE TEXT PROCESSING
# =============================================================================

def read_lyric_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def normalize_text(text: str) -> str:
    text = re.sub(r"\[.*?\]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def lemmatize_tokens(text: str) -> List[str]:
    doc = nlp(text)
    return [
        token.lemma_.lower()
        for token in doc
        if not token.is_punct and not token.is_space and not token.is_stop
        and token.is_alpha and len(token.lemma_) > 1
    ]


def dictionary_frequency(lemmas: List[str], dictionary: set) -> Dict:
    total = len(lemmas)
    if total == 0:
        return {"abs": 0, "per100": 0.0, "unique_hits": 0}
    matches = [l for l in lemmas if l in dictionary]
    return {
        "abs": len(matches),
        "per100": 100 * len(matches) / total,
        "unique_hits": len(set(matches)),
    }


# =============================================================================
# H3: SYNTACTIC PROXIES (unchanged from v2)
# =============================================================================

def syntactic_proxies(text: str) -> Dict:
    doc = nlp(text)
    tokens = [t for t in doc if not t.is_punct and not t.is_space]

    passive_clauses = sum(1 for t in doc if t.dep_ in {"nsubjpass", "auxpass"})
    total_clauses = sum(1 for t in doc if t.dep_ in {"nsubj", "nsubjpass"})
    passive_ratio = passive_clauses / total_clauses if total_clauses else 0

    first_person_pronouns = {"i", "we", "me", "us", "my", "our", "myself", "ourselves"}
    fp_agent = fp_patient = fp_total = 0
    for t in doc:
        if t.text.lower() in first_person_pronouns:
            fp_total += 1
            if t.dep_ in {"nsubj"}:
                fp_agent += 1
            elif t.dep_ in {"dobj", "pobj", "iobj"}:
                fp_patient += 1

    fp_agent_ratio = fp_agent / fp_total if fp_total else 0
    fp_patient_ratio = fp_patient / fp_total if fp_total else 0

    lemmas_lower = [t.lemma_.lower() for t in doc if t.is_alpha]
    n_lemmas = max(len(lemmas_lower), 1)
    resistance_ratio = sum(1 for l in lemmas_lower if l in DICT_RESISTANCE) / n_lemmas * 100
    victimhood_ratio = sum(1 for l in lemmas_lower if l in DICT_VICTIMHOOD) / n_lemmas * 100

    return {
        "passive_ratio": round(passive_ratio, 4),
        "fp_agent_ratio": round(fp_agent_ratio, 4),
        "fp_patient_ratio": round(fp_patient_ratio, 4),
        "fp_total": fp_total,
        "resistance_per100": round(resistance_ratio, 4),
        "victimhood_per100": round(victimhood_ratio, 4),
    }


# =============================================================================
# H4: GENDER POSITIONAL ANALYSIS
# =============================================================================

def classify_lemma_gender(lemma: str) -> Optional[str]:
    """Return 'fem', 'masc', 'neutral', 'contextual', or None for non-gendered."""
    if lemma in PRONOUNS_FEM: return "fem"
    if lemma in PRONOUNS_MASC: return "masc"
    if lemma in NOUNS_RELATIONAL_FEM: return "fem"
    if lemma in NOUNS_RELATIONAL_MASC: return "masc"
    if lemma in NOUNS_RELATIONAL_NEUTRAL: return "neutral"
    if lemma in NOUNS_AGE_GENDER_FEM: return "fem"
    if lemma in NOUNS_AGE_GENDER_MASC: return "masc"
    if lemma in NOUNS_SOCIAL_FEM_BY_CONVENTION: return "fem"
    if lemma in NOUNS_SOCIAL_MASC_BY_CONVENTION: return "masc"
    if lemma in NOUNS_SOCIAL_CONTEXTUAL: return "contextual"
    return None


def classify_dep_position(dep: str) -> str:
    """Classify dependency role into agent / patient / other."""
    if dep == "nsubj":
        return "agent"
    elif dep in {"nsubjpass", "dobj", "pobj", "iobj"}:
        return "patient"
    else:
        return "other"


def assign_contextual_gender(token, doc) -> str:
    """For NOUNS_SOCIAL_CONTEXTUAL, look for a coreferent gendered pronoun in
    the same sentence or the following sentence. Heuristic — not full
    coreference resolution.
    Returns 'fem', 'masc', or 'unknown'.
    """
    sent = token.sent
    sent_idx = list(doc.sents).index(sent)
    sentences = list(doc.sents)
    search_sentences = [sent]
    if sent_idx + 1 < len(sentences):
        search_sentences.append(sentences[sent_idx + 1])

    fem_count = 0
    masc_count = 0
    for s in search_sentences:
        for t in s:
            if t.lemma_.lower() in PRONOUNS_FEM:
                fem_count += 1
            elif t.lemma_.lower() in PRONOUNS_MASC:
                masc_count += 1

    if fem_count > masc_count and fem_count > 0:
        return "fem"
    elif masc_count > fem_count and masc_count > 0:
        return "masc"
    else:
        return "unknown"


def gender_positional_analysis(text: str) -> Dict:
    """Full H4 analysis for one track."""
    doc = nlp(text)
    n_lemmas = sum(1 for t in doc if t.is_alpha)

    # Counts: gender × position
    counts = {
        "fem_agent": 0, "fem_patient": 0, "fem_other": 0,
        "masc_agent": 0, "masc_patient": 0, "masc_other": 0,
        "neutral_agent": 0, "neutral_patient": 0, "neutral_other": 0,
        "unknown_agent": 0, "unknown_patient": 0, "unknown_other": 0,
        "fem_pron": 0, "masc_pron": 0,
        "fem_relational": 0, "masc_relational": 0, "neutral_relational": 0,
        "fem_age": 0, "masc_age": 0,
        "fem_social_conv": 0, "masc_social_conv": 0,
        "contextual_assigned_fem": 0, "contextual_assigned_masc": 0,
        "contextual_unknown": 0,
        "total_gendered_mentions": 0,
    }

    for token in doc:
        lemma = token.lemma_.lower()
        gender_class = classify_lemma_gender(lemma)
        if gender_class is None:
            continue

        # Resolve contextual to fem/masc/unknown
        if gender_class == "contextual":
            resolved = assign_contextual_gender(token, doc)
            if resolved == "unknown":
                counts["contextual_unknown"] += 1
                effective_gender = "unknown"
            elif resolved == "fem":
                counts["contextual_assigned_fem"] += 1
                effective_gender = "fem"
            else:
                counts["contextual_assigned_masc"] += 1
                effective_gender = "masc"
        else:
            effective_gender = gender_class  # fem / masc / neutral

        counts["total_gendered_mentions"] += 1

        # Lexical category counters
        if lemma in PRONOUNS_FEM:
            counts["fem_pron"] += 1
        elif lemma in PRONOUNS_MASC:
            counts["masc_pron"] += 1
        elif lemma in NOUNS_RELATIONAL_FEM:
            counts["fem_relational"] += 1
        elif lemma in NOUNS_RELATIONAL_MASC:
            counts["masc_relational"] += 1
        elif lemma in NOUNS_RELATIONAL_NEUTRAL:
            counts["neutral_relational"] += 1
        elif lemma in NOUNS_AGE_GENDER_FEM:
            counts["fem_age"] += 1
        elif lemma in NOUNS_AGE_GENDER_MASC:
            counts["masc_age"] += 1
        elif lemma in NOUNS_SOCIAL_FEM_BY_CONVENTION:
            counts["fem_social_conv"] += 1
        elif lemma in NOUNS_SOCIAL_MASC_BY_CONVENTION:
            counts["masc_social_conv"] += 1

        # Position × effective gender
        pos = classify_dep_position(token.dep_)
        key = f"{effective_gender}_{pos}"
        if key in counts:
            counts[key] += 1

    # Normalize key metrics
    n_lemmas_safe = max(n_lemmas, 1)
    total = max(counts["total_gendered_mentions"], 1)

    metrics = {
        # Density
        "h4_total_gendered_per100": round(100 * counts["total_gendered_mentions"] / n_lemmas_safe, 4),
        # Lexical category proportions
        "h4_fem_pron_per100": round(100 * counts["fem_pron"] / n_lemmas_safe, 4),
        "h4_masc_pron_per100": round(100 * counts["masc_pron"] / n_lemmas_safe, 4),
        "h4_fem_relational_per100": round(100 * counts["fem_relational"] / n_lemmas_safe, 4),
        "h4_masc_relational_per100": round(100 * counts["masc_relational"] / n_lemmas_safe, 4),
        "h4_fem_social_conv_per100": round(100 * counts["fem_social_conv"] / n_lemmas_safe, 4),
        "h4_masc_social_conv_per100": round(100 * counts["masc_social_conv"] / n_lemmas_safe, 4),
        # Gender ratio (out of total fem+masc mentions, excluding neutral and unknown)
        "h4_fem_masc_ratio": round(
            (counts["fem_pron"] + counts["fem_relational"] + counts["fem_age"]
             + counts["fem_social_conv"] + counts["contextual_assigned_fem"])
            / max(1, counts["fem_pron"] + counts["fem_relational"] + counts["fem_age"]
                  + counts["fem_social_conv"] + counts["contextual_assigned_fem"]
                  + counts["masc_pron"] + counts["masc_relational"] + counts["masc_age"]
                  + counts["masc_social_conv"] + counts["contextual_assigned_masc"]),
            4
        ),
        # Positional metrics by gender
        "h4_fem_agent_ratio": round(counts["fem_agent"] /
            max(1, counts["fem_agent"] + counts["fem_patient"] + counts["fem_other"]), 4),
        "h4_fem_patient_ratio": round(counts["fem_patient"] /
            max(1, counts["fem_agent"] + counts["fem_patient"] + counts["fem_other"]), 4),
        "h4_masc_agent_ratio": round(counts["masc_agent"] /
            max(1, counts["masc_agent"] + counts["masc_patient"] + counts["masc_other"]), 4),
        "h4_masc_patient_ratio": round(counts["masc_patient"] /
            max(1, counts["masc_agent"] + counts["masc_patient"] + counts["masc_other"]), 4),
        # Coverage (how many contextual nouns could be resolved)
        "h4_contextual_unresolved": counts["contextual_unknown"],
        "h4_contextual_resolved_fem": counts["contextual_assigned_fem"],
        "h4_contextual_resolved_masc": counts["contextual_assigned_masc"],
        # Raw absolute counts (useful for low-frequency tracks)
        "h4_n_fem_total": (counts["fem_pron"] + counts["fem_relational"] + counts["fem_age"]
                          + counts["fem_social_conv"] + counts["contextual_assigned_fem"]),
        "h4_n_masc_total": (counts["masc_pron"] + counts["masc_relational"] + counts["masc_age"]
                           + counts["masc_social_conv"] + counts["contextual_assigned_masc"]),
        "h4_n_neutral_total": counts["neutral_relational"],
        "h4_total_mentions": counts["total_gendered_mentions"],
    }
    return metrics


# =============================================================================
# TRACK-LEVEL PROCESSING
# =============================================================================

def process_track(filepath: Path, metadata_row: pd.Series) -> Dict:
    raw = read_lyric_file(filepath)
    cleaned = normalize_text(raw)
    declared_lang = metadata_row.get("language", "en")

    record = {
        "filename": metadata_row["filename"],
        "album": metadata_row["album"],
        "year": int(metadata_row["year"]),
        "track_number": metadata_row.get("track_number"),
        "title": metadata_row["title"],
        "language": declared_lang,
        "char_count": len(cleaned),
    }

    if declared_lang == "en":
        lemmas = lemmatize_tokens(cleaned)
        record["lemma_count"] = len(lemmas)
        record["unique_lemmas"] = len(set(lemmas))
        record["lexical_diversity_ttr"] = (
            len(set(lemmas)) / len(lemmas) if lemmas else 0
        )

        # H1 territorial
        terr_concrete = dictionary_frequency(lemmas, DICT_TERRITORY_CONCRETE)
        terr_metaph = dictionary_frequency(lemmas, DICT_TERRITORY_METAPHORICAL)
        record["h1_territory_concrete_per100"] = terr_concrete["per100"]
        record["h1_territory_metaphorical_per100"] = terr_metaph["per100"]
        record["h1_concrete_metaphorical_ratio"] = (
            terr_concrete["per100"] / terr_metaph["per100"]
            if terr_metaph["per100"] else np.nan
        )

        # H2 displacement
        displacement = dictionary_frequency(lemmas, DICT_DISPLACEMENT)
        record["h2_displacement_per100"] = displacement["per100"]
        record["h2_displacement_unique_hits"] = displacement["unique_hits"]

        # H3 conflict frame
        proxies = syntactic_proxies(cleaned)
        record.update({
            "h3_passive_ratio": proxies["passive_ratio"],
            "h3_fp_agent_ratio": proxies["fp_agent_ratio"],
            "h3_fp_patient_ratio": proxies["fp_patient_ratio"],
            "h3_resistance_per100": proxies["resistance_per100"],
            "h3_victimhood_per100": proxies["victimhood_per100"],
            "h3_fp_total": proxies["fp_total"],
        })

        # H4 gender (NEW)
        gender_metrics = gender_positional_analysis(cleaned)
        record.update(gender_metrics)
    else:
        for col in [
            "lemma_count", "unique_lemmas", "lexical_diversity_ttr",
            "h1_territory_concrete_per100", "h1_territory_metaphorical_per100",
            "h1_concrete_metaphorical_ratio", "h2_displacement_per100",
            "h2_displacement_unique_hits", "h3_passive_ratio",
            "h3_fp_agent_ratio", "h3_fp_patient_ratio",
            "h3_resistance_per100", "h3_victimhood_per100", "h3_fp_total",
            "h4_total_gendered_per100", "h4_fem_pron_per100", "h4_masc_pron_per100",
            "h4_fem_relational_per100", "h4_masc_relational_per100",
            "h4_fem_social_conv_per100", "h4_masc_social_conv_per100",
            "h4_fem_masc_ratio", "h4_fem_agent_ratio", "h4_fem_patient_ratio",
            "h4_masc_agent_ratio", "h4_masc_patient_ratio",
            "h4_contextual_unresolved", "h4_contextual_resolved_fem",
            "h4_contextual_resolved_masc",
            "h4_n_fem_total", "h4_n_masc_total", "h4_n_neutral_total",
            "h4_total_mentions",
        ]:
            record[col] = np.nan

    return record


# =============================================================================
# AGGREGATION & TESTS
# =============================================================================

def aggregate_by_album(track_df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [c for c in track_df.columns
                    if c.startswith(("h1_", "h2_", "h3_", "h4_", "lex"))
                    or c == "lemma_count"]
    agg = track_df.groupby(["album", "year"])[numeric_cols].mean().reset_index()
    agg = agg.sort_values("year")
    return agg


def test_h1(album_df):
    rho_c, p_c = stats.spearmanr(album_df["year"], album_df["h1_territory_concrete_per100"])
    rho_m, p_m = stats.spearmanr(album_df["year"], album_df["h1_territory_metaphorical_per100"])
    return {
        "hypothesis": "H1 — Progressive delocalization",
        "concrete_rho": round(rho_c, 3), "concrete_p": round(p_c, 4),
        "metaphorical_rho": round(rho_m, 3), "metaphorical_p": round(p_m, 4),
        "supported_concrete": rho_c < 0 and p_c < 0.10,
        "supported_metaphorical": rho_m > 0 and p_m < 0.10,
    }


def test_h2(track_df):
    duel = track_df[track_df["album"].str.contains("Duél|Duel", case=False, na=False)]
    rest = track_df[~track_df["album"].str.contains("Duél|Duel", case=False, na=False)]
    duel_vals = duel["h2_displacement_per100"].dropna()
    rest_vals = rest["h2_displacement_per100"].dropna()
    if len(duel_vals) < 2 or len(rest_vals) < 2:
        return {"hypothesis": "H2", "warning": "insufficient data"}
    t, p = stats.ttest_ind(duel_vals, rest_vals, equal_var=False)
    return {
        "hypothesis": "H2 — Post-2022 reactivation",
        "duel_mean": round(duel_vals.mean(), 3),
        "rest_mean": round(rest_vals.mean(), 3),
        "t_statistic": round(t, 3), "p_value": round(p, 4),
        "supported": (duel_vals.mean() > rest_vals.mean()) and p < 0.10,
    }


def test_h3(album_df):
    out = {"hypothesis": "H3 — Conflict frame transformation"}
    for var, expected in [
        ("h3_passive_ratio", "decrease"),
        ("h3_resistance_per100", "increase"),
        ("h3_victimhood_per100", "decrease"),
        ("h3_fp_agent_ratio", "increase"),
    ]:
        rho, p = stats.spearmanr(album_df["year"], album_df[var])
        out[f"{var}_rho"] = round(rho, 3)
        out[f"{var}_p"] = round(p, 4)
        if expected == "decrease":
            out[f"{var}_supported"] = rho < 0 and p < 0.10
        else:
            out[f"{var}_supported"] = rho > 0 and p < 0.10
    return out


def describe_h4(album_df):
    """H4 is exploratory — descriptive summary, not formal test."""
    out = {"hypothesis": "H4 — Gender positional configuration (descriptive)"}
    cols_to_summarize = [
        "h4_total_gendered_per100",
        "h4_fem_pron_per100", "h4_masc_pron_per100",
        "h4_fem_relational_per100", "h4_masc_relational_per100",
        "h4_fem_social_conv_per100", "h4_masc_social_conv_per100",
        "h4_fem_masc_ratio",
        "h4_fem_agent_ratio", "h4_fem_patient_ratio",
        "h4_masc_agent_ratio", "h4_masc_patient_ratio",
    ]
    for col in cols_to_summarize:
        out[f"{col}_mean"] = round(album_df[col].mean(), 4)
        out[f"{col}_min_album"] = album_df.loc[album_df[col].idxmin(), "album"]
        out[f"{col}_max_album"] = album_df.loc[album_df[col].idxmax(), "album"]
    return out


def language_proportion_by_album(track_df):
    counts = track_df.groupby(["album", "year", "language"]).size().unstack(fill_value=0)
    proportions = counts.div(counts.sum(axis=1), axis=0)
    return proportions.reset_index().sort_values("year")


def main():
    print("Loading metadata...")
    metadata = pd.read_csv(METADATA_PATH)
    print(f"  {len(metadata)} tracks declared.")

    print("\nProcessing tracks (v3 — gender layer added)...")
    records = []
    for _, row in metadata.iterrows():
        path = LYRICS_DIR / row["filename"]
        if not path.exists():
            print(f"  WARNING: missing {path}")
            continue
        records.append(process_track(path, row))
    track_df = pd.DataFrame(records)
    print(f"  {len(track_df)} tracks processed.")

    print("\nWriting outputs...")
    track_df.to_csv(OUTPUT_DIR / "track_metrics.csv", index=False)

    album_df = aggregate_by_album(track_df)
    album_df.to_csv(OUTPUT_DIR / "album_metrics.csv", index=False)

    lang_df = language_proportion_by_album(track_df)
    lang_df.to_csv(OUTPUT_DIR / "language_proportions.csv", index=False)

    print("\n=== INFERENTIAL DIAGNOSTICS (v3) ===\n")
    h1 = test_h1(album_df)
    h2 = test_h2(track_df)
    h3 = test_h3(album_df)
    h4 = describe_h4(album_df)
    for r in [h1, h2, h3, h4]:
        print(r)
        print()

    pd.DataFrame([h1, h2, h3]).to_csv(
        OUTPUT_DIR / "hypothesis_tests.csv", index=False
    )
    pd.DataFrame([h4]).to_csv(
        OUTPUT_DIR / "h4_gender_descriptive.csv", index=False
    )

    # Per-album H4 detail table (most useful for the paper)
    h4_album_cols = [c for c in album_df.columns if c.startswith("h4_")]
    album_df[["album", "year"] + h4_album_cols].to_csv(
        OUTPUT_DIR / "h4_gender_album_detail.csv", index=False
    )

    print(f"All outputs saved to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
