SKILL_ALIASES = {
    "js": "javascript",
    "py": "python",
    "rest api": "rest",
}


def normalize_skills(skills):
    """
    Input: list[str]
    Output: set[str]
    """
    normalized = set()

    for skill in skills or []:
        skill = skill.strip().lower()
        skill = SKILL_ALIASES.get(skill, skill)
        if skill:
            normalized.add(skill)

    return normalized