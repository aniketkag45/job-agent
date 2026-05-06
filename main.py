from app.scraper.fake_jobs_scraper import fetch_jobs
from app.services.job_diff import load_old_jobs, get_new_jobs
from app.utils.file_handler import save_jobs_to_json

def main():
    old_jobs = load_old_jobs()
    new_jobs = fetch_jobs()
    if not new_jobs:
        print("No jobs fetched. Exiting.")
        return

    new_entries = get_new_jobs(old_jobs, new_jobs)
    print(f"Found {len(new_entries)} new job(s).\n")

    for job in new_entries:
        print(job)

    save_jobs_to_json(new_jobs, "scripts/jobs.json")


if __name__ == "__main__":
    main()