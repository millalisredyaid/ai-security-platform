from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern


@dataclass(frozen=True)
class RulePattern:
    """A regex-based security detection pattern."""

    rule_id: str
    category: str
    pattern: Pattern[str]


SQLI_PATTERNS: list[RulePattern] = [
    RulePattern(
        rule_id="sqli_union_select",
        category="sqli",
        pattern=re.compile(r"\bunion\s+(all\s+)?select\b", re.IGNORECASE),
    ),
    RulePattern(
        rule_id="sqli_boolean_or_true",
        category="sqli",
        pattern=re.compile(
            r"\bor\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?",
            re.IGNORECASE,
        ),
    ),
    RulePattern(
        rule_id="sqli_boolean_and_true",
        category="sqli",
        pattern=re.compile(
            r"\band\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?",
            re.IGNORECASE,
        ),
    ),
    RulePattern(
        rule_id="sqli_drop_table",
        category="sqli",
        pattern=re.compile(r"\bdrop\s+table\b", re.IGNORECASE),
    ),
    RulePattern(
        rule_id="sqli_information_schema",
        category="sqli",
        pattern=re.compile(r"\binformation_schema\b", re.IGNORECASE),
    ),
    RulePattern(
        rule_id="sqli_sleep_function",
        category="sqli",
        pattern=re.compile(r"\bsleep\s*\(", re.IGNORECASE),
    ),
    RulePattern(
        rule_id="sqli_benchmark_function",
        category="sqli",
        pattern=re.compile(r"\bbenchmark\s*\(", re.IGNORECASE),
    ),
]


DIRECTORY_TRAVERSAL_PATTERNS: list[RulePattern] = [
    RulePattern(
        rule_id="traversal_dotdot_slash",
        category="directory_traversal",
        pattern=re.compile(r"\.\./"),
    ),
    RulePattern(
        rule_id="traversal_dotdot_backslash",
        category="directory_traversal",
        pattern=re.compile(r"\.\.\\"),
    ),
    RulePattern(
        rule_id="traversal_etc_passwd",
        category="directory_traversal",
        pattern=re.compile(r"/etc/passwd", re.IGNORECASE),
    ),
    RulePattern(
        rule_id="traversal_windows_win_ini",
        category="directory_traversal",
        pattern=re.compile(r"windows/win\.ini", re.IGNORECASE),
    ),
]


SECURITY_RULE_PATTERNS: list[RulePattern] = [
    *SQLI_PATTERNS,
    *DIRECTORY_TRAVERSAL_PATTERNS,
]
