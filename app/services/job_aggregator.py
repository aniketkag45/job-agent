from app.scraper.remoteok_scraper import fetch_remoteok_jobs

def fetch_all_jobs():
    all_jobs = []

    remoteok_jobs = fetch_remoteok_jobs()

    all_jobs.extend(remoteok_jobs)

    return all_jobs