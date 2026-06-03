from fastapi import APIRouter, Query

from app.services.database import (

    delete_job,
    fetch_all_jobs_from_db,

    search_jobs,

    filter_jobs_by_source,

    query_jobs,

    create_job,

    update_job,

    fetch_diverse_recommended_jobs
)
from app.schemas.job_schema import JobSchema, JobCreateSchema
from app.schemas.response_schema import ApiResponse

from app.core.exceptions import JobNotFoundException


router = APIRouter()


@router.get("/jobs", response_model=ApiResponse)
def get_jobs(

      page: int = Query(

        default=1,

        ge=1
    ),

    page_size: int = Query(

        default=10,

        ge=1,

        le=100
    ),

    sort_by: str = "score",

    sort_order: str = "desc"
):

    jobs = fetch_all_jobs_from_db(

        page=page,

        page_size=page_size,

        sort_by=sort_by,

        sort_order=sort_order
    )

    return ApiResponse(
        success=True,

        data=jobs,

        message=f"Fetched {len(jobs)} jobs"
    )


@router.get("/jobs/search")
def search_jobs_endpoint(

    keyword: str,

    limit: int = 10
):

    jobs = search_jobs(

        keyword=keyword,

        limit=limit
    )

    return ApiResponse(
        success=True,

        data=jobs,

        message=f"Found {len(jobs)} jobs matching '{keyword}'"
    )


@router.get("/jobs/filter")
def filter_jobs(

    source: str,

    page: int = 1,

    page_size: int = 10
):

    jobs = filter_jobs_by_source(

        source=source,

        page=page,

        page_size=page_size
    )

    return ApiResponse(

        success=True,
        data=jobs,
        message=f"Found {len(jobs)} jobs from source '{source}'"
    )


@router.get("/jobs/query")
def query_jobs_endpoint(

    keyword: str = None,

    source: str = None,

    min_score: int = None,

    page: int = 1,

    page_size: int = 10,

    sort_by: str = "score",

    sort_order: str = "desc",
    location: str = None
):

    jobs = query_jobs(

        keyword=keyword,

        source=source,

        min_score=min_score,

        page=page,

        page_size=page_size,

        sort_by=sort_by,

        sort_order=sort_order,
        location=location
    )

    return ApiResponse(

        success=True,

        data=jobs,

        message=f"Found {len(jobs)} jobs matching '{keyword}'"
    )

@router.get("/jobs/recommendations")
def get_recommended_jobs(

    limit: int = 3
):

    jobs = fetch_diverse_recommended_jobs(
        limit=limit
    )

    return ApiResponse(

        success=True,

        data=jobs,

        message=f"Fetched {len(jobs)} recommended jobs"
    )
    

@router.post("/jobs", response_model=JobSchema)
def create_manual_job(job_data: JobCreateSchema):

    created_job = create_job(job_data)

    return created_job


@router.put("/jobs/{job_id}", response_model=JobSchema)
def update_existing_job(job_id: int, job_data: JobCreateSchema):
    updated_job = update_job(job_id, job_data)

    return updated_job

@router.delete("/jobs/{job_id}")
def delete_existing_job(job_id: int):
    deleted_count = delete_job(job_id)
    if deleted_count == 0:

     raise JobNotFoundException(job_id)
    return ApiResponse(
        success=True,

        message=f"Job with ID {job_id} deleted successfully"
    )
