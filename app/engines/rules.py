import logging

from app.schemas.request import AnalyzeRequest

logger = logging.getLogger(__name__)


def evaluate_rules(
    request: AnalyzeRequest,
    raw_values: dict[str, float],
) -> tuple[list[str], float]:
    """
    Evaluate deterministic rule-based signals using raw values.

    Returns:
    - triggered rule codes
    - additional penalty to combine with model score
    """
    triggered_rules: list[str] = []
    penalty = 0.0

    if raw_values["error_rate"] > 0.4:
        triggered_rules.append("high_error_rate_rule")
        penalty -= 0.05

    if raw_values["path_depth"] > 5:
        triggered_rules.append("deep_path_access_rule")
        penalty -= 0.05

    if "admin" in request.endpoint.lower():
        triggered_rules.append("sensitive_endpoint_access")
        penalty -= 0.05

    logger.info(
        "Rule evaluation completed: endpoint=%s rules=%s penalty=%.4f",
        request.endpoint,
        triggered_rules,
        penalty,
    )
    return triggered_rules, penalty
