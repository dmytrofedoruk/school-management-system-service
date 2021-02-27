from fastapi import APIRouter
from .models import User
from .schemas import UserRegisterResponse, UserRegisterRequest

account_router = APIRouter(prefix='/accounts', tags=['accounts'])

@account_router.get('/')
async def index():
    return {'message': 'This is account index'}

@account_router.post('/create', response_model=UserRegisterResponse)
async def create_user(user: UserRegisterRequest):
    new_user = User.register(**user)
    return new_user
