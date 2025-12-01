from ai_job_compass.data_loader import load_skills
from ai_job_compass.recommend import compute_role_scores, compute_skill_gap_for_role
from ai_job_compass.learning_path import build_learning_phases


def main():
    skills = load_skills().set_index("skill_id")
    print("Available skills:")
    for sid, row in skills.iterrows():
        print(f"{sid}: {row['name']}")

    raw = input("\nEnter your skill IDs separated by commas (e.g. 1,3,9): ")
    try:
        user_skill_ids = [int(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError:
        print("Invalid input.")
        return

    scores = compute_role_scores(user_skill_ids)
    print("\nTop recommended roles:")
    print(
        scores[["name", "similarity", "ai_risk_score", "score"]]
        .head(5)
        .to_string(index=False)
    )

    top_role_id = int(scores.index[0])
    top_role_name = scores.iloc[0]["name"]
    print(f"\nUsing top role '{top_role_name}' for learning plan...")

    gap = compute_skill_gap_for_role(top_role_id, user_skill_ids)
    if gap.empty:
        print("You already match all key skills for this role.")
        return

    plan = build_learning_phases(gap, hours_per_week=8)
    print("\nLearning path (assuming ~8h/week):")
    for phase, group in plan.groupby("phase"):
        print(f"\nPhase {phase}:")
        for _, row in group.iterrows():
            print(
                f"  - {row['name']} "
                f"(~{row['estimated_weeks']:.1f} weeks, importance {row['importance']:.2f})"
            )


if __name__ == "__main__":
    main()
