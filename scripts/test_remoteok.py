from app.scraper.remoteok_scraper import fetch_remoteok_jobs

jobs = fetch_remoteok_jobs()
print(f"Fetched {len(jobs)} jobs from RemoteOK")

for job in jobs[:5]:
    print(job)
    print("-" * 40)