def format_job_message(job):
    return (
        f"🚀 New Job Alert!\n\n"
        f"🏢 Company: {job['company']}\n"
        f"💼 Role: {job['title']}\n"
        f"📍 Location: {job['location']}\n\n"
        f"🔗 Apply Here:\n{job['apply_link']}"
    )

def format_multiple_jobs_message(jobs, limit=5):
    if not jobs:
        return "No new jobs found."
    limited_jobs = jobs[:limit]
    message = f"🚀 {len(limited_jobs)} New Job(s) Found!\n\n"
    for idx, job in enumerate(limited_jobs, start=1):
        message += (
            f"{idx}. {job['title']} at {job['company']}\n"
            f"📍 {job['location']}\n"
            f"🔗 {job['apply_link']}\n\n"
        )
    return message