from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ..models import UserModel, FacultyModel
from ..dependencies import get_user
from ..schemas import FacultySchema, CreateFacultyRequest, UserSchema, RoleEnum


faculties_router = APIRouter(prefix='/faculties', tags=['faculties'])


@faculties_router.get('/')
async def index(user: UserModel = Depends(get_user)):
    return {'message': 'This is faculties details route index'}

@faculties_router.post('/create', response_model=FacultySchema)
async def create_faculty(request: CreateFacultyRequest, user: UserSchema = Depends(get_user)):
    if user.role_id != RoleEnum.FACULTY_DEAN:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='You are not allowed to create faculty')
    response = await FacultyModel.create(request, user.id)
    return response

@faculties_router.get('/get/all', response_model=List[FacultySchema])
async def get_all_faculties(user: UserSchema = Depends(get_user)):
    response = await FacultyModel.get_all()
    return response

@faculties_router.get('/get/{faculty_id}', response_model=FacultySchema)
async def get_faculty(faculty_id: int, user: UserSchema = Depends(get_user)):
    response = await FacultyModel.get_faculty(faculty_id)
    return response