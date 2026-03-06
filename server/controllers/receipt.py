from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from server.services import receipt as receipt_service
from server.utils.logger import get_logger

_logger = get_logger(__name__)

_ALLOWED_IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


async def handle_upload(
    file: UploadFile,
    db: AsyncSession,
):
    """
    Accept a receipt image, run the OCR pipeline, and return the parsed
    Receipt object. Prompts human verification when confidence < 70%.
    """
    if not file or not file.filename:
        raise HTTPException(status_code=422, detail="A receipt image file is required.")
    if file.content_type not in _ALLOWED_IMAGE_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. "
                   f"Allowed: {_ALLOWED_IMAGE_CONTENT_TYPES}.",
        )

    try:
        image_url = file.filename
        raw_ocr_text = await _read_upload_content(file)
        receipt = await receipt_service.process_ocr(image_url, raw_ocr_text, db)
        return receipt
    except ValueError as exc:
        _logger.warning("Receipt upload validation error: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        _logger.error("Unexpected receipt upload error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


async def _read_upload_content(file: UploadFile) -> str:
    """Read the uploaded file bytes and decode as UTF-8."""
    raw_bytes = await file.read()
    return raw_bytes.decode("utf-8", errors="replace")
