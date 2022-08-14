from fastapi import (
    Depends, 
    Response,  
    APIRouter,
    status
    )
from sqlalchemy.orm import Session
from typing import List

from .. import sechams, database, oauth2
from ..repository import blog


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
    )

# List all blogs
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[sechams.ShowBlog])
def all(db: Session = Depends(database.get_db), current_user: sechams.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

# Create blog 
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: sechams.Blog, db: Session = Depends(database.get_db), current_user: sechams.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db)

# Delete blog
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id, response: Response, db: Session = Depends(database.get_db), current_user: sechams.User = Depends(oauth2.get_current_user)):
    if blog.destory(id, db):
        return {'detail': f'Blog with ID {id} has been deleted succussfully.'}

    return {'detail': f'Error: Blog with ID {id} has not deleted'}    

# Update blog
@router.put('/', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: sechams.Blog, db: Session = Depends(database.get_db), current_user: sechams.User = Depends(oauth2.get_current_user)):
    if blog.update(id, request, db):
        return {'detail': f'Blog with ID {id} has been updated succussfully.'}

    return {'detail': f'Blog with ID {id} has not updated.'}

# Show blog
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=sechams.ShowBlog)
def show(id, db: Session = Depends(database.get_db), current_user: sechams.User = Depends(oauth2.get_current_user)):
    return blog.show(id, db)
