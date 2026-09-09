import streamlit as st
from engine.recommender import recommend_resources

st.set_page_config(
    page_title="EduMatch AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduMatch AI")
st.write("Personalized learning resource recommendation system powered by multi-factor scoring, time-aware filters, and Explainable AI.")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Tell us about yourself")
    name = st.text_input("Enter your name", value="Alex")
    subject = st.selectbox(
        "Select your subject",
        ["Python", "DSA", "Mathematics", "Physics", "Web Development"]
    )
    level = st.selectbox(
        "Select your level",
        ["Beginner", "Intermediate", "Advanced"]
    )
    goal = st.selectbox(
        "What is your goal?",
        [
            "Exam Preparation",
            "Concept Understanding",
            "Practice",
            "Project Building"
        ]
    )
    time_option = st.selectbox(
        "⏱️ Available Study Time",
        [
            "Any duration (No limit)",
            "25 - 30 Minutes (Quick Sprint)",
            "45 Minutes (Class Period)",
            "1 Hour (Standard Session)",
            "1.5 Hours (Deep Study)",
            "2 Hours (Intensive)",
            "3+ Hours (Masterclass)"
        ],
        index=3  # Default: 1 Hour
    )
    time_map = {
        "Any duration (No limit)": None,
        "25 - 30 Minutes (Quick Sprint)": 30,
        "45 Minutes (Class Period)": 45,
        "1 Hour (Standard Session)": 60,
        "1.5 Hours (Deep Study)": 90,
        "2 Hours (Intensive)": 120,
        "3+ Hours (Masterclass)": 180,
    }
    max_duration_minutes = time_map[time_option]

    preferred_format = st.selectbox(
        "✨ Preferred Format",
        [
            "Any format (balanced)",
            "Video",
            "PPT",
            "Notes",
            "Interactive Practice",
            "Quiz",
            "Course"
        ]
    )
    pref_type = "" if preferred_format == "Any format (balanced)" else preferred_format

    find_clicked = st.button("⚡ Find Best Matches", use_container_width=True)

with col2:
    st.header("📚 Recommended Resources")

    if find_clicked or "has_searched" not in st.session_state:
        st.session_state.has_searched = True

        result = recommend_resources({
            "name": name,
            "subject": subject,
            "level": level,
            "goal": goal,
            "preferred_type": pref_type,
            "max_duration_minutes": max_duration_minutes
        }, top_n=5)

        recs = result.get("recommendations", [])

        if not recs:
            st.info("No matching resources found for the current criteria. Try increasing your study time limit.")
        else:
            time_msg = f" (Max Time: {max_duration_minutes}m)" if max_duration_minutes else ""
            st.success(f"Found {len(recs)} personalized recommendations for **{name}**{time_msg}!")

            for idx, r in enumerate(recs, 1):
                type_icon = "🎥" if r['type'] == 'Video' else ("📊" if r['type'] == 'PPT' else ("📝" if r['type'] == 'Notes' else "⭐"))
                with st.expander(f"{type_icon} {r['title']} — {r['score']}% Match ({r['type']})", expanded=(idx == 1)):
                    st.markdown(f"**Subject:** {r['subject']} | **Level:** {r['level']} | **Rating:** {r.get('rating', '4.5')}/5.0 | **Duration:** {r.get('duration', 'N/A')}")
                    st.write(r.get("description", ""))
                    
                    explanation = r.get("explanation", {})
                    if explanation:
                        st.info(f"💡 **Why Recommended:** {explanation.get('summary', '')}")
                        reasons = explanation.get("reasons", [])
                        if reasons:
                            for reason in reasons:
                                st.write(f"- {reason}")
                        badges = explanation.get("badges", [])
                        if badges:
                            st.caption("Badges: " + " • ".join(badges))

                    col_a, col_b = st.columns(2)
                    with col_a:
                        is_downloadable = r.get("downloadable") or r.get("type") in ["Notes", "PPT"] or r.get("download_url")
                        if is_downloadable:
                            dl_url = r.get("download_url") or r.get("url")
                            st.markdown(f"📥 [**Download {r['type']} File**]({dl_url})")
                    with col_b:
                        if r.get("url"):
                            st.markdown(f"↗️ [Open Material Online]({r['url']})")