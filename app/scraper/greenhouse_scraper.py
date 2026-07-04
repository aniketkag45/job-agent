from dbm import error
import re
import html
import requests
from app.services.database import job_exists

GREENHOUSE_COMPANIES = [
    {"slug": "stripe", "name": "Stripe"},
    {"slug": "discord", "name": "Discord"},
    {"slug": "airbnb", "name": "Airbnb"},
    {"slug": "dropbox", "name": "Dropbox"},
    {"slug": "reddit", "name": "Reddit"},
    {"slug": "twitch", "name": "Twitch"},
    {"slug": "instacart", "name": "Instacart"},
    {"slug": "lyft", "name": "Lyft"},
    {"slug": "pinterest", "name": "Pinterest"},
    {"slug": "roblox", "name": "Roblox"},
    {"slug": "squarespace", "name": "Squarespace"},
    {"slug": "cloudflare", "name": "Cloudflare"},
    {"slug": "datadog", "name": "Datadog"},
    {"slug": "asana", "name": "Asana"},
    {"slug": "figma", "name": "Figma"},
    {"slug": "anduril", "name": "Anduril"},
    {"slug": "rippling", "name": "Rippling"},
    {"slug": "vercel", "name": "Vercel"},
    {"slug": "notion", "name": "Notion"},
    {"slug": "linear", "name": "Linear"},
]

def fetch_greenhouse_jobs():

    all_jobs = []


    for company in GREENHOUSE_COMPANIES:

     company_slug = company["slug"]

     company_name = company["name"]

     try:

            url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs?content=true"


            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()


            data = response.json()


            jobs = data.get("jobs", [])


            print(
                f"Fetched {len(jobs)} jobs from Greenhouse ({company_name})"
            )

            consecutive_known_jobs = 0


            for job in jobs:

                normalized_job = {
                    
                    "title": job.get("title"),

                    "company": company_name,

                    "location": job.get(
                        "location",
                        {}
                    ).get(
                        "name",
                        "Remote"
                    ),

                    "apply_link": job.get(
                        "absolute_url"
                    ),
                    "description": re.sub(r'<[^>]+>', ' ', html.unescape(job.get("content", ""))).strip(),

                    "source": "Greenhouse"
                }
                apply_link = normalized_job.get("apply_link")
                if job_exists(apply_link):
                    consecutive_known_jobs += 1
                    print(
                        f"Known Greenhouse job detected "
                        f"({consecutive_known_jobs}/5)"
                    )
                    if consecutive_known_jobs >= 5:
                        print(
                            "Encountered 5 consecutive known jobs. "
                            "Stopping early ingestion for Greenhouse."
                        )
                        break
                    continue
                consecutive_known_jobs = 0
                all_jobs.append(normalized_job)

     except Exception as error:

      print(
                f"Error fetching Greenhouse jobs for {company_name}: {error}"
            )


    return all_jobs