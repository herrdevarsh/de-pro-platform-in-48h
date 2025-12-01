from pathlib import Path
from typing import Tuple

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_job_postings() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "job_postings.csv", parse_dates=["posted_at"])
    return df


def compute_role_demand() -> pd.DataFrame:
    """
    Returns a DataFrame indexed by role_id with:
      - demand_count: number of postings
      - demand_norm: normalized demand [0,1]
      - avg_salary: mean of (salary_low + salary_high)/2
    """
    jobs = load_job_postings()
    jobs["avg_salary"] = (jobs["salary_low"] + jobs["salary_high"]) / 2

    agg = jobs.groupby("role_id").agg(
        demand_count=("job_id", "count"),
        avg_salary=("avg_salary", "mean"),
    )

    max_demand = agg["demand_count"].max()
    if max_demand > 0:
        agg["demand_norm"] = agg["demand_count"] / max_demand
    else:
        agg["demand_norm"] = 0.0

    return agg
