from app.scraper.remoteok_scraper import fetch_remoteok_jobs
from app.scraper.greenhouse_scraper import fetch_greenhouse_jobs
from app.scraper.lever_scraper import fetch_lever_jobs
from app.scraper.weworkremotely_scraper import fetch_weworkremotely_jobs


SOURCE_REGISTRY = [

    {

    "name": "RemoteOK",

    "source_type": "job_board",

    "ats": "custom",

    "enabled": True,

    "status": "healthy",

    "last_run": None,

    "last_success": None,

    "failure_count": 0,

    "jobs_fetched": 0,

    "execution_time": 0,

    "scraper": fetch_remoteok_jobs
},

    {

        "name": "Greenhouse",

        "source_type": "ats",

        "ats": "greenhouse",

        "enabled": True,

        "status": "healthy",

        "last_run": None,

        "last_success": None,

        "failure_count": 0,

        "jobs_fetched": 0,

        "execution_time": 0,

        "scraper": fetch_greenhouse_jobs
    },
    {
        
        "name": "Lever",

        "source_type": "ats",

        "ats": "lever",

        "enabled": True,

        "status": "healthy",

        "last_run": None,

        "last_success": None,

        "failure_count": 0,

        "jobs_fetched": 0,

        "execution_time": 0,

        "scraper": fetch_lever_jobs
    },
        {
        "name": "WeWorkRemotely",
        "source_type": "job_board",
        "ats": "custom",
        "enabled": True,
        "status": "healthy",
        "last_run": None,
        "last_success": None,
        "failure_count": 0,
        "jobs_fetched": 0,
        "execution_time": 0,
        "scraper": fetch_weworkremotely_jobs,
    },
        
    
]
