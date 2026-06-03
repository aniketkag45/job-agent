import numpy as np

def cosine_similarity(embedding_1,embedding_2):
    vector_1 = np.array(embedding_1)
    vector_2 = np.array(embedding_2)
    similarity = np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
    return similarity