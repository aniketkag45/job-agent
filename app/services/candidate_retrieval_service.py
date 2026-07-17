"""
Candidate Retrieval Service — Broad Engineering Feed with Resume Priority
Shows ALL engineering jobs sorted with resume matches on top (your ask)
"""

import json
import logging
from typing import List, Dict, Any, Optional
from app.services.database import get_session, UserProfile, UserResume, Job, _job_to_dict
from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_similar_jobs

logger = logging.getLogger(__name__)

ENTRY_KEYWORDS = ["intern", "new grad", "junior", "entry level", "graduate", "fresher"]
SENIOR_KEYWORDS = ["senior", "staff", "principal", "lead", "manager", "director", "head of"]

def _safe_json_list(raw: str) -> List[str]:
    if not raw:
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [str(x).lower() for x in data if x]
        return []
    except:
        return []

def _keyword_overlap(text: str, skills: List[str]) -> float:
    if not skills or not text:
        return 0.0
    text_l = text.lower()
    matches = sum(1 for s in skills if s.lower() in text_l)
    return float(matches) / float(len(skills)) if skills else 0.0

def get_user_candidate_data(user_id: int) -> Optional[Dict[str, Any]]:
    with get_session() as session:
        resume = session.query(UserResume).filter(
            UserResume.user_id == user_id,
            UserResume.is_active == True
        ).first()
        if not resume:
            resume = session.query(UserResume).filter(
                UserResume.user_id == user_id
            ).order_by(UserResume.uploaded_at.desc()).first()
        if not resume or not resume.semantic_text:
            return None

        skills = _safe_json_list(resume.skills)
        profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()

        preferred, excluded, preferred_locs = [], [], []
        remote_only, threshold, chat_id, enabled = False, 0.6, None, False

        if profile:
            preferred = _safe_json_list(profile.preferred_keywords)
            excluded = _safe_json_list(profile.excluded_keywords)
            preferred_locs = _safe_json_list(profile.preferred_locations)
            remote_only = bool(profile.remote_only)
            threshold = float(profile.notification_threshold or 0.6)
            chat_id = profile.telegram_chat_id
            enabled = bool(profile.telegram_enabled)

        combined = list(set(skills + preferred))

        return {
            "user_id": user_id,
            "resume_id": resume.id,
            "semantic_text": resume.semantic_text,
            "skills": skills,
            "combined_skills": combined,
            "preferred_keywords": preferred,
            "excluded_keywords": excluded,
            "preferred_locations": preferred_locs,
            "remote_only": remote_only,
            "notification_threshold": float(threshold),
            "telegram_chat_id": chat_id,
            "telegram_enabled": enabled,
            "experience_level": resume.experience_level or "unknown",
        }

def _score_job_against_candidate(db_job: Dict, semantic_text: str, candidate: Dict, candidate_embedding) -> Dict:
    title_l = db_job.get("title","").lower()
    loc_l = db_job.get("location","").lower()
    searchable = f"{db_job.get('title','')} {db_job.get('company','')} {db_job.get('location','')} {semantic_text}"

    kw_score = float(_keyword_overlap(searchable, candidate["combined_skills"]))

    try:
        from app.services.similarity_service import cosine_similarity
        job_emb = generate_embedding(semantic_text)
        sem_score = float(cosine_similarity(candidate_embedding, job_emb))
    except Exception:
        sem_score = 0.0

    hybrid = float((0.6 * sem_score) + (0.4 * kw_score))

    if candidate["preferred_locations"]:
        if any(pl in loc_l for pl in candidate["preferred_locations"]):
            hybrid += 0.05
    if any(kw in title_l for kw in ENTRY_KEYWORDS):
        hybrid += 0.20
    elif any(kw in title_l for kw in SENIOR_KEYWORDS):
        hybrid -= 0.10
    if candidate["excluded_keywords"]:
        if any(ex in title_l for ex in candidate["excluded_keywords"]):
            hybrid -= 0.30

    db_job["similarity"] = round(float(sem_score), 4)
    db_job["keyword_overlap"] = round(float(kw_score), 4)
    db_job["hybrid_score"] = round(float(hybrid), 4)
    return db_job

