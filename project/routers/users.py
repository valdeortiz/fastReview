from typing import List
from fastapi import HTTPException
from fastapi import Response
from fastapi import Cookie
from fastapi.routing import APIRouter
from ..database import User
from ..schemas import ReviewResponseModel, UserRequestModel,UserResponseModel
from fastapi.security import HTTPBasicCredentials
router = APIRouter(prefix='/users')

@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El username ya se encuentra en uso.')

    hash_password = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_password
    )

    return user

@router.post('/login', response_model=UserResponseModel)
async def login(credential: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credential.username).first()
    if user is None:
        raise HTTPException(404, 'USer not found')

    if user.password != User.create_password(credential.password):
        raise HTTPException(404, 'Password Error')

    response.set_cookie(key='user_id', value=user.id)

    return user

@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):
    user = User.select().where(User.id == user_id).first()
    if user is None:
        raise HTTPException(404, 'User no encontrado')

    return [user_review for user_review in user.reviews]
