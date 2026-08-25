import re

XSS_PATTERNS=[
    r"<script.*?>",
    r"javascript:",
    r"onerror\s*=",
    r"onload\s*="
]


def detect_xss(data):
    for p in XSS_PATTERNS:
        if re.search(p,data,re.I):
            return{
                "attack":"XSS",
                "severity":"MEDIUM",
                "rule":p
            }
    return None

