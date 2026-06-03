def normalize_job(job):
    required_fields = ["title", "company", "location", "apply_link", "source"]
    for field in required_fields:
        if field not in job:
            print(f"Missing required field '{field}' in job: {job}")
            return None
        if not job[field]:
            print(f"Empty value for required field '{field}' in job: {job}")
            return None
        normalized_job = {
            "title": str(job["title"]).strip(),
            "company": str(job["company"]).strip(),
            "location": str(job["location"]).strip(),
            "apply_link": str(job["apply_link"]).strip(),
            "source": str(job["source"]).strip()
        }
        if "description" in job:
            normalized_job["description"] = str(job["description"]).strip()
        if "experience_level" in job:
            normalized_job["experience_level"] = str(job["experience_level"]).strip()
        if "tech_stack" in job:
            normalized_job["tech_stack"] = str(job["tech_stack"]).strip()
    return normalized_job