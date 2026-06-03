TECH_STACK_KEYWORDS = [

    "python",

    "java",

    "javascript",

    "typescript",

    "react",

    "nextjs",

    "node",

    "express",

    "fastapi",

    "django",

    "flask",

    "postgresql",

    "mysql",

    "mongodb",

    "redis",

    "docker",

    "kubernetes",

    "aws",

    "gcp",

    "azure",

    "tensorflow",

    "pytorch",

    "llm",

    "openai",

    "langchain",

    "rag",

    "machine learning",

    "ai",

    "devops",

    "linux",

    "graphql"
]

def extract_tech_stack(job):
    title = (
        job.get("title") or ""    ).lower()
    description = (
        job.get("description") or ""    ).lower()
    combined_text = title + " " + description
    detected_tech = []
    for keyword in TECH_STACK_KEYWORDS:

        if keyword in combined_text:

            detected_tech.append(keyword)

    return detected_tech