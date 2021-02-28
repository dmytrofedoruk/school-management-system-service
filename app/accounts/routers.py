from fastapi import APIRouter

from . import schemas
from .models import User

account_router = APIRouter(prefix='/accounts', tags=['accounts'])

@account_router.get('/')
async def index():
    return {'message': 'This is accounts route index'}

@account_router.post('/register', response_model=schemas.UserRegisterResponse)
async def register(user: schemas.UserRegisterRequest):
    new_user_response = await User.register(user)
    return new_user_response.dict()

@account_router.post('/login', response_model=schemas.UserLoginResponse)
async def login(user: schemas.UserLoginRequest):
    response = await User.login(user)
    return response.dict()
