from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from config import db_dependency, SECRET_KEY, ALGORITHM
from schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
import crud

router = APIRouter()


@router.post("/", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = crud.authenticate_user(form_data.username,
                                  form_data.password,
                                  db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = crud.create_access_token(user.email, user.user_uuid, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: Annotated[str, Depends(crud.oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        user_uuid: int = payload.get('id')
        if email is None or user_uuid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"email": email, "id": user_uuid}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


user_dependency = Annotated[dict, Depends(get_current_user)]
