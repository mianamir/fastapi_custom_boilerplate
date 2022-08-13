from fastapi import (
    HTTPException, 
    status
    )
from sqlalchemy.orm import Session

from .. import modals, sechams


def get_all(db: Session):
    blogs = db.query(modals.Blog).all()
    return blogs


def create(request: sechams.Blog, db: Session):
    obj = modals.Blog(title=request.title, 
                           body=request.body, 
                           author_id=1
                           )
    db.add(obj)
    db.commit()

    db.refresh(obj)

    return obj


def destory(id: int, db: Session):
    blog = db.query(modals.Blog).\
                    filter(modals.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')
    
    blog.delete(synchronize_session=False)
                    
    db.commit()

    return True


def update(id: int, request: sechams.Blog, db: Session):
    obj = db.query(modals.Blog).filter(modals.Blog.id == id)

    if not obj.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')
                                
    obj.update({modals.Blog.title: request.title,
            modals.Blog.body: request.body
            })
                     
    db.commit()

    return True

def show(id: int, db: Session):
    obj = db.query(modals.Blog).filter(modals.Blog.id == id).first()

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')
    return obj
