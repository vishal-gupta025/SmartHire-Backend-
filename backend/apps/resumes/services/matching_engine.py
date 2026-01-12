from .skill_normalizer import normalize_skills


def compute_match_score(
    resume_skills: dict,
    job_required_skills: list,
    job_optional_skills: list | None = None,
):
    """
    Returns:
    - match_score (0–100)
    - feedback dict
    """

    resume_skill_set = normalize_skills(
        skill
        for skills in resume_skills.values()
        for skill in skills
    )

    required = normalize_skills(job_required_skills)
    optional = normalize_skills(job_optional_skills or [])

    if not required:
        return 0, {"error": "No required skills defined"}

    matched_required = resume_skill_set & required
    missing_required = required - matched_required

    matched_optional = resume_skill_set & optional

    required_score = (len(matched_required) / len(required)) * 70
    optional_score = (
        (len(matched_optional) / len(optional)) * 30 if optional else 0
    )

    final_score = round(required_score + optional_score, 2)

    feedback = {
        "matched_required": list(matched_required),
        "missing_required": list(missing_required),
        "matched_optional": list(matched_optional),
    }

    return final_score, feedback