def build_candidate_semantic_text(
    profile
):

    skills = " ".join(
        profile.get(
            "skills",
            []
        )
    )

    domains = " ".join(
        profile.get(
            "domains",
            []
        )
    )

    experience = profile.get(
        "experience_level",
        "unknown"
    )

    semantic_text = f"""

        Candidate Profile

        Experience Level:
        {experience}

        Domains:
        {domains}

        Skills:
        {skills}

        """

    return semantic_text.strip()