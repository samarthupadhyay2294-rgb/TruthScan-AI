import io
from pathlib import Path
from typing import Optional

from docx import Document
from fastapi import UploadFile
from pypdf import PdfReader

from app.core.config import settings
from app.core.exceptions import AppException
from app.utils.validators import validate_upload_file


async def extract_text_from_upload(file: UploadFile) -> str:
    validate_upload_file(file)

    content = await file.read()
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise AppException(
            f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB} MB"
        )

    extension = Path(file.filename or "").suffix.lower()

    if extension == ".txt":
        return _extract_from_txt(content)
    if extension == ".pdf":
        return _extract_from_pdf(content)
    if extension == ".docx":
        return _extract_from_docx(content)

    raise AppException(f"Unsupported file type: {extension}")


def _extract_from_txt(content: bytes) -> str:
    for encoding in ("utf-8", "latin-1", "cp1252"):
        try:
            text = content.decode(encoding).strip()
            if text:
                return text
        except UnicodeDecodeError:
            continue
    raise AppException("Unable to decode text file")


def _extract_from_pdf(content: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages).strip()
        if not text:
            raise AppException("No text could be extracted from PDF")
        return text
    except AppException:
        raise
    except Exception as exc:
        raise AppException(f"Failed to parse PDF: {exc}") from exc


def _extract_from_docx(content: bytes) -> str:
    try:
        document = Document(io.BytesIO(content))
        paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        text = "\n".join(paragraphs).strip()
        if not text:
            raise AppException("No text could be extracted from DOCX")
        return text
    except AppException:
        raise
    except Exception as exc:
        raise AppException(f"Failed to parse DOCX: {exc}") from exc


def save_upload_file(content: bytes, filename: str, upload_dir: Optional[str] = None) -> str:
    directory = Path(upload_dir or settings.UPLOAD_DIR)
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / filename
    destination.write_bytes(content)
    return str(destination)
