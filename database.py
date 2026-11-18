import  sqlalchemy
from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session
from typing import Annotated

Base=declarative_base()

database_url="postgresql://postgres:amani55@localhost:5432/blogapi"
engine=create_engine(database_url)

session_local=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()


db_dep=Annotated[session,Depends(get_db)]
