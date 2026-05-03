from app.core.config import FEATURE_ORDER, FEATURE_RANGES


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(value, upper))


def normalize_value(feature_name: str, raw_value: float) -> float:
    min_value, max_value = FEATURE_RANGES[feature_name]

    if max_value <= min_value:
        return 0.0

    scaled = (raw_value - min_value) / (max_value - min_value)
    return clamp(scaled)


def normalize_features(raw_values: dict[str, float]) -> list[float]:
    """
    Normalize raw feature values into a fixed-order vector.
    """
    return [
        normalize_value(name, float(raw_values.get(name, 0.0)))
        for name in FEATURE_ORDER
    ]
