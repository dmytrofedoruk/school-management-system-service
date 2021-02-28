from fastapi import HTTPException
from passlib.context import CryptContext

from . import schemas
from ..config.db import db
from ..tables.users import users
from ..tables.roles import roles

pwd_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])

class User:
    @classmethod
    async def register(cls, user: schemas.UserRegisterRequest) -> schemas.UserRegisterResponse:
        try:
            user.password = pwd_context.hash(user.password)
            query = users.insert().values(**user.dict())
            user_id = await db.execute(query)
            new_user_response = schemas.UserRegisterResponse(id=user_id)
            return new_user_response
        except:
            raise HTTPException(status_code=400, detail='Email has been registered')

    @classmethod
    async def login(cls, **user):
        try:
            pass
        except:
            raise HTTPException(status_code=400, detail='Wrong email or password')
