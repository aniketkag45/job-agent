import time
import schedule
from app.main import main

def run_job_agent():
    print("Running Job Agent...")
    try:
     main()
    except Exception as e:
        print(f"Error running Job Agent: {e}")

# Schedule the job to run every minute
schedule.every(1).minutes.do(run_job_agent)

print("Job Agent Scheduler started. Running every minute...\n")

while True:
    schedule.run_pending()
    time.sleep(1)