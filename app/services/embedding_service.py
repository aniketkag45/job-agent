# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('all-MiniLM-L6-v2')

# def generate_embedding(text):
#     embedding = model.encode(text)
#     return embedding.tolist()

import logging
from typing import List

logger = logging.getLogger(__name__)
_model = None

def get_model():
    global _model
    if _model is None:
        try:
            logger.info("Loading embedding model 'all-MiniLM-L6-v2'...")
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise
    logger.info("Embedding model loaded successfully.")
    return _model

def generate_embedding(text: str) -> List[float]:
    if not text or not text.strip():
        raise ValueError("Cannot generate embedding for empty text.")
    model = get_model()
    embedding = model.encode(text)
    return embedding.tolist()

def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []
    valid_texts = []
    valid_indices = []
    for i, text in enumerate(texts):
        if text and text.strip():
            valid_texts.append(text)
            valid_indices.append(i)
    
    if not valid_texts:
        return [[0.0] * 384 for _ in texts]  # Return zero embeddings for all if no valid texts
    model = get_model()
    embeddings = model.encode(valid_texts)
    result = [[0.0] * 384 for _ in texts]  # Initialize with zero embeddings
    for idx, embedding in zip(valid_indices, embeddings):
        result[idx] = embedding.tolist()
    return result

def get_embedding_dimension() -> int:
    return 384

def get_model_name() -> str:
    return 'all-MiniLM-L6-v2'