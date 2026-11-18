from fastapi import HTTPException, Depends
from fastapi import FastAPI
from sqlalchemy import select
from authentication import get_current_user,oauth2_scheme,pwd_context,create_access_token
from database import Base,engine,db_dep
from schema import UserCreate,UserUpdate
from models import User
from fastapi.security import  OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/user")
def get_user(session:db_dep,current_user:User=Depends(get_current_user)):
    query=select(User).where(User.id==current_user.id)
    user=session.execute(query).scalar()

    session.refresh(user)


    return {"user_info":user}


@app.post("/user")
def create_user(session:db_dep,user_info:UserCreate):
    user=User(username=user_info.username,
              email=user_info.email,
              password=pwd_context.hash(user_info.password))

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"user_info":user}
@app.put("/user/{user_id}")
def update_user(user_id:int,user_info:UserUpdate,session:db_dep):
    query=select(User).where(User.id==user_id)
    user=session.execute(query).scalar()
#the update process
    user.username=user_info.username
    user.email=user_info.email
    user.password=pwd_context.hash(user_info.password)

    session.commit()
    session.refresh(user)

    return {"user_info":user}

@app.delete("/user")
def delete_user(user_id:int,session:db_dep):
    query = select(User).where(User.id==user_id)
    user=session.execute(query).scalar()

    if user is None:
        raise HTTPException(status_code=404,detail="user not found")

    session.delete(user)
    session.commit()

    return {"user deleted":"good day"}



@app.post("/login")
async def login(session:db_dep,form_data:OAuth2PasswordRequestForm=Depends()):
    query = select(User).where(User.username == form_data.username)
    user = session.execute(query).scalar_one_or_none()
    if user is None:
        raise HTTPException(404,"not found")
    verif=pwd_context.verify(form_data.password,user.password)
    if not verif:
        raise HTTPException(401,"unauthorized")
    access_token=create_access_token(data={"sub":user.username})

    return {"access_token":access_token,
            "token_type":"bearer"}







