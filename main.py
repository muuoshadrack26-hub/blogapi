from fastapi import HTTPException, Depends
from fastapi import FastAPI
from sqlalchemy import select
from authentication import get_current_user,pwd_context,create_access_token
from database import Base,engine,db_dep
from schema import UserCreate,UserUpdate,CreateBlog,UpdateBlog
from models import User,Blogs
from fastapi.security import  OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/user")
def get_user(session:db_dep,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='unauthorised')
    query=select(User).where(User.id==current_user.id)
    user=session.execute(query).scalar()

    if user is None:
        raise HTTPException(status_code=404,detail="user not found")

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
@app.put("/user")
def update_user(user_info:UserUpdate,session:db_dep,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401,detail='unauthorised')
    query=select(User).where(User.id==current_user.id)
    user=session.execute(query).scalar()
#the update process
    user.username=user_info.username
    user.email=user_info.email
    user.password=pwd_context.hash(user_info.password)

    session.commit()
    session.refresh(user)

    return {"user_info":user}

@app.delete("/user")
def delete_user(session:db_dep,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='unauthorised')
    query = select(User).where(User.id==current_user.id)
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



# ----------------------------------blog methods----------------
@app.post("/blog")
def create_blog(session:db_dep,blog_info:CreateBlog,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='unauthorised')
    blog=Blogs(content=blog_info.content,user_id=current_user.id)

    if blog is None:
        raise HTTPException(status_code=404,detail="here")
    session.add(blog)
    session.commit()
    session.refresh(blog)


    return {"blog_info":blog}

@app.get("/blogs")
def get_blog(session:db_dep,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='unauthorised')

    query=select(Blogs).where(Blogs.user_id==current_user.id)
    blogs=session.execute(query).scalars().all()

    if blogs is None:
        raise  HTTPException(status_code=404,detail="blogs not found")


    return {"blogs":blogs}

@app.get("/blogs/{blog_id}")
def get_blog_by_id(session:db_dep,blog_id:int,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='unauthorised')
    query=select(Blogs).where(Blogs.blog_id==blog_id)
    blog=session.execute(query).scalar()
    if blog is None:
        raise HTTPException(status_code=404,detail="blog not found")


    return{"blog":blog}

@app.put("/blog/{blog_id}")
def update_blog(session:db_dep,blog_info:UpdateBlog,blog_id:int,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='unauthorised')
    query = select(Blogs).where(Blogs.blog_id == blog_id)
    blog = session.execute(query).scalar()
    blog.content=blog_info.content
    if blog is None:
        raise HTTPException(status_code=404,detail="blog not found")

    session.add(blog)
    session.commit()
    session.refresh(blog)

    return  {"updated_blog":blog}



@app.delete("/blog/{blog_id}")
def delete_blog(session:db_dep,blog_id:int,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='unauthorised')
    query=select(Blogs).where(Blogs.blog_id==blog_id)
    blog=session.execute(query).scalar()

    if blog is None:
        raise HTTPException(status_code=404,detail="blog not found")

     if Blogs.blog_id != current_user.id:
        raise HTTPException(status_code=403,detail="unauthorised")

    session.delete(blog)
    session.commit()


    return {"blog deleted successfully":"thankyou"}





