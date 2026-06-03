from app.services.pipeline_metrics import increment_metric   

EXCLUDED_DOMAINS = [

    "sales",

    "marketing",

    "finance",

    "accounting",

    "legal",

    "recruiter",

    "human resources",

    "hr",

    "customer success",

    "operations manager",

    "business development",

    "compliance",

    "tax",

    "commercial counsel",

    "product marketing",

    "partnerships",

    "policy"
]

REQUIRED_TECH_SIGNALS = [

    # Core engineering

    "engineer",

    "developer",

    "software",

    "backend",

    "frontend",

    "full stack",

    "fullstack",

    "web",


    # AI / ML

    "ai",

    "machine learning",

    "artificial intelligence",

    "ml",

    "llm",

    "deep learning",

    "nlp",

    "computer vision",

    "data science",

    "data engineer",

    "data analyst",


    # Infrastructure / Cloud

    "cloud",

    "devops",

    "platform",

    "infrastructure",

    "site reliability",

    "sre",

    "systems engineer",


    # Security

    "security",

    "cybersecurity",


    # Mobile

    "android",

    "ios",

    "mobile",


    # Languages / Tech stack

    "python",

    "java",

    "react",

    "node",

    "typescript",

    "javascript",


    # Specialized domains

    "robotics",

    "embedded",

    "firmware",

    "blockchain",

    "qa",

    "automation",

    "test engineer"
]

def is_domain_relevant(job):

    title = (
        job.get("title") or ""
    ).lower()


    # Reject obvious business domains

    for excluded in EXCLUDED_DOMAINS:

        if excluded in title:

            increment_metric(
                "jobs_filtered"
            )

            return False


    # Require strong technical evidence

    for signal in REQUIRED_TECH_SIGNALS:

        if signal in title:

            return True


    increment_metric(
        "jobs_filtered"
    )

    return False