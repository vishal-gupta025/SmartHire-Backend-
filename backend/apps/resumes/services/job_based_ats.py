import re
from .skill_extractor import normalize_skills


def compute_job_based_ats(resume_text: str, job) -> tuple[float, dict]:
    feedback = {}
    score = 0.0

    if not resume_text:
        return 0.0, {"resume": "Resume text not available"}

    resume_text_lower = resume_text.lower()

    # 🔹 1. Skill Match (50%)
    job_skills = normalize_skills(job.skills_required)
    resume_skills = normalize_skills(resume_text)

    if job_skills:
        matched = job_skills.intersection(resume_skills)
        skill_score = (len(matched) / len(job_skills)) * 50
        score += skill_score

        if len(matched) < len(job_skills):
            feedback["skills"] = {
                "missing": list(job_skills - matched),
                "matched": list(matched),
            }
    else:
        feedback["skills"] = "Job skills not clearly defined"

    # 🔹 2. Experience Match (25%)
    exp_match = re.search(r"\b\d+\+?\s+years?\b", resume_text_lower)
    if exp_match:
        score += 25
    else:
        feedback["experience"] = "Mention years of experience clearly"

    # 🔹 3. Content Depth (15%)
    word_count = len(resume_text.split())
    if word_count >= 300:
        score += 15
    else:
        feedback["content"] = "Resume is too short for this role"

    # 🔹 4. Formatting (10%)
    if "\n" in resume_text:
        score += 10
    else:
        feedback["format"] = "Use sections and bullet points"

    return round(score, 2), feedback
