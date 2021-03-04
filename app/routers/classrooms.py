from fastapi import APIRouter, Depends

from ..dependencies import get_user
from ..schemas import UserSchema


classroom_router = APIRouter(prefix='/classrooms', tags=['classrooms'])

@classroom_router.get('/')
async def index(user: UserSchema = Depends(get_user)):
    return {'message': 'This is classrooms route index'}