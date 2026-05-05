import logging

from app.logic.preprocessing import preprocess_payload
from app.schemas.request import AnalyzeRequest

logger = logging.getLogger(__name__)

SUSPICIOUS_USER_AGENTS = {
    "sqlmap",
    "nikto",
    "curl",
    "python-requests",
    "masscan",
    "nmap",
}


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

    normalized_endpoint = preprocess_payload(request.endpoint)
    normalized_user_agent = preprocess_payload(request.user_agent)

    if raw_values["error_rate"] > 0.4:
        triggered_rules.append("high_error_rate_rule")
        penalty -= 0.05

    if raw_values["path_depth"] > 5:
        triggered_rules.append("deep_path_access_rule")
        penalty -= 0.05

    if "admin" in normalized_endpoint:
        triggered_rules.append("sensitive_endpoint_access")
        penalty -= 0.05

    if any(agent in normalized_user_agent for agent in SUSPICIOUS_USER_AGENTS):
        triggered_rules.append("suspicious_user_agent")
        penalty -= 0.03

    logger.info(
        "Rule evaluation completed: endpoint=%s rules=%s penalty=%.4f",
        request.endpoint,
        triggered_rules,
        penalty,
    )
    return triggered_rules, penalty
