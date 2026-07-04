import time
import requests
from app.services.database import job_exists
LEVER_COMPANIES = [
    {"slug": "spotify", "name": "Spotify"},
    {"slug": "palantir", "name": "Palantir"},
    # {"slug": "twitch", "name": "Twitch"},
    # {"slug": "box", "name": "Box"},
    # {"slug": "snowflake", "name": "Snowflake"},
    # {"slug": "lyft", "name": "Lyft"},
    # {"slug": "doordash", "name": "DoorDash"},
    # {"slug": "robinhood", "name": "Robinhood"},
    # {"slug": "instacart", "name": "Instacart"},
    # {"slug": "coinbase", "name": "Coinbase"},
    # {"slug": "opensea", "name": "OpenSea"},
    # {"slug": "stripe", "name": "Stripe"},
]

def fetch_lever_jobs():
    all_jobs = []

    for company in LEVER_COMPANIES:
        slug = company["slug"]
        name = company["name"]
        try:
            url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            jobs = data if isinstance(data, list) else data.get("data", [])
            print(f"Fetched {len(jobs)} jobs from Lever ({name})")
            new_count = 0
            for job in jobs:
                apply_link = job.get("applyUrl") or job.get("hostedUrl", "")
                if job_exists(apply_link):
                    continue
                categories = job.get("categories", {})
                dept = categories.get("department", "")
                team = categories.get("team", "")
                commitment = categories.get("commitment", "")
                location_name = categories.get("location", "")
                description = " ".join(filter(None,[
                    job.get("descriptionPlain", ""),
                    f"Department: {dept}" if dept else "",
                    f"Team: {team}" if team else "",
                    f"Type: {commitment}" if commitment else "",
                ]))
                normalized_job = {
                    "title": job.get("text", "").strip(),
                    "company": name,
                    "location": location_name or job.get("categories",{}).get("allLocations", ["Remote"])[0],
                    "apply_link": apply_link,
                    "description": description,
                    "source": "Lever",
                }
                all_jobs.append(normalized_job)
                new_count += 1
            print(f"  → {new_count} new jobs from {name}")
        except requests.exceptions.Timeout:
             print(f"Lever timed out for {name} — skipping.")
        except requests.exceptions.HTTPError as e:
            print(f"Lever HTTP error for {name}: {e.response.status_code}")
        except Exception as e:
            print(f"Lever error for {name}: {e}")

        # Be respectful — 1 second between companies
        time.sleep(1)
    return all_jobs