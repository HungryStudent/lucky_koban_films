from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, update
from sqlalchemy.orm import Session
from core import models, schemas


def get_films(db: Session):
    return db.query(models.Film, func.avg(models.Comment.rating).label("count")).group_by(models.Film.id).all()


def get_film_by_id(db: Session, search_film_id):
    return db.query(models.Film, func.avg(models.Comment.rating).label("count")).join(models.Comment).filter(
        models.Film.id == search_film_id).group_by(models.Film.id).first()


def change_film(db: Session, film_id, film_data: schemas.FilmChange):
    stmt = (
        update(models.Film).
        where(models.Film.id == film_id).
        values(film_data.dict(exclude_defaults=True)).
        returning(models.Film)
    )
    db.execute(stmt)
    db.commit()
    return db.query(models.Film).filter(models.Film.id == film_id).first()


def create_user(db: Session, user_data: schemas.CreateUserForDB):
    user = models.Users(username=user_data.username, password_hash=user_data.password_hash)
    db.add(user)

    try:
        db.flush()
    except IntegrityError:
        return "This username already exists"
    db.commit()
    return user


def get_user_by_username(db: Session, user_data: schemas.UserCreds) -> schemas.UserOut:
    return db.query(models.Users).filter(user_data.username == models.Users.username).first()


def get_user_by_user_id(db: Session, user_id) -> schemas.UserOut:
    return db.query(models.Users).filter(user_id == models.Users.user_id).first()


def get_user_creds(db: Session, user_data: schemas.UserCreds) -> schemas.UserDBCreds:
    return db.query(models.Users).filter(models.Users.username == user_data.username).first()


def update_role_by_user_id(db: Session, user_id, user_role) -> schemas.UserOut:
    db.query(models.Users).filter(models.Users.user_id == user_id).update({"user_role": user_role})
    return db.query(models.Users).filter(user_id == models.Users.user_id).first()


def get_comments_by_film_id(db: Session, film_id):
    return db.query(models.Comment).filter(film_id == models.Comment.film_id).all()


def create_comment(db: Session, film_id, user_id, comment_data: schemas.CreateComment):
    comment = models.Comment(film_id=film_id, user_id=user_id, content=comment_data.content, rating=comment_data.rating,
                             comment_datetime=func.now())
    db.add(comment)

    try:
        db.flush()
    except IntegrityError:
        return "This user has already left a comment on this film"
    db.commit()
    return comment
