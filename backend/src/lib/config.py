from dotenv import load_dotenv
from sqlalchemy.engine import URL
import os

load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB"),
)
if not DATABASE_URL:
    raise RuntimeError("Database URL not found")