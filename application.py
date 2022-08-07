import re
from turtle import title
import uvicorn
from fastapi import (
    Depends, 
    FastAPI, 
    Response, 
    HTTPException,
    status
    )
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


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: sechams.BlogModal, db: Session = Depends(get_db)):
    blog_obj = modals.Blog(title=request.title, body=request.body)

    db.add(blog_obj)
    db.commit()

    db.refresh(blog_obj)

    return blog_obj


@app.get('/blog', status_code=status.HTTP_200_OK)
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(modals.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def get_single_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with ID {id} is not avaliable in the our Database.'}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')

    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    db.query(modals.Blog).\
                    filter(modals.Blog.id == id).\
                    delete(synchronize_session=False)
    db.commit()

    return {'detail': f'Blog with ID {id} has been deleted succussfully.'}


    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    