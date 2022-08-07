from turtle import title
import uvicorn
from fastapi import Depends, FastAPI
from typing import Optional
from sqlalchemy.orm import Session

from blog import modals
from blog.database import SessionLocal, engine

from blog import sechams

app = FastAPI()


# create database modals 
modals.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@app.post('/blog')
def create_blog(request: sechams.BlogModal, db: Session = Depends(get_db)):
    blog_obj = modals.Blog(title=request.title, body=request.body)

    db.add(blog_obj)
    db.commit()

    db.refresh(blog_obj)

    return blog_obj


@app.get('/blog')
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(modals.Blog).all()
    return blogs

@app.get('/blog/{id}')
def get_single_blog(id, db: Session = Depends(get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id == id).first()
    return blog


    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    