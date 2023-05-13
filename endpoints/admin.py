from fastapi import APIRouter, HTTPException, Depends
from dependencies import get_db, get_info_token
from config import jwt_secret, jwt_algorithm
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from core import schemas, crud
from jose import jwt

router = APIRouter(tags=["Admin"])


def create_access_token(user_id):
    expire = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode({"user_id": user_id, "exp": expire}, jwt_secret, algorithm=jwt_algorithm)
    return token


@router.patch("/role/{user_id}", status_code=200, response_model=schemas.UserOut)
async def create_user_request(user_id: int, new_role: str, db: Session = Depends(get_db),
                              my_user_id=Depends(get_info_token)):
    if my_user_id == "error":
        raise HTTPException(403)

    user = crud.get_user_by_user_id(db, my_user_id)
    if user.user_role != "admin":
        raise HTTPException(403, "Forbidden")

    return crud.update_role_by_user_id(db, user_id, new_role)
