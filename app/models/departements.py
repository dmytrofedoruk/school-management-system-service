from typing import List
from fastapi import HTTPException

from ..config import db, Envs
from ..tables import departements
from ..schemas import CreateDepartementRequest, DepartementSchema


class Departement:
    db = db
    departements = departements

    @classmethod
    async def create(cls, data: CreateDepartementRequest, head_id: int) -> DepartementSchema:
        try:
            query_insert = cls.departements.insert().values(**data.dict(), head_id=head_id)
            departement_id = await cls.db.execute(query_insert)
            departement = await cls.get_departement(departement_id)
            return departement
        except Exception as error:
            print('failed to create deparement', error)
            raise HTTPException(status_code=500, detail='Failed to create departement')

    @classmethod
    async def get_departement(cls, departement_id: int) -> DepartementSchema:
        query = cls.departements.select().where(cls.departements.c.id == departement_id)
        record = await cls.db.fetch_one(query)
        if len(record) == 0:
            raise HTTPException(status_code=400, detail='Departement not found')
        return DepartementSchema(**record)

    @classmethod
    async def get_all(cls) -> List[DepartementSchema]:
        query = cls.departements.select()
        record = await cls.db.fetch_all(query)
        if len(record) == 0:
            raise HTTPException(status_code=400, detail='Departement not found')
        return [DepartementSchema(**departement) for departement in record]