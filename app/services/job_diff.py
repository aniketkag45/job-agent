import json
import os

def load_old_jobs(file_path = "scripts/jobs.json"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_new_jobs(old_jobs, new_jobs):
    old_links = set(job["apply_link"] for job in old_jobs)

    new_entries = []

    for job in new_jobs:
        if job["apply_link"] not in old_links:
            new_entries.append(job)
    return new_entries