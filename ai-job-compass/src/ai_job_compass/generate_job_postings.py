import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from .data_loader import load_roles

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


ROLE_TITLE_TEMPLATES = {
    "Backend Developer": [
        "Backend Developer",
        "Backend Engineer",
        "Python Backend Developer",
    ],
    "Frontend Developer": [
        "Frontend Developer",
        "Frontend Engineer",
        "React Frontend Developer",
    ],
    "Full-Stack Developer": [
        "Full-Stack Developer",
        "Full-Stack Engineer",
    ],
    "Data Analyst": [
        "Data Analyst",
        "Junior Data Analyst",
        "Product Data Analyst",
    ],
    "BI Engineer": [
        "BI Engineer",
        "BI Developer",
        "Analytics Engineer",
    ],
    "Data Engineer": [
        "Data Engineer",
        "Data Platform Engineer",
    ],
    "ML Engineer": [
        "ML Engineer",
        "Machine Learning Engineer",
        "Applied ML Engineer",
    ],
    "MLOps Engineer": [
        "MLOps Engineer",
        "Machine Learning Platform Engineer",
    ],
    "Product Analyst": [
        "Product Analyst",
        "Growth Analyst",
    ],
    "QA Automation Engineer": [
        "QA Automation Engineer",
        "Test Automation Engineer",
    ],
    "Cloud Engineer": [
        "Cloud Engineer",
        "Cloud Platform Engineer",
    ],
}

LOCATIONS = [
    "Berlin",
    "Munich",
    "Hamburg",
    "Remote",
    "Frankfurt",
    "Amsterdam",
    "London",
]

ROLE_SALARY_BANDS = {
    "Backend Developer": (55000, 85000),
    "Frontend Developer": (50000, 80000),
    "Full-Stack Developer": (60000, 90000),
    "Data Analyst": (45000, 75000),
    "BI Engineer": (52000, 80000),
    "Data Engineer": (60000, 95000),
    "ML Engineer": (65000, 110000),
    "MLOps Engineer": (70000, 115000),
    "Product Analyst": (55000, 90000),
    "QA Automation Engineer": (45000, 75000),
    "Cloud Engineer": (65000, 105000),
}


def generate_job_postings(n_per_role: int = 30) -> pd.DataFrame:
    roles = load_roles()
    rows = []
    job_id = 1

    base_date = datetime(2025, 9, 1)

    for _, role in roles.iterrows():
        role_id = role["role_id"]
        role_name = role["name"]

        titles = ROLE_TITLE_TEMPLATES.get(role_name, [role_name])
        salary_low, salary_high = ROLE_SALARY_BANDS.get(
            role_name, (50000, 90000)
        )

        for _ in range(n_per_role):
            title = random.choice(titles)
            location = random.choice(LOCATIONS)

            # random salary band inside global band
            low = random.randint(int(salary_low * 0.9), int(salary_low * 1.1))
            high = random.randint(max(low + 5000, int(salary_high * 0.9)), int(salary_high * 1.1))

            days_offset = random.randint(0, 90)
            posted_at = base_date + timedelta(days=days_offset)

            rows.append(
                {
                    "job_id": job_id,
                    "role_id": role_id,
                    "title": title,
                    "location": location,
                    "salary_low": low,
                    "salary_high": high,
                    "posted_at": posted_at.date().isoformat(),
                }
            )
            job_id += 1

    return pd.DataFrame(rows)


def main():
    df = generate_job_postings(n_per_role=30)  # 11 roles * 30 = 330 postings
    out_path = DATA_DIR / "job_postings.csv"
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} job postings -> {out_path}")


if __name__ == "__main__":
    main()
