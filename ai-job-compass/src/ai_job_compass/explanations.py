from typing import List, Dict

import pandas as pd

from .data_loader import load_role_skills, load_skills, load_roles


def explain_recommendation(
    role_id: int, user_skill_ids: List[int], top_k: int = 3
) -> Dict[str, object]:
    """
    Return a dict with:
      - role_name
      - matched_skills: top-k skills you already have that matter for this role
      - missing_skills: top-k missing important skills
    """
    role_skills = load_role_skills()
    skills = load_skills().set_index("skill_id")
    roles = load_roles().set_index("role_id")

    role_name = roles.loc[role_id, "name"]

    rs = role_skills[role_skills["role_id"] == role_id].copy()
    rs["has_skill"] = rs["skill_id"].isin(user_skill_ids)

    matched = (
        rs[rs["has_skill"]]
        .merge(skills[["name"]], left_on="skill_id", right_index=True)
        .sort_values("importance", ascending=False)
        .head(top_k)
    )

    missing = (
        rs[~rs["has_skill"]]
        .merge(skills[["name"]], left_on="skill_id", right_index=True)
        .sort_values("importance", ascending=False)
        .head(top_k)
    )

    matched_list = matched[["name", "importance"]].to_dict(orient="records")
    missing_list = missing[["name", "importance"]].to_dict(orient="records")

    return {
        "role_name": role_name,
        "matched_skills": matched_list,
        "missing_skills": missing_list,
    }
