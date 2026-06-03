from app.services.resume_parser import extract_resume_text
from app.services.candidate_profile_builder import build_candidate_profile
from app.services.candidate_semantic_representation import build_candidate_semantic_text
from app.services.embedding_service import generate_embedding

resume_text = extract_resume_text(r"C:\Users\DELL\OneDrive\Desktop\Aniket_Resume.pdf")
profile = build_candidate_profile(resume_text)
semantic_text = build_candidate_semantic_text(profile)
embedding = generate_embedding(semantic_text)
print(f"Embedding dimension: {len(embedding)}")
print(embedding[:10])  # Print the first 10 values of the embedding vector