from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
if not DATABASE_URL:
    raise RuntimeError("Database URL not found in .env")