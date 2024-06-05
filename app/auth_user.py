from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import UserModel
from app.schemas.user import UserSchema
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config


SECRET_KEY=config('SECRET_KEY')
ALGORITHM=config('ALGORITHM')
crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserUseCases:
    def __init__(self, db_session:Session):
        self.db_session = db_session
    
    def user_register(self, user:UserSchema):
        user_model = UserModel(username=user.username, password=crypt_context.hash(user.password))
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Usuário já existe'
            )
        
    def user_login(self,user:UserSchema, expires_in:int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Nome de usuário ou senha inválidos'
            )
        
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Nome de usuário ou senha inválidos'
            )
        
        exp = datetime.utcnow() + timedelta(minutes=expires_in)
        data = {
            'sub': user.username,
            'exp': exp
        }

        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }
