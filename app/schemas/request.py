from datetime import datetime, timezone
from ipaddress import ip_address
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.config import FEATURE_RANGES


RequestRate = Annotated[
    float,
    Field(
        ge=FEATURE_RANGES["request_rate"][0],
        le=FEATURE_RANGES["request_rate"][1],
        description="Number of requests observed within one minute.",
        examples=[12.0],
    ),
]

ErrorRate = Annotated[
    float,
    Field(
        ge=FEATURE_RANGES["error_rate"][0],
        le=FEATURE_RANGES["error_rate"][1],
        description="Error rate within the 0.0 to 1.0 range.",
        examples=[0.05],
    ),
]

PayloadSize = Annotated[
    float,
    Field(
        ge=FEATURE_RANGES["payload_size"][0],
        le=FEATURE_RANGES["payload_size"][1],
        description="Payload size in bytes.",
        examples=[1024.0],
    ),
]

ResponseTime = Annotated[
    float,
    Field(
        ge=FEATURE_RANGES["response_time"][0],
        le=FEATURE_RANGES["response_time"][1],
        description="Response time in milliseconds.",
        examples=[150.0],
    ),
]

PathDepth = Annotated[
    float,
    Field(
        ge=FEATURE_RANGES["path_depth"][0],
        le=FEATURE_RANGES["path_depth"][1],
        description=(
            "Client-provided path depth hint. "
            "The server derives the effective path depth from endpoint."
        ),
        examples=[3.0],
    ),
]


class LogFeatures(BaseModel):
    """Optional numeric features used by the analysis pipeline."""

    model_config = ConfigDict(extra="forbid")

    request_rate_1m: RequestRate = 0.0
    error_rate_1m: ErrorRate = 0.0
    payload_size_bytes: PayloadSize = 0.0
    response_time_ms: ResponseTime = 0.0
    path_depth: PathDepth = 0.0


class AnalyzeRequest(BaseModel):
    """
    Input payload for the analysis API.

    `features` is optional on purpose:
    - for now, it can be used for internal testing and prototyping
    - later, the server can derive features inside
      services/feature_engineering.py
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "client_ip": "192.168.1.1",
                "endpoint": "/api/v1/login",
                "method": "POST",
                "status_code": 401,
                "user_agent": "Mozilla/5.0",
                "features": {
                    "request_rate_1m": 12.0,
                    "error_rate_1m": 0.05,
                    "payload_size_bytes": 1024.0,
                    "response_time_ms": 150.0,
                    "path_depth": 3.0,
                },
            }
        },
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    client_ip: str = Field(
        ...,
        min_length=3,
        max_length=45,
        description="Client IPv4 or IPv6 address.",
        examples=["192.168.1.1"],
    )
    endpoint: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Requested endpoint path.",
        examples=["/api/v1/login"],
    )
    method: str = Field(
        default="POST",
        description="HTTP method.",
        examples=["POST"],
    )
    status_code: int | None = Field(
        default=None,
        ge=100,
        le=599,
        description="HTTP response status code.",
        examples=[401],
    )
    user_agent: str | None = Field(
        default=None,
        max_length=512,
        description="Client user agent string.",
        examples=["Mozilla/5.0"],
    )
    features: LogFeatures | None = None

    @field_validator("timestamp")
    @classmethod
    def ensure_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    @field_validator("client_ip")
    @classmethod
    def validate_client_ip(cls, value: str) -> str:
        ip_address(value)
        return value

    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, value: str) -> str:
        if not value.startswith("/"):
            raise ValueError("endpoint must start with '/'")
        return value

    @field_validator("method", mode="before")
    @classmethod
    def normalize_and_validate_method(cls, value: str) -> str:
        method = str(value).upper()

        allowed_methods = {
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "HEAD",
            "OPTIONS",
        }

        if method not in allowed_methods:
            allowed = ", ".join(sorted(allowed_methods))
            raise ValueError(
                f"method must be one of: {allowed}"
            )

        return method

    @property
    def path(self) -> str:
        return self.endpoint
