from database import conn,cursor
from datetime import datetime

def save_log(ip,method,path,user_agent,attack,severity,rule,url):
    cursor.execute("""
INSERT INTO logs(
time,
ip,
method,
path,
user_agent,
attack,
severity,
rule,
url)
VALUES(?,?,?,?,?,?,?,?,?)
""",
(
str(datetime.now()),
ip,
method,
path,
user_agent,
attack,
severity,
rule,
url
))
    conn.commit()