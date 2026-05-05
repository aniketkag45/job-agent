import requests
import json
from bs4 import BeautifulSoup

def fetch_jobs():
    url = "https://realpython.github.io/fake-jobs/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="card-content")

    jobs= []

    for job in job_cards:
        title = job.find("h2", class_="title")
        company = job.find("h3", class_="company")
        location = job.find("p", class_="location")
        apply_link = job.find("a", string="Apply")
        if not (title and company and location and apply_link):
            continue  # Skip if any of the required fields are missing

        job_data = {
            "title": title.text.strip() if title else None,
            "company": company.text.strip() if company else None,
            "location": location.text.strip() if location else None,
            "apply_link": apply_link["href"] if apply_link else None
            }
        jobs.append(job_data)

    return jobs

def save_jobs_to_json(jobs):
    file_path = "scripts/jobs.json"
    with open(file_path,"w",encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)
    
    print(f"{len(jobs)}Jobs saved to {file_path}")
   

if __name__ == "__main__":
    jobs = fetch_jobs()
    if jobs:
        save_jobs_to_json(jobs)

        for job in jobs[:5]:
            print(job)

  
