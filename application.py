from typing import List
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
from blog.hashing import Hash
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


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[sechams.ShowBlog])
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
    blog = db.query(modals.Blog).\
                    filter(modals.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')
    
    blog.delete(synchronize_session=False)
                    
    db.commit()

    return {'detail': f'Blog with ID {id} has been deleted succussfully.'}


@app.put('/blog', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: sechams.BlogModal, db: Session = Depends(get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')
                                
    blog.update({modals.Blog.title: request.title,
            modals.Blog.body: request.body
            })
                     
    db.commit()
    return {'detail': f'Blog with ID {id} has been updated succussfully.'}


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=sechams.ShowBlog)
def show_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')


    return blog


# User management 

@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=sechams.ShowUser)
def create_user(request: sechams.User, db: Session = Depends(get_db)):

    # create the password hash before saving into the DB
    

    new_user = modals.User(
                            name=request.name, 
                            email=request.email, 
                            password=Hash.get_pass_bcrypt(request.password))

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user




@app.get('/user/{id}', response_model=sechams.ShowUser)
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(modals.User).filter(modals.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'User with ID {id} is not avaliable in the our Database.')

    return user















if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    