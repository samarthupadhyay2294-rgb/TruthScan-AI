import re
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import AppException


def validate_email_format(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True


def validate_upload_file(file: UploadFile) -> None:
    if not file.filename:
        raise AppException("Filename is required")

    extension = Path(file.filename).suffix.lower()
    if extension not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        raise AppException(
            f"Unsupported file type. Allowed: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}"
        )
