from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models import UserModel
from ..dependencies import get_user
from ..schemas import UserSchema, UserLoginRequest, UserLoginResponse, UserRegisterRequest, UserRegisterResponse


account_router = APIRouter(prefix='/accounts', tags=['accounts'])


@account_router.get('/')
async def index(user: UserSchema = Depends(get_user)):
    return {'message': 'This is accounts route index'}

@account_router.post('/register', response_model=UserRegisterResponse)
async def register(user: UserRegisterRequest):
    """
    Register a user with all the information:

    - **email**: user email, must be unique
    - **password**: user password
    - **username**: optional
    - **fullname**: optional
    - **role_id**: user role, 1 for Admin, 2 for Teacher and 3 for Student 
    """
    response = await UserModel.register(user)
    return response.dict()

@account_router.post('/login', response_model=UserLoginResponse)
async def login(user: UserLoginRequest):
    """
    Login user to get token with these required informations:

    - **email**: user email, must be unique
    - **password**: user password
    """
    response = await UserModel.login(user)
    return response.dict()

@account_router.get('/profile')
async def get_profile(user: UserSchema = Depends(get_user)):
    """
    Get logged in user's data
    """
    return user.dict()
