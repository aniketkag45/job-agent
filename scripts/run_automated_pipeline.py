import time
import schedule

from scripts.run_job_pipeline import run_pipeline

def scheduled_pipeline():
    print("\nScheduled pipeline triggered.")
    try:
     run_pipeline()
    except Exception as e:
        print(f"Error during pipeline execution: {e}")
schedule.every(1).minutes.do(scheduled_pipeline)
print("Automated job pipeline started...")
while True:
    schedule.run_pending()
    time.sleep(1)