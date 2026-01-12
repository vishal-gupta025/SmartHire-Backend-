import re

from apps.jobs.models import Job
from apps.resumes.models import Resume

def compute_ats_score(text: str) -> tuple[float, dict]:
    if not text:
        return 0.0, {"error": "No text extracted"}

    score = 0
    feedback = {}

    text_lower = text.lower()

    # 🔹 Skills heuristic
    skills = ["python", "django", "rest", "sql", "postgresql"]
    skill_matches = sum(1 for s in skills if s in text_lower)
    skill_score = (skill_matches / len(skills)) * 40
    score += skill_score

    if skill_matches < len(skills):
        feedback["skills"] = "Add more relevant technical skills"

    # 🔹 Experience heuristic
    experience_match = re.search(r"\b\d+\+?\s+years?\b", text_lower)
    if experience_match:
        score += 30
    else:
        feedback["experience"] = "Mention years of experience clearly"

    # 🔹 Resume length heuristic
    word_count = len(text.split())
    if word_count >= 300:
        score += 20
    else:
        feedback["content"] = "Resume is too short; add more detail"

    # 🔹 Formatting bonus
    if "\n" in text:
        score += 10
    else:
        feedback["format"] = "Use proper sections and formatting"

    return round(score, 2), feedback

def calculate_job_ats_score(
    resume_skills: dict,
    job_skills: list[str],
    base_resume_score: float
) -> tuple[float, dict]:
    """
    Job-aware ATS scoring
    """

    if not job_skills:
        return base_resume_score, {"info": "No job skills defined"}

    resume_flat_skills = {
        skill.lower()
        for skills in resume_skills.values()
        for skill in skills
    }

    job_skills = {s.lower() for s in job_skills}

    matched = resume_flat_skills & job_skills
    missing = job_skills - matched

    job_match_score = (len(matched) / len(job_skills)) * 40  # job weight

    final_score = min(base_resume_score + job_match_score, 100)

    feedback = {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "job_match_percent": round((len(matched) / len(job_skills)) * 100, 2),
        "recommendation": (
            "Add missing job-required skills"
            if missing else "Strong match for this role"
        ),
    }

    return round(final_score, 2), feedback


