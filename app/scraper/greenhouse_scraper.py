from dbm import error

import requests
from app.services.database import job_exists


GREENHOUSE_COMPANIES = [

    # {
    #     "slug": "openai",
    #     "name": "OpenAI"
    # },

    {
        "slug": "stripe",
        "name": "Stripe"
    },

    # {
    #     "slug": "notion",
    #     "name": "Notion"
    # },

    {
        "slug": "discord",
        "name": "Discord"
    }
]


def fetch_greenhouse_jobs():

    all_jobs = []


    for company in GREENHOUSE_COMPANIES:

     company_slug = company["slug"]

     company_name = company["name"]

     try:

            url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"


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
                    "description": job.get("content",""),

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