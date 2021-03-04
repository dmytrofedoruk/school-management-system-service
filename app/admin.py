from sqlalchemy import create_engine

from .config import Envs
from .tables import users
from .models import UserModel
from .schemas import UserRegisterRequest, RoleEnum

def create_admin(user: UserRegisterRequest):
    result: any
    engine = create_engine(Envs.DATABASE_URL)

    with engine.connect() as connection:
        user.password = UserModel.pwd_context.hash(user.password)
        query = users.insert().values(**user.dict(), role_id=RoleEnum.ADMIN)
        result = connection.execute(query)
        
    return result