from jose import jwt
from hashlib import md5
from typing import Optional, List
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi import HTTPException, status, BackgroundTasks

from ..config import db, Envs
from ..utils.email import send_email
from ..tables import users, users_roles
from ..schemas import UserSchema, UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse, RoleEnum, UserRegisterWithRole, UserVerification


class User:
    db = db
    users = users
    users_roles = users_roles
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def register(cls, user: UserRegisterRequest, role_mappings: List[RoleEnum], background_tasks: BackgroundTasks) -> UserRegisterResponse:
        response: UserRegisterResponse
        user_id: int
        transaction = await cls.db.transaction()
        try:
            user.password = cls.pwd_context.hash(user.password)
            code = md5(user.email.encode()).hexdigest()
            user_insert = cls.users.insert().values(
                **user.dict(), code=code)
            user_id = await cls.db.execute(user_insert)
            roles = [{'user_id': user_id, 'role_id': role.value}
                     for role in role_mappings]
            role_insert = cls.users_roles.insert()
            returned_values = await cls.db.execute_many(query=role_insert, values=roles)
            validation_url = f'{Envs.BACKEND_URL}/accounts/verify-account?email={user.email}&verification_code={code}'
            send_email(background_tasks,
                       user.email, validation_url)
        except Exception as error:
            await transaction.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to register account')
        else:
            await transaction.commit()

        return UserRegisterResponse(id=user_id)

    @classmethod
    async def login(cls, user: UserLoginRequest) -> UserLoginResponse:
        try:
            authenticated_user = await cls.authenticate_user(user.email, user.password)
            token_expires = timedelta(hours=Envs.ACCESS_TOKEN_EXPIRE_HOURS)
            jwt_token = cls.create_access_token(
                {'sub': authenticated_user.email}, token_expires)
            return UserLoginResponse(token_type='Bearer', access_token=jwt_token)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Wrong email or password')

    @classmethod
    async def authenticate_user(cls, email: str, password: str):
        try:
            user = await cls.get_user(email)
            verified = cls.pwd_context.verify(password, user.password)
            if verified:
                return user
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong email or password')
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong email or password')

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(hours=1)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, Envs.SECRET_KEY, algorithm=Envs.ALGORITHM)
        return encoded_jwt

    @classmethod
    async def get_user(cls, email: str) -> UserSchema:
        try:
            query = cls.users.select().where(cls.users.c.email == email)
            user_record = await cls.db.fetch_one(query)
            return UserSchema(**user_record)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    @classmethod
    async def verify_account(cls, user_verification_data: UserVerification):
        try:
            print('user_verification_data.email', user_verification_data.email)
            user = await cls.get_user(user_verification_data.email)
            print('verify user', user)
            if user.code == user_verification_data.verification_code:
                return True
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong verification code')
        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error to validate account')


class Role:
    roles_list = [RoleEnum.ADMIN, RoleEnum.FACULTY_DEAN,
                  RoleEnum.HEAD_DEPARTEMENT, RoleEnum.TEACHER, RoleEnum.STUDENT]