def get_personalized_jobs(user_id: int, top_k: int = 20, semantic_weight: float = 0.6) -> List[Dict]:
    candidate = get_user_candidate_data(user_id)
    if not candidate:
        return []

    try:
        cand_emb = generate_embedding(candidate["semantic_text"])
    except Exception:
        return []

    try:
        semantic_results = search_similar_jobs(query_embedding=cand_emb, top_k=min(top_k*5, 200))
    except Exception:
        return []

    if not semantic_results:
        return []

    job_ids = [r.get("job_id") for r in semantic_results if r.get("job_id")]
    jobs_data = {}
    with get_session() as session:
        db_jobs = session.query(Job).filter(Job.id.in_(job_ids)).all()
        for j in db_jobs:
            jobs_data[j.id] = {"dict": _job_to_dict(j), "semantic_text": j.semantic_text or ""}

    personalized = []
    for res in semantic_results:
        jid = res.get("job_id")
        data = jobs_data.get(jid)
        if not data:
            continue
        scored = _score_job_against_candidate(data["dict"], data["semantic_text"], candidate, cand_emb)
        # Use Chroma similarity for accuracy
        chroma_sim = float(res.get("similarity", 0))
        scored["similarity"] = round(chroma_sim, 4)
        base_hybrid = float(semantic_weight * chroma_sim + (1-semantic_weight) * float(scored["keyword_overlap"]))
        if any(k in scored["title"].lower() for k in ENTRY_KEYWORDS):
            base_hybrid += 0.20
        scored["hybrid_score"] = round(float(base_hybrid), 4)
        personalized.append(scored)

    personalized.sort(key=lambda x: float(x["hybrid_score"]), reverse=True)
    return personalized[:top_k]

def get_broad_engineering_feed(user_id: int, page: int = 1, page_size: int = 20) -> List[Dict]:
    candidate = get_user_candidate_data(user_id)
    if not candidate:
        from app.services.database import fetch_all_jobs_from_db
        return fetch_all_jobs_from_db(page=page, page_size=page_size, sort_by="score", sort_order="DESC")

    personalized = get_personalized_jobs(user_id, top_k=200)
    personalized_ids = set(j["id"] for j in personalized)

    from app.services.database import fetch_all_jobs_from_db
    global_needed = page * page_size + 200
    global_jobs = fetch_all_jobs_from_db(page=1, page_size=global_needed, sort_by="score", sort_order="DESC")

    broad = personalized.copy()
    for gj in global_jobs:
        if gj["id"] not in personalized_ids:
            gj["hybrid_score"] = float(gj.get("score",0) / 100.0)
            gj["similarity"] = 0.0
            gj["keyword_overlap"] = 0.0
            broad.append(gj)

    broad.sort(key=lambda x: (float(x.get("hybrid_score",0)), float(x.get("score",0))), reverse=True)
    offset = (page-1)*page_size
    return broad[offset: offset+page_size]

def get_all_new_jobs_scored(user_id: int, new_job_ids: List[int]) -> List[Dict]:
    candidate = get_user_candidate_data(user_id)
    if not candidate or not new_job_ids:
        return []

    try:
        cand_emb = generate_embedding(candidate["semantic_text"])
    except Exception:
        return []

    jobs_data = {}
    with get_session() as session:
        jobs = session.query(Job).filter(Job.id.in_(new_job_ids)).all()
        for j in jobs:
            jobs_data[j.id] = {"dict": _job_to_dict(j), "semantic_text": j.semantic_text or "", "title": j.title, "location": j.location or ""}

    results = []
    for jid in new_job_ids:
        data = jobs_data.get(jid)
        if not data:
            continue
        scored = _score_job_against_candidate(data["dict"], data["semantic_text"], candidate, cand_emb)
        results.append(scored)

    results.sort(key=lambda x: float(x["hybrid_score"]), reverse=True)
    return results

def get_personalized_new_jobs(user_id: int, new_job_ids: List[int], threshold: Optional[float] = None) -> List[Dict]:
    all_scored = get_all_new_jobs_scored(user_id, new_job_ids)
    if threshold is None:
        candidate = get_user_candidate_data(user_id)
        threshold = float(candidate.get("notification_threshold", 0.6)) if candidate else 0.6
    else:
        threshold = float(threshold)
    return [j for j in all_scored if float(j["hybrid_score"]) >= threshold]