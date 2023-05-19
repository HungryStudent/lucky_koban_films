from fastapi import APIRouter, HTTPException, Depends
from config import jwt_secret, jwt_algorithm, salt
from dependencies import get_db, get_info_token
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from core import schemas, crud
from jose import jwt
import hashlib

router = APIRouter(tags=["Auth"])


def create_access_token(user_id) -> schemas.TokenData:
    expire = datetime.utcnow() + timedelta(days=30)
    token = jwt.encode({"user_id": user_id, "exp": expire}, jwt_secret, algorithm=jwt_algorithm)
    return schemas.TokenData(token=token, expire=expire)


@router.post("/reg", status_code=200, response_model=schemas.TokenData)
async def create_user_request(user_data: schemas.UserCreds, db: Session = Depends(get_db)):
    md5 = hashlib.md5()
    md5.update((user_data.password + salt).encode("utf-8"))
    password_hash = md5.hexdigest()
    user_data_for_db = schemas.CreateUserForDB(username=user_data.username, password_hash=password_hash)
    user = crud.create_user(db, user_data_for_db)
    if user == "This username already exists":
        raise HTTPException(409, "This username already exists")
    token_data = create_access_token(user.user_id)
    return token_data


@router.post("/login", status_code=200, response_model=schemas.TokenData)
async def login_user_request(user_data: schemas.UserCreds, db: Session = Depends(get_db)):
    user = crud.get_user_creds(db, user_data)
    if user is None:
        raise HTTPException(403, "Invalid username or password")
    md5 = hashlib.md5()
    md5.update((user_data.password + salt).encode("utf-8"))
    password_hash = md5.hexdigest()
    if password_hash != user.password_hash:
        raise HTTPException(403, "Invalid username or password")
    token_data = create_access_token(user.user_id)
    return token_data


@router.get('/get_me', response_model=schemas.UserOut)
async def get_me(db: Session = Depends(get_db), user_id=Depends(get_info_token)):
    return crud.get_user_by_user_id(db, user_id)
