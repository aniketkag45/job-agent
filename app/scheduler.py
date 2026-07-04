from apscheduler.schedulers.blocking import BlockingScheduler

from scripts.run_job_pipeline import run_pipeline


scheduler = BlockingScheduler()


scheduler.add_job(

    run_pipeline,

    trigger="interval",

    hours=12,

    id="job_pipeline",

    replace_existing=True
)