from jose import jwt
from typing import Optional, List
from fastapi import HTTPException
from datetime import timedelta, datetime
from passlib.context import CryptContext

from ..tables import users, users_roles
from ..config import db, Envs
from ..schemas import UserSchema, UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse, RoleEnum, UserRegisterWithRole


class User:
    db = db
    users = users
    users_roles = users_roles
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    @classmethod
    async def register(cls, user: UserRegisterRequest, role_mappings: List[RoleEnum]) -> UserRegisterResponse:
        print('user', user)
        response: UserRegisterResponse
        user_id: int
        transaction = await cls.db.transaction()
        try:
            user.password = cls.pwd_context.hash(user.password)
            user_insert = cls.users.insert().values(**user.dict())
            print('user_insert', user_insert)
            user_id = await cls.db.execute(user_insert)
            print('user_id', user_id)
            for role in role_mappings:
                print('role', role.value)
            roles = [{'user_id': user_id, 'role_id': role.value} for role in role_mappings]
            print('roles', roles)
            role_insert = cls.users_roles.insert()
            print('role_insert', role_insert)
            returned_values = await cls.db.execute_many(query=role_insert, values=roles)
            print('returned_values', returned_values)
        except Exception as error:
            print('error', error)
            await transaction.rollback()
            raise HTTPException(status_code=500, detail='Failed to register account')
        else:
            print('here')
            await transaction.commit()

        return UserRegisterResponse(id=user_id)


    @classmethod
    async def login(cls, user: UserLoginRequest) -> UserLoginResponse:
        try:
            authenticated_user = await cls.authenticate_user(user.email, user.password)
            token_expires = timedelta(hours=Envs.ACCESS_TOKEN_EXPIRE_HOURS)
            jwt_token = cls.create_access_token({'sub': authenticated_user.email}, token_expires)
            return UserLoginResponse(token_type='Bearer', access_token=jwt_token)
        except Exception as error:
            raise HTTPException(status_code=400, detail='Wrong email or password')


    @classmethod
    async def authenticate_user(cls, email: str, password: str):
        try:
            user = await cls.get_user(email)
            verified = cls.pwd_context.verify(password, user.password)
            if verified:
                return user
            raise HTTPException(status_code=400, detail='Wrong email or password')
        except Exception as error:
            raise HTTPException(status_code=400, detail='Wrong email or password')


    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(hours=1)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, Envs.SECRET_KEY, algorithm=Envs.ALGORITHM)
        return encoded_jwt


    @classmethod
    async def get_user(cls, email: str) -> UserSchema:
        try:
            query = cls.users.select().where(cls.users.c.email == email)
            user_record = await cls.db.fetch_one(query)
            return UserSchema(**user_record)
        except Exception as error:
            raise HTTPException(status_code=400, detail='User not found')


class Role:
    roles_list = [RoleEnum.ADMIN, RoleEnum.FACULTY_DEAN, RoleEnum.HEAD_DEPARTEMENT, RoleEnum.TEACHER, RoleEnum.STUDENT]

