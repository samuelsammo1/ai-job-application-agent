import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.scoring import calculate_match
from utils.ai_analyzer import analyze_job_application
from utils.ai_generator import generate_application_materials


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Job Application Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f8fafc;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2.5rem;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            #111827,
            #1e293b,
            #312e81
        );
        color: white;
        margin-bottom: 2rem;
    }

    .hero h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        color: #cbd5e1;
        font-size: 1.1rem;
        line-height: 1.7;
        max-width: 800px;
    }

    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }

    .card {
        background: white;
        padding: 1.4rem;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    .skill {
        display: inline-block;
        padding: 0.4rem 0.75rem;
        margin: 0.25rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .skill-match {
        background: #dcfce7;
        color: #166534;
    }

    .skill-missing {
        background: #fee2e2;
        color: #991b1b;
    }

    .score-card {
        background: white;
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }

    .score {
        font-size: 3rem;
        font-weight: 800;
        color: #4f46e5;
    }

    @media (max-width: 768px) {

        .hero {
            padding: 1.5rem;
        }

        .hero h1 {
            font-size: 2rem;
        }

        .hero p {
            font-size: 0.95rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 AI Job Agent")

    st.caption(
        "Smarter applications. Better opportunities."
    )

    st.divider()

    st.subheader("🚀 How it works")

    st.markdown(
        """
        **1. Upload CV**

        Add your resume as a PDF.

        **2. Add Job Description**

        Paste the job requirements.

        **3. Analyze**

        Compare your skills with the role.

        **4. Generate**

        Create tailored application materials.
        """
    )

    st.divider()

    st.caption(
        "Built with Python • Streamlit • Gemini AI"
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="badge">
            🤖 AI-Powered Career Assistant
        </div>

        <h1>
            AI Job Application Agent
        </h1>

        <p>
            Analyze your CV against job descriptions,
            discover skill gaps, understand your suitability,
            and generate tailored application materials
            in seconds.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# INPUT SECTION
# =========================================================

st.header("📋 Start Your Application Analysis")

st.write(
    "Provide your CV and the job description to see "
    "how well you match the opportunity."
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Your CV")

    st.caption(
        "Upload your latest CV in PDF format."
    )

    uploaded_cv = st.file_uploader(
        "Upload CV",
        type=["pdf"],
    )


with col2:

    st.subheader("💼 Job Description")

    st.caption(
        "Paste the complete job description."
    )

    job_description = st.text_area(
        "Job Description",
        height=230,
        placeholder=(
            "Paste the complete job description here..."
        ),
    )


st.write("")

analyze_button = st.button(
    "🚀 Analyze My Application",
    use_container_width=True,
    type="primary",
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if uploaded_cv is None:

        st.warning(
            "📄 Please upload your CV."
        )

    elif not job_description.strip():

        st.warning(
            "💼 Please paste the job description."
        )

    else:

        with st.spinner(
            "🤖 AI is analyzing your application..."
        ):

            try:

                cv_text = extract_text_from_pdf(
                    uploaded_cv
                )

                score, matched, missing = calculate_match(
                    cv_text,
                    job_description,
                )

                try:

                    ai_analysis = analyze_job_application(
                        cv_text,
                        job_description,
                    )

                    ai_error = None

                except Exception as e:

                    ai_analysis = None
                    ai_error = str(e)

                st.session_state["cv_text"] = cv_text
                st.session_state["job_description"] = job_description
                st.session_state["score"] = score
                st.session_state["matched"] = matched
                st.session_state["missing"] = missing
                st.session_state["ai_analysis"] = ai_analysis
                st.session_state["ai_error"] = ai_error

                st.success(
                    "✅ Analysis completed successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Analysis failed: {e}"
                )


# =========================================================
# RESULTS
# =========================================================

if "score" in st.session_state:

    score = st.session_state["score"]
    matched = st.session_state["matched"]
    missing = st.session_state["missing"]

    ai_analysis = st.session_state["ai_analysis"]
    ai_error = st.session_state["ai_error"]

    cv_text = st.session_state["cv_text"]
    job_description = st.session_state["job_description"]


    st.divider()

    st.header("📊 Application Dashboard")


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)


    with m1:

        st.metric(
            "🎯 Match Score",
            f"{score}%",
        )


    with m2:

        st.metric(
            "✅ Matching Skills",
            len(matched),
        )


    with m3:

        st.metric(
            "⚠️ Potential Gaps",
            len(missing),
        )


    with m4:

        if score >= 80:

            recommendation = "Strong"

        elif score >= 60:

            recommendation = "Good"

        elif score >= 40:

            recommendation = "Moderate"

        else:

            recommendation = "Low"

        st.metric(
            "📌 Match Level",
            recommendation,
        )


    st.progress(
        score / 100,
        text=f"Technical skill alignment: {score}%",
    )


    # -----------------------------------------------------
    # RECOMMENDATION
    # -----------------------------------------------------

    if score >= 80:

        st.success(
            "🎯 Strong match. Your CV contains most "
            "of the technical skills required."
        )

    elif score >= 60:

        st.info(
            "👍 Good match. Tailoring your CV to "
            "the remaining requirements may improve alignment."
        )

    elif score >= 40:

        st.warning(
            "⚡ Moderate match. Review the identified "
            "skill gaps before applying."
        )

    else:

        st.error(
            "⚠️ Low technical match. Carefully review "
            "the job requirements and your CV."
        )


    # -----------------------------------------------------
    # SKILLS
    # -----------------------------------------------------

    st.subheader("✅ Matching Skills")

    if matched:

        skill_html = ""

        for skill in sorted(matched):

            skill_html += (
                f'<span class="skill skill-match">'
                f'✓ {skill}'
                f'</span>'
            )

        st.markdown(
            skill_html,
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "No matching technical skills detected."
        )


    st.subheader("⚠️ Potential Skill Gaps")

    if missing:

        skill_html = ""

        for skill in sorted(missing):

            skill_html += (
                f'<span class="skill skill-missing">'
                f'! {skill}'
                f'</span>'
            )

        st.markdown(
            skill_html,
            unsafe_allow_html=True,
        )

    else:

        st.success(
            "🎉 No obvious skill gaps detected."
        )


    # -----------------------------------------------------
    # GEMINI ANALYSIS
    # -----------------------------------------------------

    st.divider()

    st.header("🤖 AI Career Analysis")

    if ai_error:

        st.error(
            f"Gemini analysis failed: {ai_error}"
        )

    elif ai_analysis:

        st.markdown(ai_analysis)


    # -----------------------------------------------------
    # APPLICATION GENERATOR
    # -----------------------------------------------------

    st.divider()

    st.header("✍️ AI Application Generator")

    st.write(
        "Generate professional application materials "
        "tailored to this job."
    )


    generate_button = st.button(
        "📝 Generate Application Materials",
        use_container_width=True,
    )


    if generate_button:

        with st.spinner(
            "✍️ Generating application materials..."
        ):

            try:

                materials = generate_application_materials(
                    cv_text,
                    job_description,
                )

                st.session_state[
                    "application_materials"
                ] = materials

                st.success(
                    "🎉 Application materials generated!"
                )

            except Exception as e:

                st.error(
                    f"Application generator failed: {e}"
                )


    # -----------------------------------------------------
    # GENERATED MATERIALS
    # -----------------------------------------------------

    if "application_materials" in st.session_state:

        st.subheader("📄 Generated Materials")

        st.markdown(
            st.session_state["application_materials"]
        )


    # -----------------------------------------------------
    # CV TEXT
    # -----------------------------------------------------

    st.divider()

    with st.expander(
        "📄 View Extracted CV Text"
    ):

        st.text_area(
            "CV Text",
            cv_text[:10000],
            height=350,
            disabled=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🤖 AI Job Application Agent • "
    "Built with Python, Streamlit & Gemini AI"
)