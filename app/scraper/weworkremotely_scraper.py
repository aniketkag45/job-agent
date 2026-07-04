from playwright.sync_api import sync_playwright
from app.services.database import job_exists

WWR_URL = "https://weworkremotely.com/categories/remote-programming-jobs"


def fetch_weworkremotely_jobs():
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(WWR_URL, timeout=30000)
        page.wait_for_timeout(3000)

        listings = page.query_selector_all("li.new-listing-container")
        print(f"Found {len(listings)} listings on We Work Remotely")

        consecutive_known = 0

        for listing in listings:
            try:
                title_el = listing.query_selector("h3.new-listing__header__title")
                company_el = listing.query_selector("p.new-listing__company-name")
                link_el = listing.query_selector("a.listing-link--unlocked")
                location_el = listing.query_selector("p.new-listing__company-headquarters")

                title = title_el.inner_text().strip() if title_el else None
                company = company_el.inner_text().strip() if company_el else None
                location = location_el.inner_text().strip() if location_el else "Remote"
                href = link_el.get_attribute("href") if link_el else None

                if not (title and company and href):
                    continue

                apply_link = f"https://weworkremotely.com{href}" if href.startswith("/") else href

                if job_exists(apply_link):
                    consecutive_known += 1
                    if consecutive_known >= 5:
                        print("  5 consecutive known jobs — stopping.")
                        break
                    continue

                consecutive_known = 0
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "apply_link": apply_link,
                    "description": f"{title} at {company}. Location: {location}.",
                    "source": "WeWorkRemotely",
                })
            except Exception:
                continue

        browser.close()
    return jobs