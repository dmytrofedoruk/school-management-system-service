import sqlalchemy
from ..config.db import db, metadata

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('email', sqlalchemy.String(256), unique=True),
    sqlalchemy.Column('username', sqlalchemy.String(64), nullable=True),
    sqlalchemy.Column('fullname', sqlalchemy.String(128), nullable=True),
)