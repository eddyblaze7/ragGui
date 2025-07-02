# rag/vector_store.py
import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, dim, index_path=None):
        self.dim = dim
        self.index_path = index_path
        self.index = faiss.IndexFlatIP(dim)  # Inner product similarity (cosine if normalized)
        self.ids = []  # Keep track of document/chunk ids

        # Load index if exists
        if index_path and os.path.exists(index_path):
            self.load(index_path)

    def add(self, vectors, ids):
        """
        Add vectors and corresponding ids to the index.
        vectors: np.ndarray shape (n, dim)
        ids: list of ids (strings or ints)
        """
        # Normalize vectors for cosine similarity (optional, recommended)
        faiss.normalize_L2(vectors)
        
        self.index.add(vectors)
        self.ids.extend(ids)

    def search(self, query_vector, top_k=5):
        """
        Search top_k vectors closest to query_vector.
        query_vector: np.ndarray shape (dim,)
        Returns: list of (id, score)
        """
        faiss.normalize_L2(query_vector.reshape(1, -1))
        distances, indices = self.index.search(query_vector.reshape(1, -1), top_k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.ids[idx], dist))
        return results

    def save(self, path=None):
        path = path or self.index_path
        if not path:
            raise ValueError("No path specified to save the index.")
        faiss.write_index(self.index, path + ".index")
        with open(path + ".ids", "wb") as f:
            pickle.dump(self.ids, f)

    def load(self, path):
        self.index = faiss.read_index(path + ".index")
        with open(path + ".ids", "rb") as f:
            self.ids = pickle.load(f)
