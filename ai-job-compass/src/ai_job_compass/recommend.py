from typing import List

import numpy as np
import pandas as pd

from .data_loader import build_role_skill_matrix, load_role_skills, load_skills
from .job_data import compute_role_demand


def compute_role_scores(
    user_skill_ids: List[int],
    alpha: float = 0.55,
    beta: float = 0.35,
    gamma: float = 0.10,
) -> pd.DataFrame:
    """
    Compute a score for each role given user skills.

    score = alpha * similarity
            + beta * demand_norm
            - gamma * ai_risk_norm

    demand_norm comes from job_postings.
    """
    roles_df, skills_df, mat = build_role_skill_matrix()

    # user vector
    user_vec = np.zeros(mat.shape[1], dtype=float)
    skill_index = {sid: i for i, sid in enumerate(skills_df.index)}
    for sid in user_skill_ids:
        if sid in skill_index:
            user_vec[skill_index[sid]] = 1.0

    # cosine similarity
    role_norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-8
    user_norm = np.linalg.norm(user_vec) + 1e-8
    sims = (mat @ user_vec) / (role_norms[:, 0] * user_norm)

    # demand & salaries
    demand = compute_role_demand()  # indexed by role_id
    combined = roles_df.join(demand, how="left")

    combined["demand_count"].fillna(0, inplace=True)
    combined["demand_norm"].fillna(0, inplace=True)
    combined["avg_salary"].fillna(0, inplace=True)

    demand_norm = combined["demand_norm"].values
    ai_risk = combined["ai_risk_score"].values

    # normalize risk to [0,1]
    risk_norm = ai_risk / ai_risk.max() if ai_risk.max() > 0 else ai_risk

    score = alpha * sims + beta * demand_norm - gamma * risk_norm

    combined["similarity"] = sims
    combined["ai_risk_norm"] = risk_norm
    combined["score"] = score

    combined = combined.sort_values("score", ascending=False)
    return combined


def compute_skill_gap_for_role(
    role_id: int, user_skill_ids: List[int]
) -> pd.DataFrame:
    """
    For a given role and user skills, return missing skills with
    importance and difficulty.
    """
    rs = load_role_skills()
    skills = load_skills().set_index("skill_id")

    role_rs = rs[rs["role_id"] == role_id].copy()
    role_rs["has_skill"] = role_rs["skill_id"].isin(user_skill_ids)
    missing = role_rs[~role_rs["has_skill"]].copy()
    if missing.empty:
        return pd.DataFrame(columns=["skill_id", "name", "importance", "difficulty_hours"])

    missing = missing.merge(
        skills[["name", "difficulty_hours"]],
        left_on="skill_id",
        right_index=True,
        how="left",
    )
    missing = missing.sort_values(
        ["importance", "difficulty_hours"], ascending=[False, True]
    )
    return missing[["skill_id", "name", "importance", "difficulty_hours"]]

