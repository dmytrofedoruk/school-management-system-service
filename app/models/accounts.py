from jose import jwt
from typing import Optional
from fastapi import HTTPException
from datetime import timedelta, datetime
from passlib.context import CryptContext

from ..tables import users
from ..config import db, Envs
from ..schemas import UserSchema, UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse


class User:
    db = db
    users = users
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    @classmethod
    async def register(cls, user: UserRegisterRequest) -> UserRegisterResponse:
        try:
            user.password = cls.pwd_context.hash(user.password)
            query = cls.users.insert().values(**user.dict())
            user_id = await cls.db.execute(query)
            new_user_response = UserRegisterResponse(id=user_id)
            return new_user_response
        except Exception as error:
            raise HTTPException(status_code=400, detail='Email has been registered')


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
            query = cls.users.select().where(users.c.email == email)
            user_record = await cls.db.fetch_one(query)
            return UserSchema(**user_record)
        except Exception as error:
            raise HTTPException(status_code=400, detail='User not found')

