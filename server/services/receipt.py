from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from server.models.receipt import Receipt
from server.services.ocr_extractor import extract_items_from_receipt_text
from server.services.receipt_validator import requires_human_verification
from server.utils.logger import get_logger

_logger = get_logger(__name__)


async def process_ocr(image_url: str, raw_ocr_text: str, db: AsyncSession) -> Receipt:
    """
    Orchestrate the full OCR pipeline for a receipt upload.
    Delegates to ocr_extractor and receipt_validator sub-modules to stay
    within the 150-line complexity limit.
    """
    if not image_url or not image_url.strip():
        raise ValueError("image_url must not be empty.")
    if not raw_ocr_text or not raw_ocr_text.strip():
        raise ValueError("raw_ocr_text must not be empty.")

    try:
        parsed_items, confidence = extract_items_from_receipt_text(raw_ocr_text)
        needs_review = requires_human_verification(confidence)

        receipt = Receipt(
            receipt_id=uuid4(),
            image_url=image_url.strip(),
            confidence_score=confidence,
            requires_human_verification=needs_review,
            parsed_items=[],
        )
        await _persist_receipt(receipt, db)

        _logger.info(
            "Receipt %s processed: confidence=%.2f requires_review=%s.",
            receipt.receipt_id,
            confidence,
            needs_review,
        )
        return receipt
    except Exception as exc:
        _logger.error("OCR processing failed for '%s': %s", image_url, exc)
        raise


async def _persist_receipt(receipt: Receipt, db: AsyncSession) -> None:
    """Store the processed receipt in the database."""
    _logger.debug("Persisting receipt %s.", receipt.receipt_id)
    # Placeholder — replace with: db.add(orm_obj); await db.commit()
