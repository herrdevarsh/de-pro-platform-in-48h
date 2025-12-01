import streamlit as st
import pandas as pd

from ai_job_compass.engine import JobCompassEngine, UserProfile


st.set_page_config(
    page_title="AI Job Transition Compass",
    page_icon="🧭",
    layout="wide",
)


@st.cache_resource
def get_engine() -> JobCompassEngine:
    return JobCompassEngine()


def main():
    engine = get_engine()
    skills_df = engine.list_all_skills()

    # ---- Header ----
    st.title("AI Job Transition Compass")
    st.write("Pick your current skills. Get a realistic target role, a focused learning plan, and project ideas.")
    st.markdown("---")

    # ---- Sidebar: user inputs ----
    st.sidebar.header("Your profile")

    selected_skill_ids = st.sidebar.multiselect(
        "Current skills",
        options=list(skills_df.index),
        format_func=lambda sid: skills_df.loc[sid, "name"],
    )

    weekly_hours = st.sidebar.slider(
        "Learning hours per week",
        min_value=4,
        max_value=20,
        value=8,
        step=2,
    )

    max_roles = st.sidebar.slider(
        "How many roles to consider",
        min_value=3,
        max_value=15,
        value=8,
        step=1,
    )

    if not selected_skill_ids:
        st.info("Select at least one skill in the sidebar to see recommendations.")
        return

    profile = UserProfile(skill_ids=selected_skill_ids, weekly_hours=weekly_hours)
    scores = engine.recommend_roles(profile, top_n=50)

    if scores.empty:
        st.warning("No roles available for this skill set.")
        return

    # Limit to relevant top roles for interaction
    top_scores = scores.head(max_roles).copy()

    # ---- Choose target role (no visuals here) ----
    role_ids = list(top_scores.index)
    role_names = [top_scores.loc[rid, "name"] for rid in role_ids]

    st.subheader("Focus role")

    selected_role_name = st.selectbox(
        "Pick a role to plan for",
        options=role_names,
        index=0,  # default: top-ranked
    )
    selected_role_id = role_ids[role_names.index(selected_role_name)]

    selected_row = scores.loc[selected_role_id]

    # Compact summary (metrics only)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Role", selected_row["name"])
    c2.metric("Skill fit", f"{selected_row['similarity']:.2f}")
    c3.metric("Demand index", f"{selected_row['demand_norm']:.2f}")
    if selected_row["avg_salary"] > 0:
        c4.metric("Avg. salary (est.)", f"{selected_row['avg_salary']:.0f}")
    else:
        c4.metric("Avg. salary (est.)", "N/A")

    st.caption(
        f"You match this role with a skill fit of {selected_row['similarity']:.2f}, "
        f"in a market with demand index {selected_row['demand_norm']:.2f} "
        f"and AI risk {selected_row['ai_risk_score']:.2f}."
    )

    st.markdown("---")

    # ---- Explanation + learning plan for selected role ----
    explanation = engine.explain_role_for_user(selected_role_id, profile, top_k=3)
    gap_df, plan_df, projects = engine.build_learning_plan(selected_role_id, profile)

    st.markdown("### Skill match")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**You already have:**")
        if explanation["matched_skills"]:
            for item in explanation["matched_skills"]:
                st.write(f"- {item['name']} (importance {item['importance']:.2f})")
        else:
            st.write("- No key skills matched yet (this is a stretch role).")

    with col2:
        st.markdown("**You need to add:**")
        if explanation["missing_skills"]:
            for item in explanation["missing_skills"]:
                st.write(f"- {item['name']} (importance {item['importance']:.2f})")
        else:
            st.write("- No critical gaps. Focus on projects and experience.")

    st.markdown("### Learning steps")

    if gap_df.empty:
        st.success(
            "You already cover the key skills for this role. "
            "Next: build 1–2 strong projects and practice interviews."
        )
    else:
        st.caption(
            f"Plan assumes ~{weekly_hours} hours/week. Each phase is roughly 3–5 weeks."
        )
        for phase, group in plan_df.groupby("phase"):
            st.markdown(f"**Phase {phase}**")
            for _, r in group.iterrows():
                st.write(
                    f"- {r['name']} — ~{r['estimated_weeks']:.1f} weeks "
                    f"(importance {r['importance']:.2f})"
                )

    st.markdown("### Project ideas")
    for p in projects:
        st.write(f"- {p}")

    # ---- Table of all recommended roles ----
    st.markdown("---")
    st.markdown("### All recommended roles (summary)")

    table_cols = ["name", "similarity", "demand_count", "avg_salary", "ai_risk_score", "score"]
    table = (
        scores[table_cols]
        .reset_index(drop=True)
        .rename(
            columns={
                "name": "Role",
                "similarity": "Skill fit",
                "demand_count": "Demand",
                "avg_salary": "Avg. salary",
                "ai_risk_score": "AI risk",
                "score": "Score",
            }
        )
    )

    st.dataframe(
        table.style.format(
            {
                "Skill fit": "{:.2f}",
                "AI risk": "{:.2f}",
                "Avg. salary": "{:.0f}",
                "Score": "{:.2f}",
            }
        ),
        use_container_width=True,
    )

    # ---- Visual (not at top, not a bar graph): scatter plot ----
    st.markdown("### Role landscape (visual)")

    scatter_df = scores[["name", "similarity", "ai_risk_score", "demand_count"]].copy()
    scatter_df = scatter_df.rename(
        columns={
            "name": "Role",
            "similarity": "Skill fit",
            "ai_risk_score": "AI risk",
            "demand_count": "Demand",
        }
    )

    st.caption(
        "Each point is a role. X-axis = skill fit, Y-axis = AI risk, bubble size ≈ demand."
    )

    # Streamlit scatter chart (not a bar graph, and at the bottom)
    st.scatter_chart(
        scatter_df,
        x="Skill fit",
        y="AI risk",
        size="Demand",
    )


if __name__ == "__main__":
    main()
