from starlette.middleware.cors import CORSMiddleware
from core.database import engine
from fastapi import FastAPI
from core import models
from endpoints import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=['POST', 'GET', 'PATCH'],
    allow_credentials=True,
)

app.include_router(films.router, prefix="/api/films")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(admin.router, prefix="/api/admin")
app.include_router(comments.router, prefix="/api/comments")
exceptions.add_handlers(app)
