from pydantic import BaseModel, validator

from core.exceptions import RatingError
from typing import List
from datetime import datetime, date


class JWTPayload(BaseModel):
    user_id: int


class UserForComment(BaseModel):
    username: str
    user_role: str

    class Config:
        orm_mode = True


class CommentOut(BaseModel):
    comment_id: int
    user: UserForComment
    content: str
    rating: int
    comment_datetime: datetime

    class Config:
        orm_mode = True


class CreateComment(BaseModel):
    content: str
    rating: int

    @validator("rating")
    def check_rating(cls, v):
        if not 1 <= v <= 5:
            raise RatingError
        return v


class UserOut(BaseModel):
    user_id: int
    username: str
    user_role: str

    class Config:
        orm_mode = True


class UserDBCreds(BaseModel):
    user_id: int
    username: str
    password_hash: str

    class Config:
        orm_mode = True


class UserCreds(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    token: str
    expire: datetime


class CreateUserForDB(BaseModel):
    username: str
    password_hash: str


class Genre(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Actor(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date

    class Config:
        orm_mode = True


class Director(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date

    class Config:
        orm_mode = True


class FilmOut(BaseModel):
    id: int
    name: str
    description: str
    rating: float
    release_date: date
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
    release_date: date = None
    age_rating: int = None
