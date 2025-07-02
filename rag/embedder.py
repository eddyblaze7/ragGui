# rag/embedder.py

from InstructorEmbedding import INSTRUCTOR
from typing import List
import numpy as np



class TextEmbedder:
    def __init__(self, model_name="hkunlp/instructor-base"):
        self.model = INSTRUCTOR(model_name)

        # Dummy call to determine embedding dimension
        test_input = [["Represent the document for retrieval", "test document"]]
        embedding = self.model.encode(test_input, convert_to_numpy=True)
        self.embedding_dim = embedding.shape[1]  # Store embedding dimension

    def embed_documents(self, texts):
        try:
            inputs = [["Represent the document for retrieval", text] for text in texts]
            embeddings = self.model.encode(inputs, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            raise RuntimeError(f"Failed to embed documents: {e}")

    def embed_query(self, query):
        try:
            inputs = [["Represent the query for retrieval", query]]
            embedding = self.model.encode(inputs, convert_to_numpy=True)
            return embedding
        except Exception as e:
            raise RuntimeError(f"Failed to embed query: {e}")
