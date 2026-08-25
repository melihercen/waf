from fastapi.responses import JSONResponse


def block_response(result):
    return JSONResponse(
        status_code=403,
        content={
            "status":"BLOCK",
            "attack":result["attack"],
            "severity":result["severity"],
            "rule":result["rule"]
        }
    )

def error_response():
    return JSONResponse(
        status_code=500,
        content={
            "status":"ERROR",
            "message":"Internal WAF Error"
        }
    )