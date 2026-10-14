from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.lib.database import Base, engine
from src.lib.config import CORS_ORIGIN

from src.models import employee

from src.routers import employee_router

app = FastAPI()

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

app.add_middleware(CORSMiddleware,
                   allow_origins=CORS_ORIGIN,
                   allow_credentials=True,
                   allow_methods=["*"],
                   )