from app.scraper.remoteok_scraper import fetch_remoteok_jobs
from app.scraper.greenhouse_scraper import fetch_greenhouse_jobs

SCRAPERS = [
    fetch_remoteok_jobs,
    fetch_greenhouse_jobs
]