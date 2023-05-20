from fastapi import APIRouter, HTTPException, Depends
from dependencies import get_db, get_info_token
from sqlalchemy.orm import Session
from core import schemas, crud
from typing import List

router = APIRouter(tags=["Comments"])


@router.get("/{film_id}", response_model=List[schemas.CommentOut])
async def get_comments_by_film_id_request(film_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_film_id(db, film_id)


@router.post("/{film_id}", response_model=schemas.CommentOut)
async def create_comment_request(film_id, comment_data: schemas.CreateComment, db: Session = Depends(get_db),
                                 user_id=Depends(get_info_token)):
    print(comment_data)
    comment = crud.create_comment(db, film_id, user_id, comment_data)
    if comment == "This user has already left a comment on this film":
        raise HTTPException(409, "have you already left a comment on this movie")
    return comment
