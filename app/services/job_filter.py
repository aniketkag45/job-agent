from app.services.job_experience_intelligence import extract_experience_level,extract_years_of_experience
def filter_jobs_by_keyword(jobs, keywords):

    filtered_jobs = []

    for job in jobs:

        title = (
            job.get("title", "")
        ).lower()

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

        title = (
            job.get("title") or ""
        ).lower()


        should_exclude = False


        for keyword in EXCLUDED_KEYWORDS:

            if keyword in title:

                should_exclude = True

                break


        if not should_exclude:

            filtered_jobs.append(job)


    return filtered_jobs


# =========================================
# PRIORITY-BASED RECOMMENDATION ENGINE
# =========================================

HIGH_PRIORITY_KEYWORDS = {

    "ai": 12,

    "machine learning": 12,

    "ml": 10,

    "llm": 15,

    "artificial intelligence": 12,

    "deep learning": 12,

    "backend": 9,

    "python": 8,

    "data engineer": 8,

    "software engineer": 7,

    "intern": 10,

    "new grad": 9,

    "graduate": 8,

    "junior": 8
}


MEDIUM_PRIORITY_KEYWORDS = {

    "frontend": 5,

    "react": 5,

    "full stack": 6,

    "fullstack": 6,

    "cloud": 5,

    "platform": 5,

    "devops": 5,

    "web": 4
}


LOW_PRIORITY_KEYWORDS = {

    "senior": -8,

    "staff": -10,

    "lead": -10,

    "manager": -12,

    "director": -15,

    "principal": -12
}


def score_jobs(jobs, preferences):

    preferred_keywords = preferences.get(
        "preferred_keywords",
        []
    )

    excluded_keywords = preferences.get(
        "excluded_keywords",
        []
    )

    preferred_locations = preferences.get(
        "preferred_locations",
        []
    )

    remote_only = preferences.get(
        "remote_only",
        False
    )


    scored_jobs = []


    for job in jobs:

        title = (
            job.get("title") or ""
        ).lower()

        location = (
            job.get("location") or ""
        ).lower()


        score = 0


        # =========================================
        # USER PERSONALIZATION SIGNALS
        # =========================================

        for keyword in preferred_keywords:

            if keyword.lower() in title:

                score += 5


        for keyword in excluded_keywords:

            if keyword.lower() in title:

                score -= 10


        for pref_loc in preferred_locations:

            if pref_loc.lower() in location:

                score += 3


        if remote_only:

            if "remote" in location:

                score += 5

            else:

                score -= 5


        # =========================================
        # SYSTEM PRIORITY SIGNALS
        # =========================================

        for keyword, weight in HIGH_PRIORITY_KEYWORDS.items():

            if keyword in title:

                score += weight


        for keyword, weight in MEDIUM_PRIORITY_KEYWORDS.items():

            if keyword in title:

                score += weight


        for keyword, weight in LOW_PRIORITY_KEYWORDS.items():

            if keyword in title:

                score += weight


        # =========================================
        # FINAL SCORE ASSIGNMENT
        # =========================================
        experiance_level = extract_experience_level(job)
        years_required = extract_years_of_experience(job)

        if experiance_level == "entry":

            score += 10

        elif experiance_level == "mid":

            score += 2

        elif experiance_level == "senior":
            score -= 5

        if years_required:
            if years_required >= 5:
                score -= 4
            elif years_required >= 3:
                score -= 2 
            elif years_required <= 1:
                score += 5

        job["score"] = score

        scored_jobs.append(job)


    # =========================================
    # SORT HIGHEST SCORE FIRST
    # =========================================

    scored_jobs.sort(

        key=lambda x: x["score"],

        reverse=True
    )


    return scored_jobs