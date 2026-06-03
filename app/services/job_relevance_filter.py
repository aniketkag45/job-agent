IRRELEVANT_KEYWORDS = [
    "sales",
    "marketing",
    "legal",
    "finance",
    "accounting",
    "customer service",
    "administrative",
    "human resources",
    "operations",
    "project management",
    "hr",
    "recruitment",
    "recruiter",
    "commercial",
    "support",

]
def is_relevant_job(job):
    title = job.get("title", "").lower()
    

    for keyword in IRRELEVANT_KEYWORDS:
        if keyword in title:
            print(f"Filtered irrelevant job:{title}")
            return False

    return True