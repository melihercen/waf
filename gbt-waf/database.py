import sqlite3
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent
DB_PATH=BASE_DIR / "logs" / "logs.db"
conn= sqlite3.connect(
    DB_PATH,
    check_same_thread=False

)


cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
time TEXT,
ip TEXT,
method TEXT,
path TEXT,
user_agent TEXT,
attack TEXT,
severity TEXT,
rule TEXT,
url TEXT
)
""")

conn.commit()