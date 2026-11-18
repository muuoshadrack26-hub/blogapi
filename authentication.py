from fastapi import Depends, HTTPException
from pwdlib import PasswordHash
from jose import jwt,JWTError
from passlib.ifc import PasswordHash
from datetime import datetime, timezone, timedelta
from models import User
from sqlalchemy import select
import secrets
from database import db_dep
from fastapi.security import OAuth2PasswordRequestForm
#security code instead of a separate file
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
pwd_context = PasswordHash.recommended()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
#end



SECRET_KEY="6293d468e1b9fe7ba1b49dd1788e9dc42c18352ea7f51884f909131d567cb703"
ALGORITHM="HS256"

def create_access_token(data:dict):
    token=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(hours=5)
    encoded_jwt=jwt.encode(token,SECRET_KEY,algorithm=ALGORITHM)
    token.update({"exp":expire})

    return encoded_jwt


def get_current_user(session:db_dep,token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
    except JWTError:
        raise HTTPException (status_code=404,detail="user not found")

    query=select(User).where(User.username==username)
    user=session.execute(query).scalar()

    if user is None:
        raise HTTPException(status_code=404,detail="user not found")

    return  user

