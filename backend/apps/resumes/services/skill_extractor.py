import re


def normalize_skills(text: str) -> set[str]:
    """
    Very simple keyword normalizer.
    Lowercase, split by comma/space, remove noise.
    """
    if not text:
        return set()

    text = text.lower()
    tokens = re.split(r"[,\n;/|]+", text)
    return {t.strip() for t in tokens if len(t.strip()) > 1}


SKILL_KEYWORDS = {
    "technical": [
        "python", "django", "rest", "sql", "postgresql",
        "docker", "git", "linux", "redis", "celery"
    ],
    "soft": [
        "communication", "leadership", "teamwork",
        "problem solving", "critical thinking"
    ],
    "other": [
        "internship", "project", "research", "training"
    ]
}

def extract_skills(text: str) -> dict:
    text = text.lower()
    extracted = {}

    for category, skills in SKILL_KEYWORDS.items():
        matched = [
            skill for skill in skills
            if re.search(rf"\b{re.escape(skill)}\b", text)
        ]
        if matched:
            extracted[category] = matched

    return extracted