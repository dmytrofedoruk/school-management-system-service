from jose import JWTError, jwt
from fastapi import Header, HTTPException, status

from .models import UserModel
from .config import Envs

async def get_user(token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Envs.SECRET_KEY, algorithms=Envs.ALGORITHM)
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        user_found = await UserModel.get_user(email)
        yield user_found
    except JWTError:
        raise credentials_exception
