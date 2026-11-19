from operator import index

from pydantic_core.core_schema import nullable_schema
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from database import  Base

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str]=mapped_column(String,nullable=False,index=True,unique=False)
    email:Mapped[str]=mapped_column(String,nullable=False,unique=False)
    password:Mapped[str]=mapped_column(String,nullable=False,unique=False)

    #one user -> many blogs
    blogs:Mapped[list["Blogs"]]=relationship(back_populates="owner",cascade="all,delete-orphan")
class Blogs(Base):
    __tablename__="blogs"
    blog_id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    content:Mapped[str]=mapped_column(String,nullable=True,index=True)
    # foreign key linking each blog to the users id
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)

    # many blogs one user
    owner:Mapped["User"]=relationship(back_populates="blogs")