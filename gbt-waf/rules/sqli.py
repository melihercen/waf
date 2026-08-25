import re


SQLI_PATTERNS=[
    r"or\s+1=1",
    r"union\s+select",
    r"sleep\s*\(",
    r"benchmark\s*\("
]

def detect_sqli(data):
    

    for p in SQLI_PATTERNS:
        if re.search(p,data,re.I):
            return {
                "attack":"SQLI",
                "severity":"HIGH",
                "rule":p
            }
        
    return None
