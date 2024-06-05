from pydantic import BaseModel, field_validator
import re

class UserSchema(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[0-9]|@)+$', value):
            raise ValueError('Formato de username inválido')
        return value

