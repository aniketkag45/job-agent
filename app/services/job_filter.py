def filter_jobs_by_keyword(jobs,keywords):
    filtered_jobs = []
    for job in jobs:
        title = job.get("title","").lower()
        for keyword in keywords:
            if keyword.lower() in title:
                filtered_jobs.append(job)
                break
    return filtered_jobs

EXCLUDED_KEYWORDS = [
    "senior",
    "staff",
    "lead",
    "principal",
    "manager",
    "director"
]


def filter_experience_level(jobs):

    filtered_jobs = []

    for job in jobs:

        title = (job.get("title") or "").lower()

        should_exclude = False

        for keyword in EXCLUDED_KEYWORDS:

            if keyword in title:

                should_exclude = True

                break

        if not should_exclude:

            filtered_jobs.append(job)

    return filtered_jobs

POSITIVE_KEYWORDS = {
    "intern": 5,
    "junior": 4,
    "entry": 4,
    "python": 3,
    "backend": 3,
    "software": 2
}


NEGATIVE_KEYWORDS = {
    "senior": -5,
    "lead": -4,
    "staff": -4,
    "principal": -5,
    "manager": -3
}

def score_jobs(jobs,preferences):
     preferred_keywords = preferences.get("preferred_keywords", [])
     excluded_keywords = preferences.get("excluded_keywords", [])
     preferred_locations = preferences.get("preferred_locations", [])
     remote_only = preferences.get("remote_only", False)

     scored_jobs = []

     for job in jobs:
         title = (job.get("title") or "").lower()
         location = (job.get("location") or "").lower()

         score = 0

         for keyword in preferred_keywords:
             if keyword.lower() in title:
                 score += 3
         for keyword in excluded_keywords:
             if keyword.lower() in title:
                 score -= 5
         for pref_loc in preferred_locations:
             if pref_loc.lower() in location:
                 score += 2
         if remote_only :
             if "remote" not in location:
                 continue
            

         job["score"] = score
         scored_jobs.append(job)
     scored_jobs.sort(key=lambda x: x["score"], reverse=True)
     return scored_jobs

    