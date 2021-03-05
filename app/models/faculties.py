from typing import List
from fastapi import HTTPException

from ..config import db, Envs
from ..tables import faculties
from ..schemas import FacultySchema, CreateFacultyRequest

class Faculty:
    db = db
    faculties = faculties

    @classmethod
    async def create(cls, data: CreateFacultyRequest, dean_id: int) -> FacultySchema:
        try:
            query_insert = cls.faculties.insert().values(**data.dict, dean_id=dean_id)
            faculty_id = await cls.db.execute(query_insert)
            faculty = await cls.get_faculty(faculty_id)
            return faculty
        except HTTPException as error:
            raise error
        except Exception as error:
            print('Error to create faculties', error)
            raise HTTPException(status_code=500, detail='Internal server error')

    @classmethod
    async def get_faculty(cls, faculty_id: int) -> FacultySchema:
        query = cls.faculties.select().values(cls.faculties.c.id == faculty_id)
        record = await cls.db.fetch_one(query)
        if len(record) == 0:
            raise HTTPException(status_code=404, detail='Faculty not found')
        return FacultySchema(**record)

    @classmethod
    async def get_all(cls) -> List[FacultySchema]:
        query = cls.faculties.select()
        records = await cls.db.fetch_all(query)
        if len(records) == 0:
            raise HTTPException(status_code=404, detail='Faculty not found')
        return [FacultySchema(**faculty) for faculty in records]