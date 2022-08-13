from fastapi import (
    Depends, 
    Response, 
    HTTPException, 
    APIRouter,
    status
    )
from sqlalchemy.orm import Session
from typing import List

from .. import modals, sechams, database


router = APIRouter()

# List all blogs
@router.get('/blog', status_code=status.HTTP_200_OK, response_model=List[sechams.ShowBlog], tags=['blogs'])
def all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(modals.Blog).all()
    return blogs

# Create blog 
@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: sechams.Blog, db: Session = Depends(database.get_db)):
    blog_obj = modals.Blog(title=request.title, 
                           body=request.body, 
                           author_id=1
                           )

    db.add(blog_obj)
    db.commit()

    db.refresh(blog_obj)

    return blog_obj

# Get single blog
@router.get('/blog/{id}', status_code=status.HTTP_200_OK, tags=['blogs'])
def get_single_blog(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with ID {id} is not avaliable in the our Database.'}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')

    return blog

# Delete blog
@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(modals.Blog).\
                    filter(modals.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')
    
    blog.delete(synchronize_session=False)
                    
    db.commit()

    return {'detail': f'Blog with ID {id} has been deleted succussfully.'}

# Update blog
@router.put('/blog', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id, request: sechams.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')
                                
    blog.update({modals.Blog.title: request.title,
            modals.Blog.body: request.body
            })
                     
    db.commit()
    return {'detail': f'Blog with ID {id} has been updated succussfully.'}

# Show blog
@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=sechams.ShowBlog, tags=['blogs'])
def show_blog(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(modals.Blog).filter(modals.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'Blog with ID {id} is not avaliable in the our Database.')


    return blog
