import re

ENTRY_LEVEL_KEYWORDS = [

    "intern",

    "internship",

    "junior",

    "graduate",

    "new grad",

    "entry level",

    "fresher"
]


MID_LEVEL_KEYWORDS = [

    "mid level",

    "mid-level",

    "associate"
]


SENIOR_LEVEL_KEYWORDS = [

    "senior",

    "staff",

    "lead",

    "principal",

    "manager",

    "director",

    "architect"
]

def extract_experience_level(job):
    
    title = (
        job.get("title") or ""
    ).lower()


    for keyword in ENTRY_LEVEL_KEYWORDS:

        if keyword in title:

            return "entry"


    for keyword in MID_LEVEL_KEYWORDS:

        if keyword in title:

            return "mid"


    for keyword in SENIOR_LEVEL_KEYWORDS:

        if keyword in title:

            return "senior"


    return "unknown"

def extract_years_of_experience(job):

    title = (
        job.get("title") or ""
    ).lower()


    patterns = [

        r"(\d+)\+?\s*years",

        r"(\d+)\+?\s*yrs",

        r"(\d+)\+?\s*year"
    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            title
        )

        if match:

            return int(
                match.group(1)
            )


    return None