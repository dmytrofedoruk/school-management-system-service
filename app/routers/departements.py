from fastapi import APIRouter, Depends

from ..dependencies import get_user
from ..schemas import UserSchema


departement_router = APIRouter(prefix='/departements', tags=['departements'])

@departement_router.get('/')
async def index(user: UserSchema = Depends(get_user)):
    return {'message': 'This is departements route index'}