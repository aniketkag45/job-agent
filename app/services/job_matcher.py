# from app.services.embedding_service import generate_embedding
# from app.services.similarity_service import cosine_similarity

# def find_matching_jobs(candidate_embedding, jobs, top_k=5):
#     scored_jobs = []
#     for job in jobs:
#         semantic_text = job.get("semantic_text")
#         if not semantic_text:
#             continue
#         job_embedding = generate_embedding(semantic_text)
#         sim = cosine_similarity(candidate_embedding, job_embedding)
#         scored_jobs.append((job, sim))

#     # Sort jobs by similarity score in descending order
#     scored_jobs.sort(key=lambda x: x[1], reverse=True)
#     return scored_jobs[:top_k]

import logging
from typing import List, Dict, Any, Optional

from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_similar_jobs

logger = logging.getLogger(__name__)

SEMANTIC_WEIGHTS = 0.6
KEYWORD_WEIGHTS = 0.4

def calculate_keyword_overlap(
        job_text: str,
        candidate_skills: List[str],
) -> float:
    if not candidate_skills:
        return 0.0
    text_lower = job_text.lower()
    matches = 0
    for skill in candidate_skills:
        if skill.lower() in text_lower:
            matches += 1
    return matches / len(candidate_skills)

def match_jobs_to_candidate(candidate_embedding: List[float], candidate_skills: Optional[List[str]] = None, top_k: int = 10, semantic_weight: float = SEMANTIC_WEIGHTS) -> List[Dict[str, Any]]:
    if candidate_skills is None:
        candidate_skills = []
    semantic_results = search_similar_jobs(query_embedding=candidate_embedding, top_k=min(top_k * 5, 50))  # Get more results to re-rank with keywords
    if not semantic_results:
        logger.info("No semantic matches found, returning empty list.")
        return []
    keyword_weight = 1.0 - semantic_weight
    for result in semantic_results:
        job_text = result.get("searchable_text", "") or " ".join([
            result.get("title", ""),
            result.get("company", ""),
        ])
        keyword_score = calculate_keyword_overlap(job_text, candidate_skills)
        hybrid = (semantic_weight * result["similarity"]) + \
                 (keyword_weight * keyword_score)
        result["hybrid_score"] = round(hybrid, 4)
        result["keyword_overlap"] = round(keyword_score, 6)

    semantic_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
    return semantic_results[:top_k]

def semantic_search(query: str, top_k: int = 10, filter_source: Optional[str] = None) -> List[Dict[str, Any]]:
    if not query or not query.strip():
        return []
    query_embedding = generate_embedding(query.strip())
    results = search_similar_jobs(query_embedding=query_embedding, top_k=top_k, filter_source=filter_source)
    return results