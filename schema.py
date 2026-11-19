from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username:str
    email:str
    password:str
class UserUpdate(BaseModel):
    username:str
    email:str
    password:str


class CreateBlog(BaseModel):
 content:str


class UpdateBlog(BaseModel):
    content:str

