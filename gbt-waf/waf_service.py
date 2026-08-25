from engine import detect_attack
from logger import save_log
from responses import block_response
from responses import error_response

def process_request(ip,method,path,user_agent,query,query_params,body,headers):
    result=detect_attack(query,query_params,body,headers)
    try:
        if result:
            save_log(ip,method,path,user_agent,result["attack"],result["severity"],result["rule"],query)

            return block_response(result)
        
        return None
    except Exception as e:
        print(f"WAF Error: {e}")
        return error_response()
