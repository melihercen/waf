import time
from config import RATE_LIMIT_THRESHOLD, RATE_LIMIT_WINDOW

requests={}


def check_rate_limit(ip):
    current_time=time.time()

    if ip not in requests:
        requests[ip]={
            "count":1,
            "first_request":current_time
        }

        return True
    
    elapsed = current_time - requests[ip]["first_request"]
    if elapsed>=RATE_LIMIT_WINDOW:
        requests[ip]["count"] = 1
        requests[ip]["first_request"] = current_time
        return True
    requests[ip]["count"] += 1
    if requests[ip]["count"] >= RATE_LIMIT_THRESHOLD:
        return False
    else:
        return True