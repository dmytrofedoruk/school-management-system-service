import sqlalchemy
from datetime import datetime

from ..config.db import db, metadata


classrooms = sqlalchemy.Table(
    'classrooms',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(128), unique=True),
    sqlalchemy.Column('description', sqlalchemy.String(256)),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column('modified_at', sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),

    sqlalchemy.Column('owner_id', sqlalchemy.Integer),
    sqlalchemy.ForeignKeyConstraint(
        ['owner_id'], ['users.id'],
        name='fk_classroom_owner'
    )
)

students_classrooms = sqlalchemy.Table(
    'students_classrooms',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('classroom_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('classrooms.id')),
    sqlalchemy.Column('student_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
)