from fastapi import (
    Depends, 
    APIRouter,
    status
    )
from sqlalchemy.orm import Session


from .. import sechams, database
from ..repository import user


router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=sechams.ShowUser)
def create(request: sechams.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)



@router.get('/{id}', response_model=sechams.ShowUser)
def show(id, db: Session = Depends(database.get_db)):
    return user.show(id, db)
