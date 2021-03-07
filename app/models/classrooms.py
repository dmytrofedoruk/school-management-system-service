from typing import List
from fastapi import HTTPException

from ..config import db, Envs
from ..tables import classrooms
from ..schemas import ClassroomSchema, CreateClassroomRequest


class Classroom:
    db = db
    classrooms = classrooms

    @classmethod
    async def create(cls, data: CreateClassroomRequest, teacher_id: int) -> ClassroomSchema:
        try:
            query_insert = cls.classrooms.insert().values(**data.dict(), teacher_id=teacher_id)
            classroom_id = await cls.db.execute(query_insert)
            classroom = await cls.get_classroom(classroom_id)
            return classroom
        except HTTPException as error:
            raise error
        except Exception as error:
            print('failed to create classroom', error)
            raise HTTPException(status_code=500, detail='Failed to create classroom')

    @classmethod
    async def get_classroom(cls, classroom_id: int) -> ClassroomSchema:
        query = cls.classrooms.select().where(cls.classrooms.c.id == classroom_id)
        record = await cls.db.fetch_one(query)
        if len(record) == 0:
            raise HTTPException(status_code=404, detail='Classroom not found')
        return ClassroomSchema(**record)

    @classmethod
    async def get_all(cls) -> List[ClassroomSchema]:
        query = cls.classrooms.select()
        records = await cls.db.fetch_all(query)
        if len(records) == 0:
            raise HTTPException(status_code=400, detail='Classroom not found')
        return [ClassroomSchema(**classroom) for classroom in records]