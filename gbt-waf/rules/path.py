import re


PATH_PATTERNS=[
    r"\.\.",
    r"/etc/passwd",
    r"windows/win\.ini",
    r"boot\.ini"
]


def detect_path(data):

    for p in PATH_PATTERNS:
        if re.search(p,data,re.I):
            return{
                "attack":"PATH TRAVERSAL",
                "severity":"MEDIUM",
                "rule":p
            }
    return None

