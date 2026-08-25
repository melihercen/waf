import re


COMMAND_PATTERNS = [
    r";\s*(ls|cat|whoami|id|pwd|uname)",
    r"&&\s*(ls|cat|whoami|id|pwd|uname)",
    r"\|\s*(ls|cat|whoami|id|pwd|uname)",
    r"`[^`]+`",
    r"\$\([^)]+\)"
]


def detect_command(data):
    for p in COMMAND_PATTERNS:
        if re.search(p, data, re.I):
            return {
                "attack": "COMMAND INJECTION",
                "severity": "HIGH",
                "rule": p
            }

    return None