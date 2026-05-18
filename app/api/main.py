from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

from app.api.routes.jobs import router as jobs_router
from app.core.exceptions import JobNotFoundException
from app.core.middleware import log_request_middleware
from app.api.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.middleware("http")(log_request_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(JobNotFoundException)
async def job_not_found_exception_handler(request: Request, exc: JobNotFoundException):
    
    return JSONResponse(

        status_code=404,

        content={
            "error": "Job not found",
            "message": f"Job with ID {exc.job_id} not found"
        }
    )

@app.get("/")
def home():

    return {

        "message": "Job Agent API Running"
    }


app.include_router(jobs_router)
app.include_router(auth_router)