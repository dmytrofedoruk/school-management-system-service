from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_user
from ..models import RoleModel, ClassroomModel
from ..schemas import UserSchema, ClassroomSchema, CreateClassroomRequest, RoleEnum


classroom_router = APIRouter(prefix='/classrooms', tags=['classrooms'])


@classroom_router.get('/')
async def index(user: UserSchema = Depends(get_user)):
    return {'message': 'This is classrooms route index'}


@classroom_router.post('/create', response_model=ClassroomSchema)
async def create_classroom(request: CreateClassroomRequest, user: UserSchema = Depends(get_user)):
    if user.role_id != RoleEnum.TEACHER:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='You are not allowed to create classroom')
    response = await ClassroomModel.create(request, user.id)
    return response

@classroom_router.get('/get/all', response_model=List[ClassroomSchema])
async def get_all_classrooms(user: UserSchema = Depends(get_user)):
    response = await ClassroomModel.get_all()
    return response

@classroom_router.get('/get/{classroom_id}', response_model=ClassroomSchema)
async def get_classroom(classroom_id: int, user: UserSchema = Depends(get_user)):
    response = await ClassroomModel.get_classroom(classroom_id)
    return response
