from pathlib import Path

APP_TITLE = "AI Security Platform"
APP_DESCRIPTION = "Autonomous Security Agent API"
APP_VERSION = "0.1.0"

ANOMALY_THRESHOLD = -0.15
MEDIUM_THRESHOLD = -0.15
HIGH_THRESHOLD = -0.30

FEATURE_ORDER = [
    "request_rate",
    "error_rate",
    "payload_size",
    "response_time",
    "path_depth",
]

FEATURE_RANGES = {
    "request_rate": (0.0, 200.0),
    "error_rate": (0.0, 1.0),
    "payload_size": (0.0, 20000.0),
    "response_time": (0.0, 2000.0),
    "path_depth": (0.0, 10.0),
}

MODEL_REASON_THRESHOLDS = {
    "request_rate": 0.80,
    "error_rate": 0.80,
    "payload_size": 0.80,
    "response_time": 0.80,
    "path_depth": 0.80,
}

MODEL_DIR = Path("app/models")
MODEL_PATH = MODEL_DIR / "anomaly_model.joblib"

IFOREST_RANDOM_STATE = 42
IFOREST_CONTAMINATION = 0.05
