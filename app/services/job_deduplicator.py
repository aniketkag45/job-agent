def deduplicator_jobs(jobs):
    unique_jobs = []
    seen_titles = set()
    for job in jobs:
        apply_link = job.get("apply_link")
        if not apply_link:
            continue
        if apply_link in seen_titles:
            continue
        seen_titles.add(apply_link)
        unique_jobs.append(job)
    return unique_jobs