# rag/retriever.py
import numpy as np
from rag.vector_store import VectorStore

class VectorRetriever:
    def __init__(self, embedding_dim, index_path=None):
        self.vector_store = VectorStore(dim=embedding_dim, index_path=index_path)

    def add_embeddings(self, embeddings, ids):
        """
        Add embeddings and their corresponding ids to the vector store.
        embeddings: list or np.ndarray of shape (n_samples, embedding_dim)
        ids: list of identifiers for each embedding
        """
        embeddings = np.array(embeddings).astype('float32')
        self.vector_store.add(embeddings, ids)

    def retrieve(self, query_embedding, top_k=5):
        """
        Retrieve top_k most similar vectors and their ids for the given query embedding.
        query_embedding: np.ndarray of shape (embedding_dim,)
        Returns list of tuples: (id, score)
        """
        query_embedding = np.array(query_embedding).astype('float32')
        results = self.vector_store.search(query_embedding, top_k)
        return results

    def save(self, path):
        """
        Save the vector store index and metadata to disk.
        """
        self.vector_store.save(path)

    def load(self, path):
        """
        Load the vector store index and metadata from disk.
        """
        self.vector_store.load(path)
