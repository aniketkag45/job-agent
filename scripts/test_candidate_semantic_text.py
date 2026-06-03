from app.services.resume_parser import extract_resume_text
from app.services.candidate_profile_builder import build_candidate_profile
from app.services.candidate_semantic_representation import build_candidate_semantic_text

resume_text = extract_resume_text(r"C:\Users\DELL\OneDrive\Desktop\Aniket_Resume.pdf")
profile = build_candidate_profile(resume_text)
semantic_text = build_candidate_semantic_text(profile)

print("Candidate Semantic Text:")
print(semantic_text)