# import chromadb

# client = chromadb.Client()
# collection = client.get_or_create_collection(name="jobs")

# def store_job_embedding(job_id, embedding, metadata):
#     collection.add(
#         ids = [str(job_id)],
#         embeddings = [embedding],
#         metadatas = [metadata]
#     )

# def search_similar_jobs(query_embedding, top_k = 5):
#     results = collection.query(
#         query_embeddings = [query_embedding],
#         n_results = top_k
#     )
#     return results

import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

STORAGE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'storage',
    'chromadb'
)

COLLECTION_NAME = 'jobs_embeddings'
EMBEDDING_DIMENSION = 384

client = None
collection = None

def get_collection():
    global client,collection
    if collection is None:
        import chromadb
        os.makedirs(STORAGE_DIR, exist_ok=True)
        logger.info(f"Opening ChromaDB collection '{COLLECTION_NAME}' at '{STORAGE_DIR}'...")
        client = chromadb.PersistentClient(path=STORAGE_DIR)
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME, 
            metadata = {
           "description": "Collection for job embeddings",
           "dimension": str(EMBEDDING_DIMENSION),
          "model": "all-MiniLM-L6-v2"
            })
        logger.info(f"Collection '{COLLECTION_NAME}' is ready.")
    return collection

def sanitize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    safe = {}
    for key,value in metadata.items():
        if value is None:
            safe[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            safe[key] = value
        else:
            safe[key] = str(value)
    return safe
    
def store_job_embedding(job_id: int, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> bool:
    try:
        collection = get_collection()
        if metadata is None:
            metadata = {}
        collection.add(
            ids = [str(job_id)],
            embeddings = [embedding],
            metadatas = [sanitize_metadata(metadata)]
        )
        logger.info(f"Stored embedding for job_id {job_id} successfully.")
        return True
    except Exception as e:
        logger.error(f"Error storing embedding for job_id {job_id}: {e}")
        return False
    
def search_similar_jobs(query_embedding: List[float], top_k: int = 10, filter_source: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        collection = get_collection()
        where_filter = None
        if filter_source:
            where_filter = {"source": filter_source}
        results = collection.query(
            query_embeddings = [query_embedding],
            n_results = top_k,
            where = where_filter,
            include = ["metadatas","distances"]
        )
        ids =  results["ids"][0] if results["ids"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        distances = results["distances"][0] if results["distances"] else []

        matches = []
        for job_id, metadata, distance in zip(ids, metadatas, distances):
            similarity = 1.0 - (distance/2.0)
            matches.append({
                "job_id": int(job_id),
                "similarity": round(similarity, 4),
                "title": metadata.get("title", ""),
                "company": metadata.get("company", ""),
                "source": metadata.get("source", ""),
                "score": int(metadata.get("score", 0)),
                "location": metadata.get("location", ""),
                "apply_link": metadata.get("apply_link", ""),
                "searchable_text": metadata.get("searchable_text", "")
            })
        return matches
    except Exception as e:
        logger.error(f"Error searching similar jobs: {e}")
        return []
    
def delete_job_embedding(job_id: int) -> bool:
    try:
        collection = get_collection()
        collection.delete(ids=[str(job_id)])
        logger.info(f"Deleted embedding for job_id {job_id} successfully.")
        return True
    except Exception as e:
        logger.error(f"Error deleting embedding for job_id {job_id}: {e}")
        return False
    
def get_collection_stats() -> Dict[str,Any]:
    try:
        collection = get_collection()
        return {
            "collection_name": COLLECTION_NAME,
            "embedding_dimension": EMBEDDING_DIMENSION,
            "storage_path": STORAGE_DIR,
            "total_embeddings": collection.count()
        }
    except Exception as e:
        return{
            "total_embeddings": 0,
            "error": str(e),
            "collection_name": COLLECTION_NAME
        }
    
def clear_collection() -> bool:
    try:
        collection = get_collection()
        all_ids = collection.get()["ids"]
        if all_ids:
            collection.delete(ids=all_ids)
        logger.info(f"Cleared all embeddings from collection '{COLLECTION_NAME}'.")
        return True
    except Exception as e:
        logger.error(f"Error clearing collection '{COLLECTION_NAME}': {e}")
        return False
