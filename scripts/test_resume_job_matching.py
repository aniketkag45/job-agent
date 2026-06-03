from app.services.resume_parser import extract_resume_text
from app.services.candidate_profile_builder import build_candidate_profile
from app.services.candidate_semantic_representation import build_candidate_semantic_text
from app.services.embedding_service import generate_embedding
from app.services.job_matcher import find_matching_jobs
from app.services.database import fetch_all_jobs_from_db

resume_text = extract_resume_text(r"C:\Users\DELL\OneDrive\Desktop\Aniket_Resume.pdf")
profile = build_candidate_profile(resume_text)
candidate_text = build_candidate_semantic_text(profile)
candidate_embedding = generate_embedding(candidate_text)

jobs = fetch_all_jobs_from_db(page = 1, page_size = 10)  # Fetch first 10 jobs for testing
matching_jobs = find_matching_jobs(candidate_embedding, jobs, top_k=5)
print("Top Matching Jobs:")
for job in matching_jobs:
    print(
        f"{job['title']}"
        f"{job['company']}"
        f"{job['similarity_score']:.4f}"
    )