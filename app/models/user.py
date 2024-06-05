

from sqlalchemy import Column, Integer, String
from app.database.base import Base


class User(Base):
    __tablename__ = "usuarios"
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    nome = Column('nome', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)