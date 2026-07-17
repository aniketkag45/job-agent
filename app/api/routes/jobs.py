import os, json
from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import datetime, timedelta
from app.services.database import (
    delete_job,
    fetch_all_jobs_from_db,
    search_jobs,
    filter_jobs_by_source,
    query_jobs,
    create_job,
    update_job,
    fetch_diverse_recommended_jobs,
    get_session,
    Job,
    User,
    _job_to_dict
)
from app.schemas.job_schema import JobSchema, JobCreateSchema
from app.schemas.response_schema import ApiResponse
from app.core.exceptions import JobNotFoundException
from app.services.job_matcher import semantic_search
from app.auth.dependencies import get_current_user
from app.services.candidate_retrieval_service import get_personalized_jobs, get_user_candidate_data

router = APIRouter()

@router.get("/jobs", response_model=ApiResponse)
def get_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sort_by: str = "score",
    sort_order: str = "desc",
    filter: str = Query(default=None, description="'today' for last 24 hrs jobs"),
    current_user: dict = Depends(get_current_user),
):
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id

    from app.services.candidate_retrieval_service import get_broad_engineering_feed
    try:
        # Broad engineering feed: ALL engineering jobs sorted with resume priority first
        broad = get_broad_engineering_feed(user_id=user_id, page=page, page_size=page_size)
        if filter == "today":
            from datetime import datetime, timedelta
            yesterday = (datetime.now() - timedelta(hours=24)).isoformat()
            broad = [j for j in broad if j.get("scraped_at","") >= yesterday]
        
        return ApiResponse(
            success=True,
            data=broad,
            message=f"Fetched {len(broad)} engineering jobs (resume priority on top, all engineering to explore)"
        )
    except Exception as e:
        print(f"Broad feed failed: {e}, fallback to global")
        if filter == "today":
            yesterday = (datetime.now() - timedelta(hours=24)).isoformat()
            with get_session() as session:
                all_jobs = session.query(Job).filter(Job.scraped_at >= yesterday, Job.applied_at == None).order_by(Job.score.desc()).offset((page-1)*page_size).limit(page_size).all()
                jobs = [_job_to_dict(j) for j in all_jobs]
        else:
            jobs = fetch_all_jobs_from_db(page=page, page_size=page_size, sort_by=sort_by, sort_order=sort_order)
        return ApiResponse(success=True, data=jobs, message=f"Fetched {len(jobs)} jobs (global fallback)")
    
    
@router.get("/jobs/search")
def search_jobs_endpoint(keyword: str, limit: int = 10, current_user: dict = Depends(get_current_user)):
    jobs = search_jobs(keyword=keyword, limit=limit)
    return ApiResponse(success=True, data=jobs, message=f"Found {len(jobs)} jobs matching '{keyword}'")


@router.get("/jobs/filter")
def filter_jobs(source: str, page: int = 1, page_size: int = 10, current_user: dict = Depends(get_current_user)):
    jobs = filter_jobs_by_source(source=source, page=page, page_size=page_size)
    return ApiResponse(success=True, data=jobs, message=f"Found {len(jobs)} jobs from source '{source}'")


@router.get("/jobs/query")
def query_jobs_endpoint(
    keyword: str = None,
    source: str = None,
    min_score: int = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "score",
    sort_order: str = "desc",
    location: str = None,
    current_user: dict = Depends(get_current_user)
):
    jobs = query_jobs(keyword=keyword, source=source, min_score=min_score, page=page, page_size=page_size, sort_by=sort_by, sort_order=sort_order, location=location)
    return ApiResponse(success=True, data=jobs, message=f"Found {len(jobs)} jobs matching query")


@router.get("/jobs/recommendations")
def get_recommended_jobs(limit: int = 3, current_user: dict = Depends(get_current_user)):
    # Now returns personalized diverse recommendations
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        personalized = get_personalized_jobs(user_id=user.id, top_k=limit*3)
        if personalized:
            # Diverse: unique titles
            seen = set()
            diverse = []
            for j in personalized:
                key = j["title"].strip().lower()
                if key not in seen:
                    seen.add(key)
                    diverse.append(j)
                if len(diverse) >= limit:
                    break
            return ApiResponse(success=True, data=diverse, message=f"Fetched {len(diverse)} personalized recommendations")

    # Fallback
    jobs = fetch_diverse_recommended_jobs(limit=limit)
    return ApiResponse(success=True, data=jobs, message=f"Fetched {len(jobs)} recommended jobs (global)")


@router.get("/jobs/semantic-search")
def semantic_search_endpoint(
     query: str = Query(..., description="Natural language like 'python backend intern remote'"),
    top_k: int = Query(default=10, ge=1, le=50),
    source: str = Query(default=None, description="Filter: 'RemoteOK', 'Greenhouse'"),
    current_user: dict = Depends(get_current_user)
):
    results = semantic_search(query=query, top_k=top_k, filter_source=source)
    return ApiResponse(success=True, data=results, message=f"Found {len(results)} semantically similar jobs for query '{query}'")


@router.get("/jobs/for-me")
def get_jobs_for_my_profile(
    top_k: int = Query(default=10, ge=1, le=50),
    semantic_weight: float = Query(default=0.6, ge=0.0, le=1.0),
    current_user: dict = Depends(get_current_user)
):
    """
    Now uses DB per-user retrieval, not candidate_profile.json file.
    """
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id

    jobs = get_personalized_jobs(user_id=user_id, top_k=top_k, semantic_weight=semantic_weight)
    if not jobs:
        return ApiResponse(success=False, data=None, message="No resume uploaded or no matches. POST to /resume/upload first.")
    return ApiResponse(success=True, data=jobs, message=f"Found {len(jobs)} jobs matching your profile with weight {semantic_weight}")


