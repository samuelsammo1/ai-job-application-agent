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

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f8fafc;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- HERO ---------- */

    .hero {
        padding: 2.5rem;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1e293b 50%,
            #312e81 100%
        );
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(15, 23, 42, 0.15);
    }


    .hero h1 {
        font-size: 3rem;
        line-height: 1.1;
        margin: 0;
        font-weight: 800;
    }

    .hero p {
        font-size: 1.1rem;
        color: #cbd5e1;
        max-width: 750px;
        margin-top: 1rem;
        line-height: 1.7;
    }

    /* ---------- CARDS ---------- */

    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.6rem;
    }

    .card-description {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ---------- SKILL BADGES ---------- */

    .skill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.8rem;
    }

    .skill {
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .skill-match {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }

    .skill-missing {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }

    /* ---------- SECTION HEADERS ---------- */

    .section-header {
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .section-header h2 {
        font-size: 1.55rem;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }

    .section-header p {
        color: #64748b;
        margin-top: 0;
    }

    /* ---------- SCORE ---------- */

    .score-card {
        background: white;
        padding: 1.8rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    }

    .score-number {
        font-size: 3rem;
        font-weight: 800;
        color: #4f46e5;
        margin: 0.4rem 0;
    }

    .score-label {
        color: #64748b;
        font-size: 0.9rem;
    }

    /* ---------- STATUS ---------- */

    .status-good {
        padding: 1rem;
        border-radius: 14px;
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
        font-weight: 600;
    }

    .status-medium {
        padding: 1rem;
        border-radius: 14px;
        background: #fffbeb;
        border: 1px solid #fde68a;
        color: #92400e;
        font-weight: 600;
    }

    .status-low {
        padding: 1rem;
        border-radius: 14px;
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #991b1b;
        font-weight: 600;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #0f172a;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 10px;
        min-height: 2.8rem;
        font-weight: 600;
        border: none;
    }

    /* ---------- TEXT AREA ---------- */

    textarea {
        border-radius: 12px !important;
    }

    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 14px;
        padding: 0.5rem;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 1.5rem;
            border-radius: 18px;
        }

        .hero h1 {
            font-size: 2rem;
        }

        .hero p {
            font-size: 0.95rem;
        }

        .score-number {
            font-size: 2.4rem;
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
    st.markdown(
        """
        <div style="text-align:center; padding:1rem 0 2rem 0;">
            <div style="font-size:3rem;">🤖</div>
            <h2>AI Job Agent</h2>
            <p style="color:#94a3b8;">
                Smarter applications.<br>
                Better opportunities.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### 🚀 How it works")

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

    st.caption("Built with Python + Streamlit + Gemini AI")


# =========================================================
# HERO SECTION
# =========================================================

st.title("🤖 AI Job Application Agent")

st.subheader("AI-Powered Career Assistant")

st.write(
    "Analyze your CV against job descriptions, discover "
    "skill gaps, understand your suitability, and generate "
    "tailored application materials in seconds."
)


# =========================================================
# INPUT SECTION
# =========================================================

input_col1, input_col2 = st.columns([1, 1])


with input_col1:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">📄 Your CV</div>
            <div class="card-description">
                Upload your latest CV in PDF format.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_cv = st.file_uploader(
        "Upload CV", type=["pdf"], label_visibility="collapsed"
    )


with input_col2:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">💼 Job Description</div>
            <div class="card-description">
                Paste the complete job description.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder=("Paste the complete job description here..."),
        label_visibility="collapsed",
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

analyze_button = st.button(
    "🚀 Analyze My Application", use_container_width=True, type="primary"
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:
    if uploaded_cv is None:
        st.warning("📄 Please upload your CV before starting the analysis.")

    elif not job_description.strip():
        st.warning("💼 Please paste the job description before starting.")

    else:
        with st.spinner("🤖 AI is analyzing your application..."):
            try:
                cv_text = extract_text_from_pdf(uploaded_cv)

                # Traditional matching
                score, matched, missing = calculate_match(cv_text, job_description)

                # Gemini analysis
                try:
                    ai_analysis = analyze_job_application(cv_text, job_description)

                    ai_error = None

                except Exception as e:
                    ai_analysis = None
                    ai_error = str(e)

                # Save results in session state
                st.session_state["cv_text"] = cv_text
                st.session_state["job_description"] = job_description
                st.session_state["score"] = score
                st.session_state["matched"] = matched
                st.session_state["missing"] = missing
                st.session_state["ai_analysis"] = ai_analysis
                st.session_state["ai_error"] = ai_error

                st.success("✅ Analysis completed successfully!")

            except Exception as e:
                st.error(f"❌ Unable to analyze the CV: {e}")


# =========================================================
# DISPLAY RESULTS
# =========================================================

if "score" in st.session_state:
    score = st.session_state["score"]
    matched = st.session_state["matched"]
    missing = st.session_state["missing"]
    ai_analysis = st.session_state["ai_analysis"]
    ai_error = st.session_state["ai_error"]
    cv_text = st.session_state["cv_text"]
    job_description = st.session_state["job_description"]

    # =====================================================
    # DASHBOARD
    # =====================================================

    st.markdown(
        """
        <div class="section-header">
            <h2>📊 Application Dashboard</h2>
            <p>
                Here's how your CV compares with the job requirements.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-label">
                    Technical Match
                </div>

                <div class="score-number">
                    {score}%
                </div>

                <div class="score-label">
                    Overall skill alignment
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric2:
        st.metric("✅ Matching Skills", len(matched))

    with metric3:
        st.metric("⚠️ Potential Gaps", len(missing))

    with metric4:
        if score >= 80:
            st.metric("🎯 Recommendation", "Strong Match")

        elif score >= 60:
            st.metric("🎯 Recommendation", "Good Match")

        elif score >= 40:
            st.metric("🎯 Recommendation", "Moderate")

        else:
            st.metric("🎯 Recommendation", "Low Match")

    st.progress(score / 100, text=f"Technical skill alignment: {score}%")

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    if score >= 80:
        st.markdown(
            """
            <div class="status-good">
                🎯 Strong Match — Your CV contains most of the
                technical skills identified in this job description.
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif score >= 60:
        st.markdown(
            """
            <div class="status-medium">
                👍 Good Match — You have a solid foundation.
                Tailor your CV to emphasize the remaining requirements.
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif score >= 40:
        st.markdown(
            """
            <div class="status-medium">
                ⚡ Moderate Match — Consider strengthening your CV
                around the key requirements before applying.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            """
            <div class="status-low">
                ⚠️ Low Match — Review the identified skill gaps
                carefully before applying.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # SKILLS
    # =====================================================

    skills_col1, skills_col2 = st.columns(2)

    with skills_col1:
        st.markdown(
            """
            <div class="section-header">
                <h2>✅ Matching Skills</h2>
                <p>Skills detected in both your CV and the job.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if matched:
            badges = ""

            for skill in sorted(matched):
                badges += f'<span class="skill skill-match">✓ {skill}</span>'

            st.markdown(
                f'<div class="skill-container">{badges}</div>', unsafe_allow_html=True
            )

        else:
            st.info("No matching technical skills were detected.")

    with skills_col2:
        st.markdown(
            """
            <div class="section-header">
                <h2>⚠️ Potential Skill Gaps</h2>
                <p>Skills mentioned in the job but not detected in your CV.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if missing:
            badges = ""

            for skill in sorted(missing):
                badges += f'<span class="skill skill-missing">! {skill}</span>'

            st.markdown(
                f'<div class="skill-container">{badges}</div>', unsafe_allow_html=True
            )

        else:
            st.success("🎉 No obvious technical skill gaps detected.")

    # =====================================================
    # GEMINI ANALYSIS
    # =====================================================

    st.divider()

    st.markdown(
        """
        <div class="section-header">
            <h2>🤖 AI Career Analysis</h2>
            <p>
                Gemini's assessment of your suitability for this role.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if ai_error:
        st.error(f"Gemini analysis failed: {ai_error}")

    elif ai_analysis:
        with st.container(border=True):
            st.markdown(ai_analysis)

    # =====================================================
    # APPLICATION GENERATOR
    # =====================================================

    st.divider()

    st.markdown(
        """
        <div class="section-header">
            <h2>✍️ AI Application Generator</h2>
            <p>
                Generate professional application materials
                tailored to this specific job.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    generate_button = st.button(
        "📝 Generate Application Materials", use_container_width=True
    )

    if generate_button:
        with st.spinner("✍️ Creating your tailored application materials..."):
            try:
                application_materials = generate_application_materials(
                    cv_text, job_description
                )

                st.session_state["application_materials"] = application_materials

                st.success("🎉 Application materials generated!")

            except Exception as e:
                st.error(f"Application generator failed: {e}")

    # =====================================================
    # GENERATED MATERIALS
    # =====================================================

    if "application_materials" in st.session_state:
        materials = st.session_state["application_materials"]

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "💌 Cover Letter",
                "🎯 Why I'm a Good Fit",
                "👤 About Me",
                "📩 Recruiter Message",
            ]
        )

        with tab1:
            st.markdown("### 💌 Tailored Cover Letter")

            st.markdown(materials)

        with tab2:
            st.markdown("### 🎯 Why Are You a Good Fit?")

            st.markdown(materials)

        with tab3:
            st.markdown("### 👤 Tell Me About Yourself")

            st.markdown(materials)

        with tab4:
            st.markdown("### 📩 Short Application Message")

            st.markdown(materials)

    # =====================================================
    # CV TEXT
    # =====================================================

    st.divider()

    with st.expander("📄 View Extracted CV Text"):
        st.text_area("Extracted CV", cv_text[:10000], height=350, disabled=True)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption("🤖 AI Job Application Agent • Built with Python • Streamlit • Gemini AI")

st.caption("AI-assisted career technology project")
