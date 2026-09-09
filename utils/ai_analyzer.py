import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from your .env file.")


client = genai.Client(api_key=api_key)


def analyze_job_application(cv_text, job_description):

    prompt = f"""
You are an expert career and recruitment AI.

Analyze the candidate's CV against the job description.

CV:
{cv_text}

JOB DESCRIPTION:
{job_description}

Provide a clear analysis with these sections:

1. Overall Suitability
2. Strengths
3. Missing or Weak Skills
4. Experience Match
5. Recommendations
6. Suggested CV Improvements

Be honest. Do not invent experience, qualifications,
or skills that are not present in the CV.

Keep the response professional and practical.
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
