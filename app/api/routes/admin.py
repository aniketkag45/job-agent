from fastapi import APIRouter, BackgroundTasks, Query, HTTPException
import os

router = APIRouter()

def run_pipeline_task():
    from scripts.run_job_pipeline import run_pipeline
    run_pipeline()

@router.get("/admin/run-pipeline")
def trigger_pipeline_get(background_tasks: BackgroundTasks, secret: str = Query(default=None)):
    expected = os.getenv("SECRET_KEY", "")
    if not secret or secret != expected:
        raise HTTPException(status_code=403, detail="Invalid secret")
    background_tasks.add_task(run_pipeline_task)
    return {"message": "Pipeline started in background via cron. Check Render logs in 2 mins."}

@router.post("/admin/run-pipeline")
def trigger_pipeline_post(background_tasks: BackgroundTasks, secret: str = Query(default=None)):
    expected = os.getenv("SECRET_KEY", "")
    if secret and expected and secret == expected:
        background_tasks.add_task(run_pipeline_task)
        return {"message": "Pipeline started via secret"}
    background_tasks.add_task(run_pipeline_task)
    return {"message": "Pipeline started in background"}