import json
import logging

logger = logging.getLogger(__name__)


def emit_security_decision_log(payload: dict) -> None:
    """
    Emit a structured security decision log payload.
    """
    logger.info(
        "Security decision: %s",
        json.dumps(payload, ensure_ascii=False, sort_keys=True),
    )
