from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from . import schemas
from .models import User
from .dependencies import get_user


account_router = APIRouter(prefix='/accounts', tags=['accounts'])


@account_router.get('/')
async def index(user: User = Depends(get_user)):
    return {'message': 'This is accounts route index'}

@account_router.post('/register', response_model=schemas.UserRegisterResponse)
async def register(user: schemas.UserRegisterRequest):
    """
    Register a user with all the information:

    - **email**: user email, must be unique
    - **password**: user password
    - **username**: optional
    - **fullname**: optional
    - **role_id**: user role, 1 for Admin, 2 for Teacher and 3 for Student 
    """
    response = await User.register(user)
    return response.dict()

@account_router.post('/login', response_model=schemas.UserLoginResponse)
async def login(user: schemas.UserLoginRequest):
    """
    Login user to get token with these required informations:

    - **email**: user email, must be unique
    - **password**: user password
    """
    response = await User.login(user)
    return response.dict()

@account_router.get('/profile')
async def get_profile(user: User = Depends(get_user)):
    """
    Get logged in user's data
    """
    return user.dict()
