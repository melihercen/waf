import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://host.docker.internal:3000"
)

RATE_LIMIT_WINDOW = 60

RATE_LIMIT_THRESHOLD = 100