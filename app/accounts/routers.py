from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from . import schemas
from .models import User

account_router = APIRouter(prefix='/accounts', tags=['accounts'])

@account_router.get('/')
async def index():
    return {'message': 'This is accounts route index'}

@account_router.post('/register', response_model=schemas.UserRegisterResponse)
async def register(user: schemas.UserRegisterRequest):
    response = await User.register(user)
    return response.dict()

@account_router.post('/login', response_model=schemas.UserLoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = schemas.UserLoginRequest(email=form_data.username, password=form_data.password)
    response = await User.login(user)
    return response.dict()

