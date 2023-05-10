from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core import models
from core.database import engine
from endpoints import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=['POST', 'GET', 'PATCH'],
    allow_credentials=True,
)

app.include_router(films.router, prefix="/api/films")
