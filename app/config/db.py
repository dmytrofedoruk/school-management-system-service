import sqlalchemy
from databases import Database

from .config import Envs

db = Database(Envs.DATABASE_URL)

metadata = sqlalchemy.MetaData()