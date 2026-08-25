import re

SSRF_PATTERNS=[
    r"https?://localhost(?=[:/]|$)",
    r"https?://127\.0\.0\.1(?=[:/]|$)",
    r"https?://0\.0\.0\.1(?=[:/]|$)",
    r"https?://169\.254\.169\.254(?=[:/]|$)",
    r"file://",
    r"gopher://"
]


def detect_ssrf(data):
    for pattern in SSRF_PATTERNS:
        if re.search(pattern,data,re.I):
            return {
                "attack":"SSRF",
                "severity":"HIGH",
                "rule":pattern
            }
    return None
