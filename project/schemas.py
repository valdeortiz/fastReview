from pydantic import BaseModel
from pydantic import validator
from pydantic.utils import GetterDict

from peewee import ModelSelect
from typing import Any

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

# ----------- User -----------

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La longitud debe ser mayor a 3 caracteres y menor a 50')
        
        return username

class UserResponseModel(ResponseModel):
    id: int
    username: str


# ----------- Movie -----------
class MovieResponseModel(ResponseModel):
    id: int
    title:str

# ----------- Review -----------

class ReviewValidator():
    @validator('score')
    def username_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('La puntuacion debe ser mayor a 1 y menor a 5')
        return score

class ReviewRequestModel(BaseModel, ReviewValidator):
    user_id: int
    movie_id: int
    review: str
    score: int

class ReviewResponseModel(ResponseModel):
    id: int
    movie: MovieResponseModel
    review: str
    score: int

class ReviewRequestPutModel(BaseModel, ReviewValidator):
    review: str
    score: int

