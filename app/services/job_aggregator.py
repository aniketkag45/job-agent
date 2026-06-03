import time
from datetime import datetime

from app.services.job_experience_intelligence import extract_experience_level
from app.services.job_relevance_filter import (
    is_relevant_job
)

from app.services.source_registry import (
    SOURCE_REGISTRY
)

from app.services.job_normalizer import (
    normalize_job
)

from app.services.job_domain_filter import (
    is_domain_relevant
)

from app.services.pipeline_metrics import (
    increment_metric
)
from app.services.job_enrichment import extract_tech_stack
from app.services.semantic_representation import build_semantic_representation


def fetch_all_jobs():

    all_jobs = []


    for source in SOURCE_REGISTRY:

        start_time = time.time()

        scraper = source["scraper"]


        try:

            jobs = scraper()


            source["status"] = "healthy"

            source["last_success"] = (
                datetime.now().isoformat()
            )

            source["jobs_fetched"] = len(jobs)


            increment_metric(
                "jobs_fetched",
                len(jobs)
            )


            print(

                f"Fetched {len(jobs)} jobs "
                f"from {source['name']}."

            )


            for job in jobs:

                normalized_job = normalize_job(job)


                if not normalized_job:

                    continue


                if not is_domain_relevant(

                    normalized_job
                ):
                   
                    continue
                
               


                if not is_relevant_job(
                    normalized_job
                ):
                
                    continue

                normalized_job["experience_level"] = extract_experience_level(normalized_job)
                normalized_job["tech_stack"] = extract_tech_stack(normalized_job)
                normalized_job["semantic_representation"] = build_semantic_representation(normalized_job)

                print(
    "\nDEBUG:",
    normalized_job.get("title"),
    "| Source:",
    normalized_job.get("source"),
    "| Description Length:",
    len(
        normalized_job.get(
            "description",
            ""
        )
    )
)


                all_jobs.append(
                    normalized_job
                )


            source["last_run"] = (
                datetime.now().isoformat()
            )


            source["execution_time"] = round(

                time.time() - start_time,

                2
            )


        except Exception as error:

            source["status"] = "failing"

            source["failure_count"] += 1


            print(

                f"Source {source['name']} failed: "
                f"{error}"

            )


    return all_jobs