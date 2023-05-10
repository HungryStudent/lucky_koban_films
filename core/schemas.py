import datetime

from typing import List

from pydantic import BaseModel


class Genre(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Actor(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: datetime.date

    class Config:
        orm_mode = True


class Director(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: datetime.date

    class Config:
        orm_mode = True


class FilmOut(BaseModel):
    id: int
    name: str
    description: str
    rating: float
    release_date: datetime.date
    age_rating: int

    genres: List[Genre]
    actors: List[Actor]
    directors: List[Director]

    class Config:
        orm_mode = True


class FilmChange(BaseModel):
    name: str = None
    description: str = None
    rating: float = None
    release_date: datetime.date = None
    age_rating: int = None

    def __new__(cls, *args, **kwargs):
        if all(v is None for v in args) and all(v is None for v in kwargs.values()):
            pass
        else:
            return super().__new__(cls)
