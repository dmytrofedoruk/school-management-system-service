from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_user
from ..models import RoleModel, DepartementModel
from ..schemas import UserSchema, DepartementSchema, CreateDepartementRequest, RoleEnum


departement_router = APIRouter(prefix='/departements', tags=['departements'])


@departement_router.get('/')
async def index(user: UserSchema = Depends(get_user)):
    return {'message': 'This is departements route index'}


@departement_router.post('/create', response_model=DepartementSchema)
async def create_departement(request: CreateDepartementRequest, user: UserSchema = Depends(get_user)):
    if user.role_id != RoleEnum.HEAD_DEPARTEMENT:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='You are not allowed to create departement')
    response = await DepartementModel.create(request, user.id)
    return response

@departement_router.get('/get/all', response_model=List[DepartementSchema])
async def get_all_departements(user: UserSchema = Depends(get_user)):
    response = await DepartementModel.get_all()
    return response

@departement_router.get('/get/{departement_id}', response_model=DepartementSchema)
async def get_departement(departement_id: int, user: UserSchema = Depends(get_user)):
    response = await DepartementModel.get_departement(departement_id)
    return response
