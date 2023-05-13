from core.database import SessionLocal
from config import jwt_secret
from fastapi import Header
from jose import jwt


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_info_token(authorization: str = Header()):
    user_data = jwt.decode(authorization, jwt_secret, algorithms="HS256")
    return user_data["user_id"]
