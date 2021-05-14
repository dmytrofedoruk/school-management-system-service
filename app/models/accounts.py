from jose import jwt
from uuid import uuid4
from typing import Optional, List
from datetime import timedelta, datetime
from passlib.context import CryptContext
from sqlalchemy.sql import select, update
from fastapi import HTTPException, status, BackgroundTasks

from ..config import db, Envs
from ..tables import users, users_roles, roles
from ..utils.email import send_email, BodyEmail
from ..utils.context_managers import transaction
from ..schemas import UserSchema, UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse, RoleEnum, UserRegisterWithRole, UserVerification, ChangePasswordRequest


class User:
    db = db
    users = users
    users_roles = users_roles
    roles = roles
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    @transaction(db)
    async def register(cls, user: UserRegisterRequest, role_mappings: List[RoleEnum], background_tasks: BackgroundTasks) -> UserRegisterResponse:
        user.password = cls.pwd_context.hash(user.password)
        code = str(uuid4())
        user_insert = cls.users.insert().values(
            **user.dict(), code=code)
        user_id = await cls.db.execute(user_insert)
        roles = [{'user_id': user_id, 'role_id': role.value}
                 for role in role_mappings]
        role_insert = cls.users_roles.insert()
        returned_values = await cls.db.execute_many(query=role_insert, values=roles)
        validation_url = f'{Envs.BACKEND_URL}/accounts/verify-account?email={user.email}&verification_code={code}'
        body_email = BodyEmail(
            validation_url=validation_url,
            title='Validate Account on School Management System',
            h3='Thank you for registering!',
            p='Click this button to validate and login to your account',
            button_title='Validate'
        )
        send_email(background_tasks,
                   user.email, 'Validate your account', body_email)
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
            user_query = select([cls.users.c.id, cls.users.c.email, cls.users.c.password, cls.users.c.code, cls.users.c.is_validated, cls.users.c.username,
                                cls.users.c.fullname, cls.users.c.created_at, cls.users.c.modified_at]).where(cls.users.c.email == email)
            user_record = await cls.db.fetch_one(user_query)
            user_record = dict(**user_record)
            roles_mapping_query = select([cls.roles]).select_from(cls.users_roles.join(
                cls.roles, cls.users_roles.c.role_id == cls.roles.c.id)).where(cls.users_roles.c.user_id == user_record.get('id'))
            roles_mapping_records = await cls.db.fetch_all(roles_mapping_query)
            roles_mapping_records = [dict(**record)
                                     for record in roles_mapping_records]
            return UserSchema(**user_record, role_mappings=roles_mapping_records)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    @classmethod
    async def verify_account(cls, user_verification_data: UserVerification):
        transaction = await cls.db.transaction()
        try:
            user = await cls.get_user(user_verification_data.email)
            if user.code == user_verification_data.verification_code:
                update_query = update(cls.users).where(
                    cls.users.c.email == user_verification_data.email).values(is_validated=True, code=None)
                await cls.db.execute(query=update_query)
        except HTTPException as error:
            await transaction.rollback()
            raise error
        except Exception as error:
            await transaction.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error to validate account')
        else:
            await transaction.commit()

    @classmethod
    async def resend_email(cls, email: str, background_tasks: BackgroundTasks):
        transaction = await cls.db.transaction()
        try:
            user = await cls.get_user(email)
            code = str(uuid4())
            validation_url = f'{Envs.BACKEND_URL}/accounts/verify-account?email={user.email}&verification_code={code}'
            body_email = BodyEmail(
                validation_url=validation_url,
                title='Validate Account on School Management System',
                h3='Thank you for registering!',
                p='Click this button to validate and login to your account',
                button_title='Validate'
            )
            send_email(background_tasks,
                       user.email, 'Validate your account', body_email)
            update_query = update(cls.users).where(
                cls.users.c.email == user.email).values(is_validated=False, code=code)
            await cls.db.execute(query=update_query)
        except HTTPException as error:
            await transaction.rollback()
            raise error
        except Exception as error:
            await transaction.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error to resend email')
        else:
            await transaction.commit()

    @classmethod
    async def ask_change_password(cls, email: str, background_tasks: BackgroundTasks):
        transaction = await cls.db.transaction()
        try:
            user = await cls.get_user(email)
            code = str(uuid4())
            change_password_url = f'{Envs.FRONTEND_URL}/auth/change-password?email={user.email}&verification_code={code}'
            body_email = BodyEmail(
                validation_url=change_password_url,
                title='Change your password',
                h3='Thank you for using SSMS!',
                p='Click this button to be redirected to change your password',
                button_title='Change Password'
            )
            send_email(background_tasks,
                       user.email, 'Change password',  body_email)
            update_query = update(cls.users).where(
                cls.users.c.email == user.email).values(code=code)
            await cls.db.execute(query=update_query)
        except HTTPException as error:
            await transaction.rollback()
            raise error
        except Exception as error:
            await transaction.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error to ask change password email')
        else:
            await transaction.commit()

    @classmethod
    async def change_password(cls, request: ChangePasswordRequest, email: str, verification_code: str):
        transaction = await cls.db.transaction()
        try:
            user = await cls.get_user(email)
            if user.code == verification_code:
                update_query = update(cls.users).where(
                    cls.users.c.email == user.email).values(password=cls.pwd_context.hash(request.password), code=None)
                await cls.db.execute(query=update_query)
        except HTTPException as error:
            await transaction.rollback()
            raise error
        except Exception as error:
            await transaction.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error to change password')
        else:
            await transaction.commit()


class Role:
    roles_list = [RoleEnum.ADMIN, RoleEnum.FACULTY_DEAN,
                  RoleEnum.HEAD_DEPARTEMENT, RoleEnum.TEACHER, RoleEnum.STUDENT]
