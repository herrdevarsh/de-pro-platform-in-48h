import pandas as pd


def build_learning_phases(
    missing_skills_df: pd.DataFrame,
    hours_per_week: int = 8,
) -> pd.DataFrame:
    """
    Assign missing skills into sequential phases given user capacity.
    Approx rule: around 4 weeks of content per phase.

    Returns: dataframe with phase + estimated weeks per skill.
    """
    if missing_skills_df.empty:
        return missing_skills_df.assign(phase=0, estimated_weeks=0.0)

    df = missing_skills_df.copy().reset_index(drop=True)
    df["estimated_weeks"] = df["difficulty_hours"] / hours_per_week

    phases = []
    current_phase = 1
    current_sum = 0.0

    for _, row in df.iterrows():
        weeks = row["estimated_weeks"]
        # if adding this skill makes the phase > ~4 weeks, start new phase
        if current_sum + weeks > 4 and current_sum > 0:
            current_phase += 1
            current_sum = 0.0
        phases.append(current_phase)
        current_sum += weeks

    df["phase"] = phases
    return df[
        ["skill_id", "name", "importance", "difficulty_hours", "estimated_weeks", "phase"]
    ]
