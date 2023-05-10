from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, Table, VARCHAR, Float, \
    ForeignKeyConstraint, UniqueConstraint, TIMESTAMP, DATE
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
