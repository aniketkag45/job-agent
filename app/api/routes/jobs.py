import os,json
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from fastapi import HTTPException
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
from app.services.job_matcher import semantic_search
from app.services.job_matcher import match_jobs_to_candidate
from app.api.routes.resume import load_profile
from app.auth.dependencies import get_current_user

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

    sort_order: str = "desc",

    filter: str = Query(default=None, description=" ' today' for last 24 hrs jobs"),
):

    from app.services.database import get_session, Job, _job_to_dict
    from datetime import datetime, timedelta

    if filter == "today":
        yesterday = (datetime.now() - timedelta(hours=24)).isoformat()
        with get_session() as session:
            total = session.query(Job).filter(
                Job.scraped_at >= yesterday,
                Job.applied_at == None
            ).count()
            all_jobs = session.query(Job).filter(
                Job.scraped_at >= yesterday,
                Job.applied_at == None
            ).order_by(Job.score.desc()).offset((page - 1) * page_size).limit(page_size).all()
            jobs = [_job_to_dict(j) for j in all_jobs]
    else:
        jobs = fetch_all_jobs_from_db(
            page=page, page_size=page_size,
            sort_by=sort_by, sort_order=sort_order
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

    limit: int = 3, current_user: dict = Depends(get_current_user)
):

    jobs = fetch_diverse_recommended_jobs(
        limit=limit
    )

    return ApiResponse(

        success=True,

        data=jobs,

        message=f"Fetched {len(jobs)} recommended jobs"
    )

@router.get("/jobs/semantic-search")
def semantic_search_endpoint(
     query: str = Query(..., description="Natural language like 'python backend intern remote'"),
    top_k: int = Query(default=10, ge=1, le=50),
    source: str = Query(default=None, description="Filter: 'RemoteOK', 'Greenhouse'"),
    current_user: dict = Depends(get_current_user)
):
    results = semantic_search(
        query=query,
        top_k=top_k,
        filter_source=source
    )

    return ApiResponse(
        success=True,
        data=results,
        message=f"Found {len(results)} semantically similar jobs for query '{query}'"
    )

@router.get("/jobs/for-me")
def get_jobs_for_my_profile(
    top_k: int = Query(default=10, ge=1, le=50),
    semantic_weight: float = Query(default=0.6, ge=0.0, le=1.0),
    current_user: dict = Depends(get_current_user)
):
    candidate_data = load_profile()
    if candidate_data is None:
        return ApiResponse(
            success=False,
            data=None,
            message="No resume uploaded. POST to /resume/upload first, then come back."
        )
    candidate_embedding = candidate_data.get("embedding")
    candidate_skills = candidate_data.get("profile", {}).get("skills", [])
    if not candidate_embedding:
        return ApiResponse(
            success=False,
            data=None,
            message="Candidate profile is missing embedding. Please re-upload your resume."
        )
    matches = match_jobs_to_candidate(
        candidate_embedding=candidate_embedding,
        candidate_skills=candidate_skills,
        top_k=min(top_k*3, 50),  # fetch more for better hybrid scoring
        semantic_weight=semantic_weight
    )
    matches = [m for m in matches if m.get("score", -999) >= -20]
    ENTRY_KEYWORDS = ["intern", "new grad", "junior", "entry level", "graduate", "fresher"]
    SENIOR_KEYWORDS = ["senior", "staff", "principal", "lead", "manager", "director", "head of"]

    for match in matches:
        title_lower = match.get("title", "").lower()
        
        # Check entry-level first (stronger boost for student candidates)
        is_entry = any(kw in title_lower for kw in ENTRY_KEYWORDS)
        is_senior = any(kw in title_lower for kw in SENIOR_KEYWORDS)
        
        if is_entry:
            match["hybrid_score"] = round(match["hybrid_score"] + 0.40, 4)
        elif is_senior:
            match["hybrid_score"] = round(match["hybrid_score"] - 0.20, 4)

    matches.sort(key=lambda x: x["hybrid_score"], reverse=True)
    return ApiResponse(
        success=True,
        data=matches,
        message=f"Found {len(matches)} jobs matching your profile with semantic weight {semantic_weight}"
    )

