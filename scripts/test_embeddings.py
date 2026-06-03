from app.services.embedding_service import generate_embedding

text = """
Junior Python Backend Engineer
Tech Stack: Python, Django, REST APIs, PostgreSQL
"""
embedding = generate_embedding(text)
print(f"Embedding dimension: {len(embedding)}")
print(embedding[:10])  # Print the first 10 values of the embedding vector