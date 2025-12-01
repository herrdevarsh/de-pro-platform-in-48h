from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

import pandas as pd

from .data_loader import load_skills
from .recommend import compute_role_scores, compute_skill_gap_for_role
from .learning_path import build_learning_phases
from .explanations import explain_recommendation
from .projects import suggest_projects_for_role


@dataclass(frozen=True)
class UserProfile:
    """Simple representation of a user for the compass."""
    skill_ids: List[int]
    weekly_hours: int = 8


class JobCompassEngine:
    """
    High-level façade around the underlying data / recommendation logic.

    Responsibilities:
      - Hold skill metadata
      - Compute role recommendations for a user
      - Explain why a role is recommended
      - Build learning plans and project suggestions
    """

    def __init__(self) -> None:
        # Load once, reuse (avoids re-reading CSVs on every call)
        self.skills_df: pd.DataFrame = load_skills().set_index("skill_id")

    # ---------- Public API ----------

    def list_all_skills(self) -> pd.DataFrame:
        """Return the skills table (indexed by skill_id)."""
        return self.skills_df

    def recommend_roles(
        self, profile: UserProfile, top_n: int = 10
    ) -> pd.DataFrame:
        """
        Compute ranked role recommendations for a user profile.

        Returns a DataFrame sorted by 'score' (descending).
        """
        if not profile.skill_ids:
            raise ValueError("UserProfile.skill_ids must not be empty.")

        scores = compute_role_scores(profile.skill_ids)
        # Defensive: keep only top_n rows, copy to avoid accidental mutation
        return scores.head(top_n).copy()

    def explain_role_for_user(
        self, role_id: int, profile: UserProfile, top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Explain why a role is recommended for this user.
        Wraps explain_recommendation.
        """
        return explain_recommendation(role_id, profile.skill_ids, top_k=top_k)

    def build_learning_plan(
        self, role_id: int, profile: UserProfile
    ) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """
        Build a learning plan for a user targeting a specific role.

        Returns:
          - gap_df: missing skills with importance & difficulty
          - plan_df: same as gap_df + estimated_weeks + phase
          - projects: list of project idea strings
        """
        gap_df = compute_skill_gap_for_role(role_id, profile.skill_ids)

        if gap_df.empty:
            # User already matches key skills; still suggest projects.
            projects = suggest_projects_for_role(role_id, [])
            # Empty plan DataFrame with expected columns
            plan_df = gap_df.assign(estimated_weeks=0.0, phase=0)
            return gap_df, plan_df, projects

        plan_df = build_learning_phases(
            gap_df, hours_per_week=profile.weekly_hours
        )
        missing_ids = gap_df["skill_id"].tolist()
        projects = suggest_projects_for_role(role_id, missing_ids)

        return gap_df, plan_df, projects
