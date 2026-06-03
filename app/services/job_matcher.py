from app.services.embedding_service import generate_embedding
from app.services.similarity_service import cosine_similarity

def find_matching_jobs(candidate_embedding, jobs, top_k=5):
    scored_jobs = []
    for job in jobs:
        semantic_text = job.get("semantic_text")
        if not semantic_text:
            continue
        job_embedding = generate_embedding(semantic_text)
        sim = cosine_similarity(candidate_embedding, job_embedding)
        scored_jobs.append((job, sim))

    # Sort jobs by similarity score in descending order
    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    return scored_jobs[:top_k]
