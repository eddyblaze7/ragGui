# rag/query_engine.py

from rag.loader import DocumentLoader
from rag.chunker import TextChunker
from rag.embedder import TextEmbedder
from rag.retriever import VectorRetriever
from rag.llm_runner import LLMRunner

from typing import List


class QueryEngine:
    def __init__(self, embedder, vector_store, llm_runner, chunk_id_to_text):
        # Core components
        
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm_runner= llm_runner
        self.chunk_id_to_text = chunk_id_to_text  # receive mapping 
        self.chunk_id_to_source = {}  # ✅ Add this line
        self.retriever = vector_store # optional alias
        

    def index_documents(self, file_paths: List[str]):
        """
        Load, chunk, embed, and index documents for retrieval.
        """
        all_chunks = []

        for path in file_paths:
            docs = self.loader.load(path)
            for doc in docs:
                chunks = self.chunker.chunk_text(doc.page_content)
                all_chunks.extend(chunks)

        # Store embeddings in retriever memory/index
        self.retriever.index_chunks(all_chunks, self.embedder)


    def query(self, user_query: str, top_k: int = 3) -> str:
        # Pass string directly, not a list
        query_embedding = self.embedder.embed_query(user_query)[0]

        # Retrieve top_k similar chunks
        retrieved = self.retriever.retrieve(query_embedding, top_k=top_k)

        # Map chunk IDs to actual text
        retrieved_chunks = [
            self.chunk_id_to_text.get(chunk_id, "[Missing Text]")
            for chunk_id, _ in retrieved
        ]

        context = "\n".join(retrieved_chunks)
        prompt = (
            f"You are a helpful assistant. Use the following context to answer the question:\n\n"
            f"{context}\n\nQuestion: {user_query}\nAnswer:"
        )

        answer = self.llm_runner.generate_answer(prompt)
        return answer

