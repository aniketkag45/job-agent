from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.routes.jobs import router as jobs_router
from app.core.exceptions import JobNotFoundException
from app.core.middleware import log_request_middleware
from app.api.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.agent_overview import router as agent_overview_router
from app.api.routes.resume import router as resume_router
from app.api.routes.profile import router as profile_router
from app.api.routes.notifications import router as notifications_router
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.services.database import init_db
    try:
        init_db()
        print("✅ DB initialized")
    except Exception as e:
        print(f"DB init failed: {e}")

    try:
        from scripts.run_job_pipeline import run_pipeline
        scheduler.add_job(run_pipeline, trigger="interval", hours=12, id="job_pipeline", replace_existing=True)
        scheduler.start()
        print("✅ Scheduler started every 12h")
    except Exception as e:
        print(f"Scheduler failed: {e}")

    yield
    try:
        scheduler.shutdown()
    except:
        pass

app = FastAPI(lifespan=lifespan)
app.middleware("http")(log_request_middleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(JobNotFoundException)
async def job_not_found_exception_handler(request: Request, exc: JobNotFoundException):
    return JSONResponse(status_code=404, content={"error": "Job not found", "message": f"Job with ID {exc.job_id} not found"})

@app.get("/")
def home():
    return {"message": "Job Agent API Running - Broad Feed + Bell + Google OAuth + Docker"}

app.include_router(jobs_router)
app.include_router(auth_router)
app.include_router(agent_overview_router)
app.include_router(resume_router)
app.include_router(profile_router)
app.include_router(notifications_router)