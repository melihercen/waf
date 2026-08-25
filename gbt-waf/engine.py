import re

from rules.sqli import detect_sqli
from rules.xss import detect_xss
from rules.path import detect_path
from rules.command import detect_command
from rules.ssrf import detect_ssrf
from urllib.parse import unquote_plus


DETECTORS=[
    detect_sqli,
    detect_xss,
    detect_path,
    detect_command
]
def detect_attack(query,query_params,body,headers):
    
    body=body.decode("utf-8",errors="ignore") if body else ""
    body = unquote_plus(body)

    inputs=[]

    inputs.append(query)
    inputs.extend(query_params.values())
    inputs.extend(headers.values())
    inputs.append(body)

    for detector in DETECTORS:
        for data in inputs:
            result=detector(data)
            if result:
                return result

    ssrf_inputs=[]
    ssrf_inputs.extend(query_params.values())
    ssrf_inputs.append(body)

    for data in ssrf_inputs:
        result=detect_ssrf(data)
        if result:
            return result
    return None



 