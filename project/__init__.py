from fastapi import FastAPI
from fastapi.routing import APIRouter
from .database import database as connection
from .database import UserReview, User, Movie


from .routers import user_router, revirew_router

app = FastAPI(title='Proyecto para resenar pelicular',
            description='Proyecto de resenas de peliculas',
            version='1',
)

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(revirew_router)

app.include_router(api_v1)

@app.on_event('startup')
async def startup():
    if connection.is_closed():
        connection.connect()
        print('conect')

    connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
async def shutdown():
    if not connection.is_closed():
        connection.close()
        print('close')
