from urllib.parse import unquote


MAX_DECODE_ROUNDS = 2


def decode_url_encoded(
    value: str,
    max_rounds: int = MAX_DECODE_ROUNDS,
) -> str:
    """
    Decode URL-encoded text with a small fixed number of rounds.

    This helps detect simple evasion attempts such as:
    - %2e%2e%2f
    - %41dmin
    """
    decoded_value = value

    for _ in range(max_rounds):
        next_value = unquote(decoded_value)

        if next_value == decoded_value:
            break

        decoded_value = next_value

    return decoded_value


def normalize_whitespace(value: str) -> str:
    """
    Collapse repeated whitespace into a single space.
    """
    return " ".join(value.split())


def preprocess_payload(value: str | None) -> str:
    """
    Normalize text before rule-based security detection.
    """
    if value is None:
        return ""

    decoded = decode_url_encoded(value)
    lowered = decoded.lower()

    return normalize_whitespace(lowered)
