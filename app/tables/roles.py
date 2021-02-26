import sqlalchemy
from ..config.db import db, metadata

roles = sqlalchemy.Table(
    'roles',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('title', sqlalchemy.String(32), unique=True, nullable=False),
    sqlalchemy.Column('description', sqlalchemy.String(128), nullable=False)
)