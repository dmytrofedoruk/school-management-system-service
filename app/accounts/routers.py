from fastapi import APIRouter

account_router = APIRouter(prefix='/accounts', tags=['accounts'])

@account_router.get('/')
async def index():
    return {'message': 'This is account index'}
