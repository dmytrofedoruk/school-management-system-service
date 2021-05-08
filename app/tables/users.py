import sqlalchemy
from sqlalchemy.sql import expression
from datetime import datetime

from ..config.db import db, metadata

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('email', sqlalchemy.String(256), unique=True),
    sqlalchemy.Column('password', sqlalchemy.String(256)),
    sqlalchemy.Column('username', sqlalchemy.String(64), nullable=True),
    sqlalchemy.Column('fullname', sqlalchemy.String(128), nullable=True),
    sqlalchemy.Column('is_validated', sqlalchemy.Boolean, nullable=False,
                      server_default=expression.false()),
    sqlalchemy.Column('code', sqlalchemy.String(256), nullable=True),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime,
                      server_default=sqlalchemy.func.now()),
    sqlalchemy.Column('modified_at', sqlalchemy.DateTime,
                      server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())
)

users_roles = sqlalchemy.Table(
    'user_role_mappings',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('role_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('roles.id'))
)
