from pydantic_core.core_schema import nullable_schema
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from database import  Base

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str]=mapped_column(String,nullable=False,index=True,unique=False)
    email:Mapped[str]=mapped_column(String,nullable=False,unique=False)
    password:Mapped[str]=mapped_column(String,nullable=False,unique=False)


