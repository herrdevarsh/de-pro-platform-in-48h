from typing import List, Dict

import pandas as pd

from .data_loader import load_roles, load_skills


ROLE_TEMPLATES = {
    "Data Analyst": [
        "Build a business KPI dashboard using a public dataset (e.g. sales or marketing) with at least 3 key metrics and a written summary.",
        "Analyze a customer churn dataset and present your findings in both SQL queries and a visualization tool."
    ],
    "BI Engineer": [
        "Design and implement a small star-schema warehouse (fact + 2–3 dimensions) and build a BI report on top of it.",
        "Take raw CSV data, build an ETL script into a database, and create a self-service dashboard for a fictional stakeholder."
    ],
    "ML Engineer": [
        "Train and deploy a small ML model as an API (FastAPI/Flask) and document the full pipeline from data to deployment.",
        "Implement an end-to-end ML project with train/validation split, metrics tracking, and model versioning."
    ],
    "Backend Developer": [
        "Build a REST API with authentication and a simple database, including tests and documentation.",
        "Refactor a small monolithic service into modular components and document the architecture decisions."
    ],
    "MLOps Engineer": [
        "Take an existing ML model and wrap it in a container, add logging, and create a simple CI/CD pipeline.",
        "Set up an experiment tracking flow (e.g. MLflow-like) for a toy ML project, including configuration management."
    ],
}


def suggest_projects_for_role(
    role_id: int,
    missing_skill_ids: List[int],
    max_projects: int = 2,
) -> List[str]:
    """
    Return a list of project ideas for the given role, optionally tweaked
    based on missing skills.
    """
    roles = load_roles().set_index("role_id")
    skills = load_skills().set_index("skill_id")

    role_name = roles.loc[role_id, "name"]

    base_projects = ROLE_TEMPLATES.get(role_name, [])
    if not base_projects:
        # generic fallback
        base_projects = [
            "Choose a realistic dataset and build a small end-to-end project that demonstrates your core skills.",
            "Document your project in a README with problem, approach, and results so it is portfolio-ready."
        ]

    # Light personalization: mention 1–2 key missing skills in the project text
    missing_names = [skills.loc[sid, "name"] for sid in missing_skill_ids if sid in skills.index]
    missing_extra = ""
    if missing_names:
        top_missing = ", ".join(missing_names[:2])
        missing_extra = f" Focus especially on practicing: {top_missing}."

    projects = []
    for idea in base_projects[:max_projects]:
        projects.append(idea + missing_extra)

    return projects
