from typing import List

from fastapi import APIRouter, HTTPException

from core import schemas, crud

router = APIRouter(tags=["Films"])


@router.get("/", response_model=List[schemas.FilmOut])
async def get_films_request():
    films = crud.get_films()
    return films


@router.get("/{film_id}", response_model=schemas.FilmOut)
async def get_film_by_id_request(film_id: int):
    film = crud.get_film_by_id(film_id)
    if film is None:
        raise HTTPException(404, f"film with id {film_id} not found")
    return film


@router.get("/{film_id}", response_model=schemas.FilmOut)
async def get_film_by_id_request(film_id: int):
    film = crud.get_film_by_id(film_id)
    if film is None:
        raise HTTPException(404, f"film with id {film_id} not found")
    return film


@router.patch("/{film_id}", response_model=schemas.FilmOut)
async def change_film_by_id_request(film_id: int, change_data: schemas.FilmChange):
    if change_data is None:
        return crud.get_film_by_id(film_id)
    return crud.change_film(film_id, change_data)
