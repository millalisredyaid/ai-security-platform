import logging
from dataclasses import dataclass

from app.logic.normalization import normalize_features
from app.schemas.request import AnalyzeRequest, LogFeatures

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FeatureBundle:
    vector: list[float]
    raw_values: dict[str, float]
    sources: dict[str, str]


def extract_features(request: AnalyzeRequest) -> FeatureBundle:
    """
    Build a feature bundle containing:
    - normalized vector for ML inference
    - raw values for rule evaluation
    - source metadata for future server-side aggregation
    """
    feats = request.features or LogFeatures()
    path_depth = len([part for part in request.endpoint.split("/") if part])

    raw_values = {
        "request_rate": float(feats.request_rate_1m),
        "error_rate": float(feats.error_rate_1m),
        "payload_size": float(feats.payload_size_bytes),
        "response_time": float(feats.response_time_ms),
        "path_depth": float(path_depth),
    }

    sources = {
        "request_rate": "client",
        "error_rate": "client",
        "payload_size": "client",
        "response_time": "client",
        "path_depth": "server_derived",
    }

    vector = normalize_features(raw_values)

    logger.info(
        "Feature bundle created: endpoint=%s raw_values=%s sources=%s",
        request.endpoint,
        raw_values,
        sources,
    )

    return FeatureBundle(
        vector=vector,
        raw_values=raw_values,
        sources=sources,
    )
