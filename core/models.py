from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, Float, UniqueConstraint, TIMESTAMP, DATE, SMALLINT
from sqlalchemy.orm import relationship

from .database import Base


class Actor(Base):
    __tablename__ = "actor"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
    date_of_birth = Column(DATE())


class Director(Base):
    __tablename__ = "director"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
    date_of_birth = Column(DATE())


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(50))


class Film(Base):
    __tablename__ = "film"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(50))
    description = Column(VARCHAR(1000))
    age_rating = Column(Integer())
    rating = Column(Float())
    release_date = Column(DATE())

    actors = relationship("Actor", secondary="actor_film", lazy='subquery')
    directors = relationship("Director", secondary="director_film", lazy='subquery')
    genres = relationship("Genre", secondary="genre_film", lazy='subquery')


class ActorFilm(Base):
    __tablename__ = "actor_film"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey(Actor.id))
    film_id = Column(Integer, ForeignKey(Film.id))


class DirectorFilm(Base):
    __tablename__ = "director_film"

    id = Column(Integer, primary_key=True, index=True)
    director_id = Column(Integer, ForeignKey(Director.id))
    film_id = Column(Integer, ForeignKey(Film.id))


class GenreFilm(Base):
    __tablename__ = "genre_film"

    id = Column(Integer, primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey(Genre.id))
    film_id = Column(Integer, ForeignKey(Film.id))


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR(32), unique=True)
    password_hash = Column(VARCHAR(32))
    user_role = Column(VARCHAR(10), default="user")


class Comment(Base):
    __tablename__ = "comment"
    __table_args__ = (UniqueConstraint('film_id', 'user_id', name='one_comment'),)

    comment_id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey(Film.id))
    user_id = Column(Integer, ForeignKey(Users.user_id))
    content = Column(VARCHAR(2048))
    rating = Column(SMALLINT)
    comment_datetime = Column(TIMESTAMP)

    user = relationship("Users", foreign_keys=[user_id])
