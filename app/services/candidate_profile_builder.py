from pydoc import text


KNOWN_SKILLS = [

    "java",
    "python",
    "javascript",
    "react",
    "spring boot",
    "docker",
    "postgresql",
    "mysql",
    "tensorflow",
    "pytorch",
    "opencv",
    "transformers",
    "git",
    "kafka",
    "aws",
    "rest api",
    "tailwindcss"
]

def extract_skills(text):
    text = text.lower()
    skills = []
    for skill in KNOWN_SKILLS:
        if skill in text:
            skills.append(skill)
    return skills

DOMAIN_KEYWORDS = {

    "backend": [
        "spring boot",
        "rest api",
        "java",
        "postgresql"
    ],

    "ai": [
        "tensorflow",
        "pytorch",
        "transformers",
        "machine learning"
    ],

    "frontend": [
        "react",
        "javascript",
        "tailwindcss"
    ]
}

def extract_domains(skills):
    domains = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in skills:
                domains.append(domain)
                break
    return domains

def detect_experience_level(text):

    text = text.lower()

    if "intern" in text:
        return "student"

    if "bachelor" in text:
        return "student"

    return "unknown"

def build_candidate_profile(resume_text):
    skills = extract_skills(resume_text)
    domains = extract_domains(skills)
    experience_level = detect_experience_level(resume_text)

    profile = {
        "skills": skills,
        "domains": domains,
        "experience_level": experience_level
    }
    return profile