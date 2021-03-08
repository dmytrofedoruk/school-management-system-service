from sqlalchemy import create_engine

from .config import Envs
from .tables import users, users_roles
from .models import UserModel
from .schemas import UserRegisterRequest, RoleEnum

def create_admin(user: UserRegisterRequest):
    result: any = None
    engine = create_engine(Envs.DATABASE_URL)

    with engine.connect() as connection:
        with connection.begin():
            user.password = UserModel.pwd_context.hash(user.password)
            user_insert_query = users.insert().values(**user.dict())
            print('user_insert_query', user_insert_query)
            user_id = connection.execute(user_insert_query)
            print('user_id', user_id)
            role_insert_query = users_roles.insert()
            result = connection.execute(role_insert_query, [{'user_id': user_id, 'role_id': RoleEnum.ADMIN}])
        
    return result