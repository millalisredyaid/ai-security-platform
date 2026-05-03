import logging

import joblib
import numpy as np

from app.core.config import (
    FEATURE_ORDER,
    MODEL_PATH,
    MODEL_REASON_THRESHOLDS,
)

logger = logging.getLogger(__name__)

try:
    if MODEL_PATH.exists():
        artifact = joblib.load(MODEL_PATH)
        model = artifact["model"]

        artifact_feature_order = artifact.get("feature_order")
        artifact_normalized = artifact.get("normalized")

        if artifact_feature_order != FEATURE_ORDER:
            raise ValueError(
                "Model feature order mismatch: "
                f"expected={FEATURE_ORDER}, got={artifact_feature_order}"
            )

        if artifact_normalized is not True:
            raise ValueError(
                "Model normalization metadata mismatch: "
                f"expected=True, got={artifact_normalized}"
            )

        logger.info(
            "Successfully loaded Isolation Forest model from %s",
            MODEL_PATH,
        )
    else:
        artifact = None
        model = None
        logger.warning(
            "Model file not found. Inference will use fallback logic."
        )
except Exception as exc:
    logger.error("Failed to load model: %s", exc)
    artifact = None
    model = None


def get_anomaly_score(vector: list[float]) -> tuple[float, list[str]]:
    """
    Run inference on a normalized feature vector and return:
    - anomaly score
    - structured model reason codes
    """
    model_reasons: list[str] = []

    if model is None:
        return -0.10, ["model_not_loaded"]

    input_data = np.array(vector, dtype=float).reshape(1, -1)
    raw_score = float(model.decision_function(input_data)[0])

    if vector[0] > MODEL_REASON_THRESHOLDS["request_rate"]:
        model_reasons.append("high_request_rate")

    if vector[1] > MODEL_REASON_THRESHOLDS["error_rate"]:
        model_reasons.append("high_error_rate")

    if vector[2] > MODEL_REASON_THRESHOLDS["payload_size"]:
        model_reasons.append("large_payload_size")

    if vector[3] > MODEL_REASON_THRESHOLDS["response_time"]:
        model_reasons.append("slow_response_time")

    if vector[4] > MODEL_REASON_THRESHOLDS["path_depth"]:
        model_reasons.append("deep_path_access")

    if raw_score < -0.15:
        model_reasons.append("statistical_outlier")

    logger.info(
        "Inference completed: score=%.4f reasons=%s",
        raw_score,
        model_reasons,
    )
    return raw_score, model_reasons
