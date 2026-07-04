import traceback
import time
from datetime import datetime

from app.services.job_aggregator import fetch_all_jobs
from app.services.job_deduplicator import deduplicator_jobs
from app.services.job_filter import score_jobs
from app.utils.config_loader import load_user_preferences

from app.services.database import (
    insert_job,
    fetch_unnotified_jobs,
    mark_job_as_notified,
    job_exists
)

from app.notifier.telegram_notifier import (
    send_telegram_message
)

from app.services.pipeline_metrics import (
    increment_metric,
    reset_metrics,
    get_metrics 
)

from app.services.embedding_service import generate_embedding
from app.services.job_matcher import match_jobs_to_candidate


def run_pipeline():

    start_time = time.time()

    reset_metrics()

    run_started_at = datetime.now().isoformat()

    jobs_fetched_count = 0
    jobs_inserted_count = 0
    alerts_sent_count = 0

    try:

        print("\nStarting job pipeline...\n")

        jobs = fetch_all_jobs()

        jobs_fetched_count = len(jobs)

        print(
            f"Fetched {jobs_fetched_count} jobs from sources."
        )

        jobs = deduplicator_jobs(jobs)

        print(
            f"{len(jobs)} jobs after deduplication."
        )

        preferences = load_user_preferences()

        jobs = score_jobs(
            jobs,
            preferences
        )

        print(
            "Scored jobs based on user preferences."
        )

        for job in jobs:
            apply_link = job.get("apply_link")
            if job_exists(apply_link):
                increment_metric("duplicates_skipped")
                continue

            was_inserted = insert_job(job)

            if was_inserted:

                jobs_inserted_count += 1

                increment_metric(
                    "jobs_inserted"
                )

        print(
            "\nJobs saved to database."
        )

        unnotified_jobs = fetch_unnotified_jobs()

        print(
            f"\nFound {len(unnotified_jobs)} unnotified jobs."
        )

        scored_for_alert = []
        try:
            import json,os
            profile_path = os.path.join("storage","candidate_profile.json")
            if os.path.exists(profile_path):
                with open(profile_path) as f:
                    candidate_data = json.load(f)

                candidate_embedding = candidate_data.get("embedding")
                candidate_skills = candidate_data.get("profile", {}).get("skills", [])

                if candidate_embedding and candidate_skills:
                     print(f"\n using candidate profile for alert ({len(candidate_skills)} skills)")
                     matches = match_jobs_to_candidate(
                          candidate_embedding = candidate_embedding,
                            candidate_skills = candidate_skills,
                            top_k = min(len(unnotified_jobs), 50),
                            semantic_weight = 0.6,
                     )
                     hybrid_scores = {match["job_id"]: match["hybrid_score"] for match in matches}

                     for job in unnotified_jobs:
                          keyword_score = job.get("score", 0)
                          ai_score = hybrid_scores.get(job["id"], 0)
                          combined = (keyword_score * 0.5) + (ai_score * 50)

                          scored_for_alert.append((job, combined))
                else:
                  raise Exception("No embedding in profile")
            else:
              raise Exception("Candidate profile not found for alert scoring")
        except Exception as e:
            print(f"\nNo candidate profile for alerts ({e}). Using keyword scores only.")
            for job in unnotified_jobs:
                scored_for_alert.append((job, job.get("score", 0)))

        scored_for_alert.sort(key=lambda x: x[1], reverse=True)
        top_jobs = [job for job, score in scored_for_alert[:5]]



        for job in top_jobs[:5]:

            message = f"""
🚀 New Job Found!

💼 {job['title']}

🏢 {job['company']}

📍 {job['location']}

⭐ Score: {job['score']}

🔗 {job['apply_link']}
"""

            send_telegram_message(message)

            alerts_sent_count += 1

            increment_metric(
                "alerts_sent"
            )

            mark_job_as_notified(
                job["id"]
            )

        execution_time = (
            time.time() - start_time
        )

        metrics = get_metrics()

        from app.services.database import get_session,PipelineRun
        with get_session() as session:
            run = PipelineRun(
                run_started_at = run_started_at,
                run_completed_at = datetime.now().isoformat(),
                jobs_fetched = jobs_fetched_count,
                jobs_inserted = jobs_inserted_count,
                jobs_filtered = metrics["jobs_filtered"],
                duplicates_skipped = metrics["duplicates_skipped"],
                scraper_failures = metrics["scraper_failures"],
                alerts_sent = alerts_sent_count,
                status = "SUCCESS",
                execution_time_seconds = execution_time,
                
            )
            session.add(run)
        
         # Cleanup old jobs
        from app.services.database import cleanup_old_jobs
        deleted = cleanup_old_jobs()
        print(f"\nCleaned up {deleted} old jobs.")

        print("\nPipeline Metrics Summary:\n")

        for key, value in metrics.items():

            print(f"{key}: {value}")

        print(
            f"\nPipeline execution completed in {execution_time:.2f} seconds."
        )

    except Exception as error:

        execution_time = (
            time.time() - start_time
        )

        metrics = get_metrics()

        from app.services.database import get_session,PipelineRun
        with get_session() as session:
            run = PipelineRun(
                run_started_at = run_started_at,
                run_completed_at = datetime.now().isoformat(),
                jobs_fetched = jobs_fetched_count,
                jobs_inserted = jobs_inserted_count,
                jobs_filtered = metrics["jobs_filtered"],
                duplicates_skipped = metrics["duplicates_skipped"],
                scraper_failures = metrics["scraper_failures"],
                alerts_sent = alerts_sent_count,
                status = "FAILED",
                error_message = str(error),
                execution_time_seconds = execution_time
            )
            session.add(run)

        traceback.print_exc()


if __name__ == "__main__":

    run_pipeline()