# app_model.py
import os
import logging
from rag.chunker import TextChunker
from rag.embedder import TextEmbedder
from rag.retriever import VectorRetriever
from rag.llm_runner import LLMRunner
from rag.querry_engine import QueryEngine

class AppModel:
    def __init__(self):
        self.document_paths = []
        self.chunker = TextChunker()
        self.embedder = TextEmbedder()
        self.retriever = VectorRetriever(embedding_dim=self.embedder.embedding_dim)
        self.llm = LLMRunner(model_path="models/llama-2-7b-chat.Q2_K.gguf")
        self.chunk_id_to_text = {}  # New: map chunk ID to text
        # self.query_engine = QueryEngine(
        #     embedder=self.embedder,
        #     vector_store=self.retriever,
        #     llm_runner=self.llm,
        #     chunk_id_to_text=self.chunk_id_to_text  # pass mapping
        # )
        self.query_engine = QueryEngine(
            embedder=self.embedder,
            vector_store=self.retriever,
            llm_runner=self.llm,
            chunk_id_to_text=self.chunk_id_to_text  # pass mapping
        )

    def load_and_index_documents(self, file_paths):
        logging.info("Loading and indexing documents...")
        all_chunks = []
        all_chunk_ids = []

        for doc_id, path in enumerate(file_paths):
            try:
                text = self._load_document(path)
                chunks = self.chunker.chunk(text)
                chunk_ids = [f"doc{doc_id}_chunk{i}" for i in range(len(chunks))]
                embeddings = self.embedder.embed_documents(chunks)
                self.retriever.add_embeddings(embeddings, chunk_ids)
                
                all_chunks.extend(chunks)
                all_chunk_ids.extend(chunk_ids)
            except Exception as e:
                logging.error(f"Failed to load file {path}: {e}")
        
        # Save mapping of ID -> chunk text
        self.chunk_id_to_text.update(dict(zip(all_chunk_ids, all_chunks)))

        self.document_paths = file_paths
        self.retriever.save("db/vector_store")
        logging.info("Indexing complete.")

    def answer_query(self, query_text):
        try:
            return self.query_engine.query(query_text)
        except Exception as e:
            logging.error(f"Query failed: {e}")
            return "An error occurred while processing the query."

    def _load_document(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        elif ext == ".docx":
            import docx
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
