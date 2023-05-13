from fastapi.responses import Response, JSONResponse
from fastapi import FastAPI, Request
from jose import JWTError

from core.exceptions import *


def auth_exception_handler(request: Request, exc: JWTError):
    return Response(status_code=401)


def rating_exception_handler(request: Request, exc: RatingError):
    return JSONResponse(status_code=400, content={"detail": "the rating value should be between 1 and 5"})


def add_handlers(my_app: FastAPI):
    my_app.add_exception_handler(JWTError, auth_exception_handler)
    my_app.add_exception_handler(RatingError, rating_exception_handler)
