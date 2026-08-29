from uuid import RFC_4122, UUID

from fastapi.testclient import TestClient

from app.api.endpoints import analyze as analyze_endpoint
from app.main import app
from app.middleware.request_id import REQUEST_ID_HEADER


def assert_uuid_v4(value: str) -> None:
    parsed_value = UUID(value)

    assert parsed_value.version == 4
    assert parsed_value.variant == RFC_4122
    assert str(parsed_value) == value


def test_valid_request_id_is_reused():
    request_id = "trace:abc_123-xyz.456"

    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == request_id


def test_missing_request_id_is_replaced_with_uuid_v4():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert_uuid_v4(response.headers[REQUEST_ID_HEADER])


def test_request_id_with_whitespace_is_replaced_with_uuid_v4():
    request_id = "invalid request-id"

    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] != request_id
    assert_uuid_v4(response.headers[REQUEST_ID_HEADER])


def test_129_character_request_id_is_replaced_with_uuid_v4():
    request_id = "a" * 129

    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] != request_id
    assert_uuid_v4(response.headers[REQUEST_ID_HEADER])


def test_128_character_request_id_is_reused():
    request_id = "a" + ":" * 127

    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == request_id


def test_disallowed_request_id_character_is_replaced_with_uuid_v4():
    request_id = "invalid/request-id"

    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] != request_id
    assert_uuid_v4(response.headers[REQUEST_ID_HEADER])


def test_request_id_starting_with_colon_is_replaced_with_uuid_v4():
    request_id = ":request-id"

    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] != request_id
    assert_uuid_v4(response.headers[REQUEST_ID_HEADER])


def test_404_response_includes_request_id():
    request_id = "request-id-for-404"

    with TestClient(app) as client:
        response = client.get(
            "/route-that-does-not-exist",
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 404
    assert response.headers[REQUEST_ID_HEADER] == request_id


def test_422_response_includes_request_id():
    request_id = "request-id-for-422"

    with TestClient(app) as client:
        response = client.post(
            "/analyze",
            json={},
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 422
    assert response.headers[REQUEST_ID_HEADER] == request_id


def test_analyze_propagates_request_id_to_security_decision_log(monkeypatch):
    request_id = "analyze-request:123"
    analyze_messages = []
    decision_logs = []

    def capture_info(message, *args):
        analyze_messages.append(message % args)

    monkeypatch.setattr(analyze_endpoint.logger, "info", capture_info)
    monkeypatch.setattr(
        analyze_endpoint,
        "emit_security_decision_log",
        decision_logs.append,
    )

    with TestClient(app) as client:
        response = client.post(
            "/analyze",
            json={
                "client_ip": "192.0.2.1",
                "endpoint": "/api/v1/login",
                "method": "POST",
            },
            headers={REQUEST_ID_HEADER: request_id},
        )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == request_id
    assert "request_id" not in response.json()
    assert len(decision_logs) == 1
    assert decision_logs[0]["request_id"] == request_id
    assert any(
        message.startswith("Analyze request received:")
        and f"request_id={request_id}" in message
        for message in analyze_messages
    )
