import re


SKILLS = {
    "python",
    "javascript",
    "typescript",
    "react",
    "next.js",
    "node.js",
    "express",
    "html",
    "css",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "api",
    "apis",
    "rest api",
    "claude api",
    "fastapi",
    "django",
    "flask",
    "streamlit",
    "machine learning",
    "artificial intelligence",
    "data analysis",
    "data mining",
    "pandas",
    "numpy",
    "matplotlib",
    "power bi",
    "excel",
    "wordpress",
    "php",
}


def normalize_text(text):
    text = text.lower()

    # Normalize common variations
    text = text.replace("rest apis", "rest api")
    text = text.replace("html5", "html")
    text = text.replace("css3", "css")

    # Remove punctuation
    text = re.sub(r"[^\w\s.+#-]", " ", text)

    return text


def extract_skills(text):
    text = normalize_text(text)

    found_skills = set()

    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)

    return found_skills


def calculate_match(cv_text, job_text):

    cv_skills = extract_skills(cv_text)
    job_skills = extract_skills(job_text)

    matched = cv_skills.intersection(job_skills)
    missing = job_skills - cv_skills

    if not job_skills:
        score = 0
    else:
        score = round((len(matched) / len(job_skills)) * 100)

    return score, matched, missing
