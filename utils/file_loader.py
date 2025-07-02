import os
from .pdf_loader import load_pdf
from .docx_loader import load_docx
from .text_loader import load_txt

def load_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
    else:
        print(f"[WARN] Unsupported file type: {ext}")
        return ""
