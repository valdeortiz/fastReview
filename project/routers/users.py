from fastapi import HTTPException
from fastapi.routing import APIRouter
from ..database import User
from ..schemas import UserRequestModel,UserResponseModel
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
async def login(credential: HTTPBasicCredentials):
    user = User.select().where(User.username == credential.username).first()
    if user is None:
        raise HTTPException(404, 'USer not found')

    if user.password != User.create_password(credential.password):
        raise HTTPException(404, 'Password Error')

    return user