import logging

from fastapi import APIRouter, BackgroundTasks, Request
from starlette.concurrency import run_in_threadpool

from app.engines.rules import evaluate_rules
from app.logic.scoring import combine_scores
from app.logic.thresholding import evaluate_thresholds
from app.schemas.request import AnalyzeRequest
from app.schemas.response import (AnalyzeResponse, RecommendedAction,
                                  SeverityLevel)
from app.services.feature_engineering import extract_features
from app.services.inference import get_anomaly_score
from app.tasks.security_events import emit_security_decision_log

logger = logging.getLogger(__name__)

router = APIRouter()

ACTION_POLICY = {
    SeverityLevel.critical: RecommendedAction.block,
    SeverityLevel.high: RecommendedAction.alert,
    SeverityLevel.medium: RecommendedAction.alert,
    SeverityLevel.low: RecommendedAction.allow,
}


def build_human_readable_details(
    endpoint: str,
    severity: SeverityLevel,
    model_reasons: list[str],
    has_rule_hits: bool,
) -> str:
    """
    Build a human-readable explanation from structured model reasons
    without exposing internal rule codes directly.
    """
    reason_labels = {
        "high_request_rate": "a spike in request volume",
        "high_error_rate": "an elevated error rate",
        "large_payload_size": "an unusually large payload size",
        "slow_response_time": "slow response time",
        "deep_path_access": "unusually deep path access",
        "statistical_outlier": "a statistically unusual access pattern",
        "model_not_loaded": (
            "a fallback scoring path due to missing model artifact"
        ),
    }

    readable_reasons = [
        reason_labels.get(reason, reason.replace("_", " "))
        for reason in model_reasons
    ]

    if readable_reasons and has_rule_hits:
        return (
            f"Analysis completed for endpoint={endpoint}. "
            f"Severity was assessed as {severity.value}. "
            f"Model signals indicate {', '.join(readable_reasons)}. "
            f"Additional rule-based signals were also detected."
        )

    if readable_reasons:
        return (
            f"Analysis completed for endpoint={endpoint}. "
            f"Severity was assessed as {severity.value}. "
            f"Model signals indicate {', '.join(readable_reasons)}."
        )

    if has_rule_hits:
        return (
            f"Analysis completed for endpoint={endpoint}. "
            f"Severity was assessed as {severity.value}. "
            f"Additional rule-based signals were detected."
        )

    return (
        f"Analysis completed for endpoint={endpoint}. "
        f"Severity was assessed as {severity.value}."
    )


@router.post("", response_model=AnalyzeResponse)
async def analyze_log(
    request: Request,
    payload: AnalyzeRequest,
    background_tasks: BackgroundTasks,
):
    request_id = request.state.request_id

    logger.info(
        "Analyze request received: request_id=%s client_ip=%s endpoint=%s",
        request_id,
        payload.client_ip,
        payload.endpoint,
    )

    bundle = await run_in_threadpool(extract_features, payload)
    model_score, model_reasons = await run_in_threadpool(
        get_anomaly_score,
        bundle.vector,
    )
    rule_result = evaluate_rules(payload, bundle.raw_values)

    triggered_rules = rule_result.triggered_rules
    rule_penalty = rule_result.penalty

    final_score = combine_scores(model_score, rule_penalty)
    decision = evaluate_thresholds(final_score)

    recommended_action = ACTION_POLICY.get(
        decision.severity,
        RecommendedAction.allow,
    )

    details = build_human_readable_details(
        endpoint=payload.endpoint,
        severity=decision.severity,
        model_reasons=model_reasons,
        has_rule_hits=bool(triggered_rules),
    )

    security_decision_log = {
        "event": "security_decision",
        "request_id": request_id,
        "endpoint": payload.endpoint,
        "client_ip": payload.client_ip,
        "severity": decision.severity.value,
        "action": recommended_action.value,
        "is_anomaly": decision.is_anomaly,
        "model_score": model_score,
        "rule_penalty": rule_penalty,
        "final_score": final_score,
        "threshold": decision.threshold,
        "model_reasons": model_reasons,
        "triggered_rules": triggered_rules,
        "feature_sources": bundle.sources,
        "raw_values": bundle.raw_values,
        "normalized_vector": bundle.vector,
    }

    background_tasks.add_task(
        emit_security_decision_log,
        security_decision_log,
    )

    return AnalyzeResponse(
        is_anomaly=decision.is_anomaly,
        anomaly_score=final_score,
        threshold=decision.threshold,
        severity=decision.severity,
        action=recommended_action,
        triggered_rules=triggered_rules,
        received_path=payload.path,
        details=details,
    )
