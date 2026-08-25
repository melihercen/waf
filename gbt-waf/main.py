from atexit import register

from fastapi import FastAPI
from fastapi import Request
from starlette.middleware.sessions import SessionMiddleware

import bcrypt
from config import SECRET_KEY,ADMIN_USERNAME, ADMIN_PASSWORD_HASH

from admin_rate_limiter import (
    check_admin_login_limit,
    register_failed_login,
    reset_failed_logins
)

from proxy import forward_request
from fastapi.responses import Response

from waf_service import process_request
from rate_limiter import check_rate_limit


from database import cursor
from fastapi.templating import Jinja2Templates


from fastapi import Form
from fastapi.responses import RedirectResponse

import time


app=FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
session_cookie="waf_admin_sessions",
    same_site="lax",
    https_only=True,
    max_age=1800
)





templates = Jinja2Templates(directory="templates")

@app.get("/admin/login")
async def admin_login_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request":request
        }
    )
@app.post("/admin/login")
async def admin_login(
    request:Request,
    username:str= Form(...),
    password:str=Form(...)
):
    ip=request.client.host

    if not check_admin_login_limit(ip):
        return templates.TemplateResponse(
            "login.html",
            {
                "request":request,
                "error":"Çok fazla hatalı giriş yapıldı. 5 dakika sonra tekrar deneyin."
            },
            status_code=429
        )
    
    if username==ADMIN_USERNAME and bcrypt.checkpw(password.encode("utf-8"), ADMIN_PASSWORD_HASH.encode("utf-8")):
        reset_failed_logins(ip)
        request.session["admin"]=True

        return RedirectResponse(
            url="/admin/dashboard",
            status_code=303
        )

    register_failed_login(ip)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request":request,
            "error":"Kullanıcı adı veya şifre yanlış."
        },
        status_code=401
    )

@app.get("/admin/logout")
async def admin_logout(request:Request):
    request.session.clear()
    return RedirectResponse(
        url="/admin/login",
        status_code=303
    )

@app.get("/admin/dashboard")
async def dashboard(request:Request):
    if not request.session.get("admin"):
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )

    cursor.execute("SELECT COUNT(*) FROM logs")
    total=cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE attack=?",("SQLI",)
    )
    sqli=cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE attack=?",("XSS",)
    )
    xss=cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE attack=?",("PATH TRAVERSAL",)
    )
    path_count=cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE attack=?",("COMMAND INJECTION",)
    )
    command=cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE attack=?",("SSRF",)
    )
    ssrf=cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            time,
            ip,
            method,
            path,
            attack,
            severity
        FROM logs
        ORDER BY id DESC
        LIMIT 10
    """)

    rows=cursor.fetchall()
    logs=[]

    for row in rows:
        logs.append({
            "time":row[0],
            "ip":row[1],
            "method":row[2],
            "path":row[3],
            "attack":row[4],
            "severity":row[5]
        })

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total":total,
            "sqli":sqli,
            "xss":xss,
            "path_count":path_count,
            "command":command,
            "ssrf":ssrf,
            "logs":logs[-10:],

            "chart_data":[
                sqli,
                xss,
                path_count,
                command,
                ssrf
            ]
        }
    )

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "waf"
    }

@app.api_route("/{path:path}",methods=["GET","POST","PUT","DELETE","PATCH"])

async def waf(request:Request,path:str):

    waf_start = time.perf_counter()

    query=str(request.url)
    query_params=dict(request.query_params)
    ip = request.headers.get("x-real-ip") or request.client.host
    method=request.method
    path=request.url.path
    query_string=request.url.query
    if query_string:
        path=path+"?"+query_string
    headers=dict(request.headers)
    body=await request.body()
    user_agent=headers.get("user-agent","Unknown")
 
    
    
    

    if not check_rate_limit(ip):
        return {
        "status": "RATE_LIMIT"
    }

    process_start = time.perf_counter()
    
    result=process_request(ip,method,path,user_agent,query,query_params,body,headers)

    process_end = time.perf_counter()

    process_time = (process_end - process_start) * 1000

    print(f"Detection süresi: {process_time:.2f} ms")
    
    if result:
        return result
    

    start = time.perf_counter()

    response = await forward_request(
        method,
        path,
        headers,
        body
    )

    end = time.perf_counter()

    proxy_time = (end - start) * 1000

    print(f"Proxy süresi: {proxy_time:.2f} ms")
    
    response=await forward_request(
        method,
        path,
        headers,
        body
    )
    

    waf_end = time.perf_counter()

    total_waf_time = (waf_end - waf_start) * 1000

    print(f"Toplam WAF süresi: {total_waf_time:.2f} ms")
    
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )

    