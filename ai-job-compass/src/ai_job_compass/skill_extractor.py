from typing import Set
import re

import pandas as pd


def build_skill_lexicon(skills_df: pd.DataFrame) -> dict:
    """Map normalized name variants -> skill_id."""
    lexicon = {}
    for sid, row in skills_df.iterrows():
        name = str(row["name"]).strip().lower()
        variants = {name}
        # variations: remove punctuation, normalize spaces, no-space
        variants.add(re.sub(r"[^a-z0-9]+", " ", name).strip())
        variants.add(name.replace(" ", ""))
        for v in variants:
            if not v:
                continue
            lexicon[v] = sid
    return lexicon


def extract_skills_from_text(text: str, skills_df: pd.DataFrame) -> Set[int]:
    """Return a set of skill_ids detected in text."""
    if not text:
        return set()
    text_norm = re.sub(r"[^a-z0-9]+", " ", text.lower())
    tokens = set(text_norm.split())
    lexicon = build_skill_lexicon(skills_df)
    found = set()
    for variant, sid in lexicon.items():
        parts = variant.split()
        if len(parts) == 1:
            if variant in tokens:
                found.add(sid)
        else:
            if variant in text_norm:
                found.add(sid)
    return found
