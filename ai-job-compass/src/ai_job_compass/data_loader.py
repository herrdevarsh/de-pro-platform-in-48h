from pathlib import Path
from typing import Tuple

import pandas as pd
import numpy as np

# project_root/src/ai_job_compass/data_loader.py  -> parents[2] = project_root
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_skills() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "skills.csv")
    return df


def load_roles() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "roles.csv")
    return df


def load_role_skills() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "role_skills.csv")
    return df


def build_role_skill_matrix() -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    """
    Returns:
      roles_df (indexed by role_id),
      skills_df (indexed by skill_id),
      matrix: roles x skills with importance values.
    """
    skills = load_skills()
    roles = load_roles()
    role_skills = load_role_skills()

    mat = role_skills.pivot_table(
        index="role_id",
        columns="skill_id",
        values="importance",
        fill_value=0.0,
        aggfunc="mean",
    )
    # ensure all skills appear
    mat = mat.reindex(columns=skills["skill_id"], fill_value=0.0)

    mat = mat.sort_index(axis=0).sort_index(axis=1)

    return roles.set_index("role_id"), skills.set_index("skill_id"), mat.values
