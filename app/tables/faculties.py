import sqlalchemy
from datetime import datetime 

from ..config.db import db, metadata


faculties = sqlalchemy.Table(
    'faculties',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(128), unique=True),
    sqlalchemy.Column('description', sqlalchemy.String(256)),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column('modified_at', sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),

    # foreign key(s)
    sqlalchemy.Column('dean_id', sqlalchemy.Integer),
    sqlalchemy.ForeignKeyConstraint(
        ['dean_id'], ['users.id'],
        name='fk_faculty_dean'
    )
)

students_faculties = sqlalchemy.Table(
    'students_faculties',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('faculty_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('faculties.id')),
    sqlalchemy.Column('student_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
)