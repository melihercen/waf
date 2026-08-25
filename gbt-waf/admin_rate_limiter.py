import time


failed_attempts={}

MAX_ATTEMPTS= 5
BLOCK_TIME=300


def check_admin_login_limit(ip):
    current_time=time.time()

    if ip not in failed_attempts:
        return True

    data=failed_attempts[ip]

    if data["blocked_until"]>current_time:
        return False

    if data["blocked_until"]!=0 and data["blocked_until"]<=current_time:
        failed_attempts.pop(ip)
        return True 
    return True

def register_failed_login(ip):
    current_time=time.time()

    if ip not in failed_attempts:
        failed_attempts[ip]={
            "count":1,
            "blocked_until":0
        }
        return
    failed_attempts[ip]["count"]+=1

    if failed_attempts[ip]["count"] >= MAX_ATTEMPTS:
        failed_attempts[ip]["blocked_until"]= current_time + BLOCK_TIME

def reset_failed_logins(ip):
    failed_attempts.pop(ip,None)