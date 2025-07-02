# rag/loader.py

import os
from typing import List
from dataclasses import dataclass

from pypdf import PdfReader
from docx import Document


@dataclass
class DocumentPage:
    content: str
    metadata: dict


class DocumentLoader:
    def load(self, file_path: str) -> List[DocumentPage]:
        ext = os.path.splitext(file_path)[-1].lower()

        if ext == ".pdf":
            return self._load_pdf(file_path)
        elif ext == ".docx":
            return self._load_docx(file_path)
        elif ext == ".txt":
            return self._load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _load_pdf(self, path: str) -> List[DocumentPage]:
        reader = PdfReader(path)
        return [DocumentPage(content=page.extract_text(), metadata={"source": path, "page": i})
                for i, page in enumerate(reader.pages)]

    def _load_docx(self, path: str) -> List[DocumentPage]:
        doc = Document(path)
        full_text = "\n".join(para.text for para in doc.paragraphs)
        return [DocumentPage(content=full_text, metadata={"source": path})]

    def _load_txt(self, path: str) -> List[DocumentPage]:
        with open(path, 'r', encoding='utf-8') as f:
            return [DocumentPage(content=f.read(), metadata={"source": path})]
