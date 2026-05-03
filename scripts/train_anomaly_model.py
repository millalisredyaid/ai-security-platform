import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

from app.core.config import (
    FEATURE_ORDER,
    IFOREST_CONTAMINATION,
    IFOREST_RANDOM_STATE,
    MODEL_PATH,
)
from app.logic.normalization import normalize_features


def build_raw_sample(
    request_rate: float,
    error_rate: float,
    payload_size: float,
    response_time: float,
    path_depth: float,
) -> dict[str, float]:
    return {
        "request_rate": request_rate,
        "error_rate": error_rate,
        "payload_size": payload_size,
        "response_time": response_time,
        "path_depth": path_depth,
    }


def generate_training_data(n_samples: int = 1000) -> np.ndarray:
    """
    Generate synthetic raw feature samples and normalize them using
    the same normalization logic used in the application.
    """
    rng = np.random.default_rng(IFOREST_RANDOM_STATE)
    rows: list[list[float]] = []

    for _ in range(n_samples):
        raw_sample = build_raw_sample(
            request_rate=float(rng.normal(loc=20, scale=8)),
            error_rate=float(rng.uniform(0.0, 0.2)),
            payload_size=float(rng.normal(loc=1500, scale=700)),
            response_time=float(rng.uniform(50, 600)),
            path_depth=float(rng.integers(1, 5)),
        )
        rows.append(normalize_features(raw_sample))

    return np.array(rows, dtype=float)


def train() -> None:
    print("Generating synthetic training data...")
    x_train = generate_training_data()

    print("Training Isolation Forest model...")
    model = IsolationForest(
        contamination=IFOREST_CONTAMINATION,
        random_state=IFOREST_RANDOM_STATE,
    )
    model.fit(x_train)

    artifact = {
        "model": model,
        "feature_order": FEATURE_ORDER,
        "normalized": True,
        "model_name": "isolation_forest_v1",
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train()
