from fastapi import APIRouter

classroom_router = APIRouter(prefix='/classrooms', tags=['classrooms'])

@classroom_router.get('/')
async def index('user')