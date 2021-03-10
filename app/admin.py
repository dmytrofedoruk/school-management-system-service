from sqlalchemy import create_engine

from .config import Envs
from .tables import users, users_roles
from .models import UserModel
from .schemas import UserRegisterRequest, RoleEnum

def create_admin(user: UserRegisterRequest):
    engine = create_engine(Envs.DATABASE_URL)

    with engine.connect() as connection:
        with connection.begin():
            user.password = UserModel.pwd_context.hash(user.password)
            user_insert_query = users.insert().values(**user.dict()).returning(users.c.id)
            user_id, = connection.execute(user_insert_query).fetchone()
            role_insert_query = users_roles.insert()
            connection.execute(role_insert_query, [{'user_id': user_id, 'role_id': RoleEnum.ADMIN}])