from playwright.sync_api import sync_playwright
from app.services.database import job_exists


REMOTEOK_URL = (
    "https://remoteok.com/remote-dev-jobs"
)


def fetch_remoteok_jobs():

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            REMOTEOK_URL,
            timeout=60000
        )

        page.wait_for_timeout(5000)

        # Select all job rows
        job_cards = page.query_selector_all(
            "tr.job"
        )

        print(
            f"\nFound {len(job_cards)} "
            f"job cards"
        )

        consecutive_known_jobs = 0

        for card in job_cards:

            try:
                

                title_element = card.query_selector(
                    "h2"
                )

                company_element = (
                    card.query_selector(
                        "h3"
                    )
                )

                link_element = (
                    card.query_selector(
                        "a.preventLink"
                    )
                )

                location_element = (
                    card.query_selector(
                        ".location"
                    )
                )

                tag_elements = (
                    card.query_selector_all(
                        ".tag"
                    )
                )


                title = (
                    title_element.inner_text().strip()
                    if title_element
                    else None
                )

                company = (
                    company_element.inner_text().strip()
                    if company_element
                    else None
                )

                location = (
                    location_element.inner_text().strip()
                    if location_element
                    else "Remote"
                )
                tags = []
                for tag in tag_elements:
                    tag_text = tag.inner_text().strip()
                    if tag_text:
                        tags.append(tag_text)

                apply_link = None

                if link_element:

                    href = link_element.get_attribute(
                        "href"
                    )

                    if href:

                        apply_link = (
                            "https://remoteok.com"
                            + href
                        )

                if not (
                    title
                    and company
                    and apply_link
                ):

                    continue

                normalized_job = {

                    "title": title,

                    "company": company,

                    "location": location,

                    "apply_link": apply_link,

                    "description": " ".join(tags),

                    "source": "RemoteOK"
                }
                if job_exists(apply_link):
                    consecutive_known_jobs += 1
                    print(
                        f"Known RemoteOK job detected "
                        f"({consecutive_known_jobs}/5)"
                    )
                    if consecutive_known_jobs >= 5:
                        print(
                            "Encountered 5 consecutive known jobs. "
                            "Stopping early ingestion for RemoteOK."
                        )
                        break
                    continue
                consecutive_known_jobs = 0

                jobs.append(normalized_job)

            except Exception as e:

                print(
                    f"Error parsing job card: {e}"
                )

        browser.close()

    return jobs