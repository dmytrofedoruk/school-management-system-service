from passlib.context import CryptContext

from ..config.db import db
from ..tables.users import users
from ..tables.roles import roles

pwd_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])

class User:
    @classmethod
    async def register(cls, **user):
        hashed_password = pwd_context.hash(user.password)
        query = users.insert().values(**user, password=hashed_password)
        user_id = await db.execute(query)
        return user_id
