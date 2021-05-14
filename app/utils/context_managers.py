import functools
from fastapi import HTTPException, status
from ..schemas import Response


def transaction(db):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            transaction = await db.transaction()
            try:
                result = await func(*args, **kwargs)
            except HTTPException as error:
                await transaction.rollback()
                raise error
            except Exception as error:
                await transaction.rollback()
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR, detail='INTERNAL SERVER ERROR')
            else:
                await transaction.commit()
            return result
        return wrapper
    return decorator
