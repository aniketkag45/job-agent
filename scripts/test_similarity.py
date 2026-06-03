from app.services.embedding_service import generate_embedding
from app.services.similarity_service import cosine_similarity

job_1 = """
Junior Python Backend Engineer
FastAPI Docker PostgreSQL APIs
"""
job_2 = """
Backend API Developer
Python, FastAPI, Microservices
"""

job_3 = """
Senior Accountant
Finance Tax Payroll
"""
embedding_1 = generate_embedding(job_1)
embedding_2 = generate_embedding(job_2)
embedding_3 = generate_embedding(job_3)

similarity_1_2 = cosine_similarity(embedding_1, embedding_2)
similarity_1_3 = cosine_similarity(embedding_1, embedding_3)
print(f"Backend <-> Backend:"
      f" {similarity_1_2:.4f}")
print(f"Backend <-> Accountant:"
      f" {similarity_1_3:.4f}")