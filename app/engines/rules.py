import logging
from dataclasses import dataclass

from app.engines.rule_patterns import SECURITY_RULE_PATTERNS
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


@dataclass(frozen=True)
class RuleMatchInfo:
    """Detailed information about a matched security rule."""

    rule_id: str
    category: str
    field: str
    pattern: str
    matched_value: str


@dataclass(frozen=True)
class RuleEvaluationResult:
    """Result of deterministic rule-based evaluation."""

    triggered_rules: list[str]
    penalty: float
    rule_matches: list[RuleMatchInfo]


def detect_security_patterns(
    value: str,
    field: str,
) -> tuple[list[str], list[RuleMatchInfo]]:
    """
    Detect suspicious security patterns in a normalized value.

    Returns:
    - triggered rule labels
    - detailed rule match information for traceability
    """
    triggered_categories: set[str] = set()
    match_details: list[RuleMatchInfo] = []

    for rule in SECURITY_RULE_PATTERNS:
        match = rule.pattern.search(value)
        if not match:
            continue

        triggered_categories.add(rule.category)
        match_details.append(
            RuleMatchInfo(
                rule_id=rule.rule_id,
                category=rule.category,
                field=field,
                pattern=rule.pattern.pattern,
                matched_value=match.group(0),
            )
        )

    triggered_rules: list[str] = []

    if "sqli" in triggered_categories:
        triggered_rules.append("sqli_pattern_detected")

    if "directory_traversal" in triggered_categories:
        triggered_rules.append("directory_traversal_detected")

    return triggered_rules, match_details


def evaluate_rules(
    request: AnalyzeRequest,
    raw_values: dict[str, float],
) -> RuleEvaluationResult:
    """
    Evaluate deterministic rule-based signals using raw values.

    Returns:
    - triggered rule codes
    - additional penalty to combine with model score
    - detailed rule match information for traceability
    """
    triggered_rules: list[str] = []
    rule_matches: list[RuleMatchInfo] = []
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

    security_pattern_rules, security_match_details = detect_security_patterns(
        value=normalized_endpoint,
        field="endpoint",
    )

    triggered_rules.extend(security_pattern_rules)
    rule_matches.extend(security_match_details)

    if "sqli_pattern_detected" in security_pattern_rules:
        penalty -= 0.15

    if "directory_traversal_detected" in security_pattern_rules:
        penalty -= 0.12

    logger.info(
        "Rule evaluation completed: endpoint=%s rules=%s penalty=%.4f matches=%s",
        request.endpoint,
        triggered_rules,
        penalty,
        rule_matches,
    )

    return RuleEvaluationResult(
        triggered_rules=triggered_rules,
        penalty=penalty,
        rule_matches=rule_matches,
    )
