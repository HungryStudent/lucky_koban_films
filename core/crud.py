from typing import List

from pydantic import parse_obj_as
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func, text
from sqlalchemy import func, update
from core import models, schemas
import random
import string

import hashlib

from core.database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    return db


def get_films():
    with get_db() as db:
        return db.query(models.Film).all()


def get_film_by_id(search_film_id):
    with get_db() as db:
        return db.query(models.Film).filter(models.Film.id == search_film_id).first()


def change_film(film_id, film_data: schemas.FilmChange):
    with get_db() as db:
        stmt = (
            update(models.Film).
            where(models.Film.id == film_id).
            values(film_data.dict(exclude_defaults=True)).
            returning(models.Film)
        )
        db.execute(stmt)
        db.commit()
        return db.query(models.Film).filter(models.Film.id == film_id).first()
