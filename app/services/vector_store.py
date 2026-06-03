import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="jobs")

def store_job_embedding(job_id, embedding, metadata):
    collection.add(
        ids = [str(job_id)],
        embeddings = [embedding],
        metadatas = [metadata]
    )

def search_similar_jobs(query_embedding, top_k = 5):
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = top_k
    )
    return results
