from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db_sesion
from app.auth_user import UserUseCases
from app.schemas.user import UserSchema

router = APIRouter(prefix='/user')

@router.post('/register')
async def user_register(user:UserSchema,db_session:Session=Depends(get_db_sesion)):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user=user)
    return JSONResponse(
        content={'msg': 'Success'},
        status_code=status.HTTP_201_CREATED
    )

@router.post('/login')
async def user_login(request_form_user: OAuth2PasswordRequestForm=Depends(), db_session:Session=Depends(get_db_sesion)):
    uc = UserUseCases(db_session=db_session)
    user = UserSchema(username=request_form_user.username, password=request_form_user.password)
    auth_data = uc.user_login(user=user)
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_201_CREATED
    )