@router.get("/jobs/{job_id}/explain")
def explain_job_match(job_id: int, current_user: dict = Depends(get_current_user)):
    candidate_data = load_profile()
    if candidate_data is None:
        return ApiResponse(
            success=False,
            data=None,
            message="No resume uploaded. POST to /resume/upload first, then come back."
        )
    candidate_profile = candidate_data.get("profile", {})
    candidate_skills = candidate_data.get("profile", {}).get("skills", [])
    from app.services.database import get_session,Job
    with get_session() as session:
        row = session.query(Job).filter(Job.id == job_id).first()
   
    if not row:
        return ApiResponse(
            success=False,
            data=None,
            message=f"No job found with ID {job_id}"
        )
    job = {
        "title": row.title,
        "company": row.company,
        "location": row.location,
        "description": row.semantic_text or "",
        "tech_stack": [],  # Assuming tech stack is not stored separately, we can extract
    }
    explanation = None
    try:
        from app.services.llm_service import explain_match
        explanation = explain_match(job, candidate_profile)
    except Exception as e:
        pass
    matched = []
    if explanation is None:
        matched = [s for s in candidate_skills if s.lower() in job["description"].lower()]
        if matched:
            explanation = (
                f"Skills matched: {', '.join(matched)}. "
                f"Your profile has {len(candidate_skills)} skills — "
                f"{len(matched)} appear in this job description."
            )
        else:
            explanation = "No specific skills from your profile were found in the job description, but it may still be a good match based on other factors."
    return ApiResponse(
        success=True,
        data={
            "job": {"title": job["title"], "company": job["company"]},
            "explanation": explanation,
            "matched_skills": matched if 'matched' in dir() else [],
        },
        message=f"Explanation for why job ID {job_id} matches your profile"
    )

@router.get("/jobs/{job_id}/cover-letter")
def generate_cover_letter(job_id: int,
                          candidate_name: str = 'Candidate',
                          current_user: dict = Depends(get_current_user)):
    
    candidate_data = load_profile()
    if candidate_data is None:
        return ApiResponse(
            success=False,
            data=None,
            message="No resume uploaded. POST to /resume/upload first, then come back."
        )
    candidate_profile = candidate_data.get("profile", {})
    from app.services.database import get_session,Job
    with get_session() as session:
        row = session.query(Job).filter(Job.id == job_id).first()
    if not row:
        return ApiResponse(
            success=False,
            data=None,
            message=f"No job found with ID {job_id}"
        )
    job = {
        "title": row.title,
        "company": row.company,
        "location": row.location,
        "description": row.semantic_text or "",
        "tech_stack": [],  # Assuming tech stack is not stored separately, we can extract
    }
    cover_letter = None
    try:
        from app.services.llm_service import generate_cover_letter
        cover_letter = generate_cover_letter(job, candidate_profile, candidate_name)
    except Exception as e:
        pass
    if cover_letter is None:
        cover_letter = (
            f"Dear Hiring Manager,\n\n"
            f"I am writing to express my interest in the {job['title']} position "
            f"at {job['company']}.\n\n"
            f"[LLM not configured — set LLM_API_KEY in .env for an AI-written letter]\n\n"
            f"Sincerely,\n{candidate_name}"
        )
    return ApiResponse(
        success=True,
        data={
            "job": {"title": job["title"], "company": job["company"]},
            "cover_letter": cover_letter,
        },
        message=f"Generated cover letter for job ID {job_id}"
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


@router.post("/jobs/{job_id}/apply")
def apply_to_job(job_id: int, current_user: dict = Depends(get_current_user)):
    """
    Mark a job as applied by the current user.
    Also marks the job's applied_at timestamp.
    """
    from app.services.database import get_session, User, Job, UserApplication
    from app.services.email_service import send_email, is_configured

    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        job = session.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        # Check if already applied
        existing = session.query(UserApplication).filter(
            UserApplication.user_id == user.id,
            UserApplication.job_id == job_id
        ).first()
        if existing:
            return ApiResponse(success=True, message="Already applied.")

        # Create application record
        now = datetime.now().isoformat()
        app = UserApplication(user_id=user.id, job_id=job_id, applied_at=now, source="manual")
        session.add(app)

        # Mark job as applied
        job.applied_at = now

        # Send confirmation email (non-blocking — if configured)
        if is_configured():
            try:
                subject = f"Application Submitted — {job.title} at {job.company}"
                body = f"""
                <div style="font-family: Inter, sans-serif; max-width: 600px; padding: 30px;">
                    <h2 style="color: #14213D;">Application Submitted ✓</h2>
                    <p>You've applied to:</p>
                    <div style="background: #F8F4F1; padding: 16px; border-radius: 12px; margin: 16px 0;">
                        <strong>{job.title}</strong><br/>
                        {job.company} · {job.location}
                    </div>
                    <p style="color: #667085;">Track your applications from the dashboard.</p>
                </div>
                """
                send_email(user.email, subject, body)
            except Exception:
                pass  # Email failure shouldn't block apply

        return ApiResponse(success=True, message=f"Applied to {job.title} at {job.company}.")


@router.get("/jobs/applied")
def get_applied_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
):
    """
    Get jobs the current user has applied to.
    Returns most recently applied first.
    """
    from app.services.database import get_session, User, Job, UserApplication

    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        offset = (page - 1) * page_size
        applications = (
            session.query(UserApplication, Job)
            .join(Job, UserApplication.job_id == Job.id)
            .filter(UserApplication.user_id == user.id)
            .order_by(UserApplication.applied_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        results = []
        for app, job in applications:
            results.append({
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "apply_link": job.apply_link,
                "source": job.source,
                "score": job.score,
                "applied_at": app.applied_at,
                "application_source": app.source,
            })

        return ApiResponse(success=True, data=results, message=f"Found {len(results)} applied jobs.")