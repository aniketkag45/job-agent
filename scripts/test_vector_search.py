from app.services.embedding_service import generate_embedding
from app.services.vector_store import store_job_embedding, search_similar_jobs

jobs = [
    {
        "id": 1,
        "title": "Junior Python Backend Engineer",
        "text" : """
        python FastAPI APIs Postgresql
"""
    },
    {
        "id": 2,
        "title" : "Frontend React Developer",
        "text" : """
        React Typescript JavaScript HTML CSS Next.js UI
"""
    },
    {
        "id": 3,
        "title" : "machine learning engineer",
        "text" : """
        Pytorch LLM Deep Learning NLP AI 
"""
    },
    {
        "id": 4,
        "title" : "Senior Accountant",
        "text" : """
        Finance Tax Payroll Accounting
"""
    }
]

for job in jobs:
    embedding = generate_embedding(job["text"])
    store_job_embedding(job["id"], embedding, metadata={"title": job["title"]})

query = """
Backend API Developer
Python, FastAPI, Microservices"""

query_embedding = generate_embedding(query)
results = search_similar_jobs(query_embedding, top_k=3)
print("\nDSemantic Search Results:")
for metadata,distance in zip(results["metadatas"][0], results["distances"][0]):
    print(f"{metadata['title']} (distance: {distance:.4f})")