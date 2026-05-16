from app.services.database import fetch_jobs

jobs = fetch_jobs()

print("\nTop jobs from database:\n")
for job in jobs:
    print(job)
    print("-" * 40)