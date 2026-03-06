from server.utils.logger import get_logger

_logger = get_logger(__name__)

HUMAN_VERIFICATION_THRESHOLD = 0.70


def requires_human_verification(confidence_score: float) -> bool:
    """
    Determine if a scanned receipt requires manual human review.
    Per requirements: confidence < 70% triggers a verification prompt.
    """
    if not isinstance(confidence_score, float):
        raise TypeError(
            f"confidence_score must be a float, received {type(confidence_score).__name__}."
        )
    if not (0.0 <= confidence_score <= 1.0):
        raise ValueError(
            f"confidence_score must be between 0.0 and 1.0, received {confidence_score}."
        )

    needs_review = confidence_score < HUMAN_VERIFICATION_THRESHOLD
    _logger.debug(
        "Confidence=%.2f → requires_human_verification=%s.",
        confidence_score,
        needs_review,
    )
    return needs_review
