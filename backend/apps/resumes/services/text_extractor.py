import os
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    return extract_pdf_text(file_path)


def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_resume_text(file_path: str) -> str:
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file type")
