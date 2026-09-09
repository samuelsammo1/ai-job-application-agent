import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.scoring import calculate_match
from utils.ai_analyzer import analyze_job_application
from utils.ai_generator import generate_application_materials


st.set_page_config(page_title="AI Job Application Agent", page_icon="🤖", layout="wide")


st.title("🤖 AI Job Application Agent")

st.write(
    "Analyze how well your CV matches a job description "
    "using skill matching and Gemini AI."
)

st.divider()


uploaded_cv = st.file_uploader("📄 Upload your CV", type=["pdf"])


job_description = st.text_area(
    "💼 Paste the Job Description",
    height=300,
    placeholder="Paste the complete job description here...",
)


if st.button("🚀 Analyze Application"):
    if uploaded_cv is None:
        st.warning("Please upload your CV.")

    elif not job_description.strip():
        st.warning("Please paste the job description.")

    else:
        with st.spinner("Analyzing your application..."):
            cv_text = extract_text_from_pdf(uploaded_cv)

            # Traditional skill matching
            score, matched, missing = calculate_match(cv_text, job_description)

            # Gemini AI analysis
            try:
                ai_analysis = analyze_job_application(cv_text, job_description)

                ai_error = None

            except Exception as e:
                ai_analysis = None
                ai_error = str(e)

        st.success("Analysis complete!")

        st.divider()

        # -----------------------------
        # MATCH SCORE
        # -----------------------------

        st.subheader("📊 Technical Match Score")

        st.metric("CV Match", f"{score}%")

        st.progress(score / 100)

        # -----------------------------
        # MATCHING SKILLS
        # -----------------------------

        st.subheader("✅ Matching Skills")

        if matched:
            for skill in sorted(matched):
                st.write(f"• {skill}")

        else:
            st.write("No matching technical skills were detected.")

        # -----------------------------
        # MISSING SKILLS
        # -----------------------------

        st.subheader("⚠️ Potential Missing Skills")

        if missing:
            for skill in sorted(missing):
                st.write(f"• {skill}")

        else:
            st.write("No obvious missing skills were detected.")

        # -----------------------------
        # BASIC RECOMMENDATION
        # -----------------------------

        st.subheader("💡 Basic Recommendation")

        if score >= 80:
            st.success(
                "Strong match. Your CV contains most of "
                "the technical skills identified in the job description."
            )

        elif score >= 60:
            st.info(
                "Good match. Consider tailoring your CV "
                "to emphasize the missing skills."
            )

        elif score >= 40:
            st.warning(
                "Moderate match. Your CV should be tailored "
                "more closely to the requirements of this role."
            )

        else:
            st.error("Low technical match. Review the missing skills before applying.")

        # -----------------------------
        # GEMINI AI ANALYSIS
        # -----------------------------

        st.divider()

        st.subheader("🤖 Gemini AI Analysis")

        if ai_error:
            st.error(f"Gemini analysis failed: {ai_error}")

        elif ai_analysis:
            st.markdown(ai_analysis)

        # -----------------------------
        # AI APPLICATION GENERATOR
        # -----------------------------

        st.divider()

        st.subheader("✍️ AI Application Generator")

        if st.button("📝 Generate Application Materials"):
            with st.spinner("Generating tailored application materials..."):
                try:
                    application_materials = generate_application_materials(
                        cv_text, job_description
                    )

                    st.success("Application materials generated!")

                    st.markdown(application_materials)

                except Exception as e:
                    st.error(f"Application generator failed: {e}")

        # -----------------------------
        # CV TEXT
        # -----------------------------

        with st.expander("📄 View Extracted CV Text"):
            st.text(cv_text[:5000])
