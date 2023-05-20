from fastapi import APIRouter, HTTPException, Depends
from dependencies import get_db, get_info_token
from sqlalchemy.orm import Session
from core import schemas, crud
from typing import List

router = APIRouter(tags=["Films"])


@router.get("/", response_model=List[schemas.FilmOut])
async def get_films_request(db: Session = Depends(get_db)):
    films = crud.get_films(db)
    res = []
    for film in films:
        my_film = schemas.FilmOut(id=film[0].id, name=film[0].name, description=film[0].description,
                                  age_rating=film[0].age_rating, release_date=film[0].release_date,
                                  actors=film[0].actors, directors=film[0].directors, genres=film[0].genres,
                                  rating=round(film[1], 1))
        res.append(my_film)
    return res


@router.get("/{film_id}", response_model=schemas.FilmOut)
async def get_film_by_id_request(film_id: int, db: Session = Depends(get_db)):
    film = crud.get_film_by_id(db, film_id)
    if film is None:
        raise HTTPException(404, f"film with id {film_id} not found")
    res = schemas.FilmOut(id=film[0].id, name=film[0].name, description=film[0].description,
                          age_rating=film[0].age_rating, release_date=film[0].release_date,
                          actors=film[0].actors, directors=film[0].directors, genres=film[0].genres,
                          rating=round(film[1], 1))
    return res


@router.patch("/{film_id}", response_model=schemas.FilmOut)
async def change_film_by_id_request(film_id: int, change_data: schemas.FilmChange, db: Session = Depends(get_db),
                                    user_id=Depends(get_info_token)):
    user = crud.get_user_by_user_id(db, user_id)
    if user.user_role not in ["moderator", "admin"]:
        raise HTTPException(403, "You not moderator or admin")

    if all(val is None for val in dict(change_data).values()):
        change_data = None
    if change_data is None:
        return crud.get_film_by_id(db, film_id)
    return crud.change_film(db, film_id, change_data)