@router.get("/jobs/{job_id}/explain")
def explain_job_match(job_id: int, current_user: dict = Depends(get_current_user)):
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id

    candidate = get_user_candidate_data(user_id)
    if not candidate:
        return ApiResponse(success=False, data=None, message="No resume uploaded. POST to /resume/upload first.")

    candidate_skills = candidate.get("skills", [])
    candidate_profile = {"skills": candidate_skills, "experience_level": candidate.get("experience_level")}

    with get_session() as session:
        row = session.query(Job).filter(Job.id == job_id).first()
    if not row:
        return ApiResponse(success=False, data=None, message=f"No job found with ID {job_id}")

    job = {"title": row.title, "company": row.company, "location": row.location, "description": row.semantic_text or "", "tech_stack": []}
    explanation = None
    try:
        from app.services.llm_service import explain_match
        explanation = explain_match(job, candidate_profile)
    except Exception:
        pass

    matched = []
    if explanation is None:
        matched = [s for s in candidate_skills if s.lower() in job["description"].lower()]
        if matched:
            explanation = f"Skills matched: {', '.join(matched)}. Your profile has {len(candidate_skills)} skills — {len(matched)} appear in this job."
        else:
            explanation = "No specific skills from your profile were found, but it may still be a good match based on other factors."

    return ApiResponse(success=True, data={"job": {"title": job["title"], "company": job["company"]}, "explanation": explanation, "matched_skills": matched}, message=f"Explanation for job ID {job_id}")


@router.get("/jobs/{job_id}/cover-letter")
def generate_cover_letter(job_id: int, candidate_name: str = 'Candidate', current_user: dict = Depends(get_current_user)):
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id

    candidate = get_user_candidate_data(user_id)
    if not candidate:
        return ApiResponse(success=False, data=None, message="No resume uploaded. POST to /resume/upload first.")
    candidate_profile = {"skills": candidate.get("skills", []), "experience_level": candidate.get("experience_level")}

    with get_session() as session:
        row = session.query(Job).filter(Job.id == job_id).first()
    if not row:
        return ApiResponse(success=False, data=None, message=f"No job found with ID {job_id}")

    job = {"title": row.title, "company": row.company, "location": row.location, "description": row.semantic_text or "", "tech_stack": []}
    cover_letter = None
    try:
        from app.services.llm_service import generate_cover_letter as gen_letter
        cover_letter = gen_letter(job, candidate_profile, candidate_name)
    except Exception:
        pass
    if cover_letter is None:
        cover_letter = f"Dear Hiring Manager,\n\nI am writing to express my interest in the {job['title']} position at {job['company']}.\n\n[LLM not configured — set LLM_API_KEY]\n\nSincerely,\n{candidate_name}"

    return ApiResponse(success=True, data={"job": {"title": job["title"], "company": job["company"]}, "cover_letter": cover_letter}, message=f"Generated cover letter for job ID {job_id}")


@router.post("/jobs", response_model=JobSchema)
def create_manual_job(job_data: JobCreateSchema, current_user: dict = Depends(get_current_user)):
    created_job = create_job(job_data)
    return created_job


@router.put("/jobs/{job_id}", response_model=JobSchema)
def update_existing_job(job_id: int, job_data: JobCreateSchema, current_user: dict = Depends(get_current_user)):
    updated_job = update_job(job_id, job_data)
    return updated_job


@router.delete("/jobs/{job_id}")
def delete_existing_job(job_id: int, current_user: dict = Depends(get_current_user)):
    deleted_count = delete_job(job_id)
    if deleted_count == 0:
        raise JobNotFoundException(job_id)
    return ApiResponse(success=True, message=f"Job with ID {job_id} deleted successfully")


@router.post("/jobs/{job_id}/apply")
def apply_to_job(job_id: int, current_user: dict = Depends(get_current_user)):
    from app.services.database import User, Job, UserApplication
    from app.services.email_service import send_email, is_configured
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        job = session.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        existing = session.query(UserApplication).filter(UserApplication.user_id == user.id, UserApplication.job_id == job_id).first()
        if existing:
            return ApiResponse(success=True, message="Already applied.")
        now = datetime.now().isoformat()
        app = UserApplication(user_id=user.id, job_id=job_id, applied_at=now, source="manual")
        session.add(app)
        job.applied_at = now
        if is_configured():
            try:
                subject = f"Application Submitted — {job.title} at {job.company}"
                body = f"""<div style="font-family: Inter, sans-serif; max-width: 600px; padding: 30px;"><h2 style="color: #14213D;">Application Submitted ✓</h2><p>You've applied to:</p><div style="background: #F8F4F1; padding: 16px; border-radius: 12px; margin: 16px 0;"><strong>{job.title}</strong><br/>{job.company} · {job.location}</div></div>"""
                send_email(user.email, subject, body)
            except Exception:
                pass
        return ApiResponse(success=True, message=f"Applied to {job.title} at {job.company}.")


@router.get("/jobs/applied")
def get_applied_jobs(page: int = Query(default=1, ge=1), page_size: int = Query(default=10, ge=1, le=50), current_user: dict = Depends(get_current_user)):
    from app.services.database import User, Job, UserApplication
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        offset = (page - 1) * page_size
        applications = session.query(UserApplication, Job).join(Job, UserApplication.job_id == Job.id).filter(UserApplication.user_id == user.id).order_by(UserApplication.applied_at.desc()).offset(offset).limit(page_size).all()
        results = []
        for app, job in applications:
            results.append({"id": job.id, "title": job.title, "company": job.company, "location": job.location, "apply_link": job.apply_link, "source": job.source, "score": job.score, "applied_at": app.applied_at, "application_source": app.source})
        return ApiResponse(success=True, data=results, message=f"Found {len(results)} applied jobs.")