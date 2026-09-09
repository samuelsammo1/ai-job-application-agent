import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from your .env file.")


client = genai.Client(api_key=api_key)


def generate_application_materials(cv_text, job_description):

    prompt = f"""
You are an expert career application assistant.

Use ONLY the information provided in the candidate's CV.
Do not invent skills, experience, qualifications, projects,
companies, achievements, or technologies.

Create professional application materials tailored to the
job description.

CANDIDATE CV:
{cv_text}

JOB DESCRIPTION:
{job_description}

Generate the following sections:

1. TAILORED COVER LETTER

Write a professional cover letter specifically for this role.
Keep it concise and relevant.

2. WHY ARE YOU A GOOD FIT?

Write a strong answer suitable for an application form.
Use specific evidence from the CV.

3. TELL ME ABOUT YOURSELF

Write a concise professional introduction suitable for an
interview or application form.

4. SHORT APPLICATION MESSAGE

Write a short message the candidate can send to the recruiter
or hiring manager.

5. CV IMPROVEMENT SUGGESTIONS

Give 5 practical suggestions for tailoring the CV to this job.

Important:
- Never claim the candidate has React, Node.js, Docker,
  or any other technology unless it appears in the CV.
- Do not exaggerate experience.
- Keep the writing natural and professional.
"""

    models = [
        "gemini-3.8-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash",
    ]

    last_error = None

    for model in models:
        try:
            response = client.models.generate_content(model=model, contents=prompt)

            return response.text

        except Exception as e:
            last_error = e

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")
