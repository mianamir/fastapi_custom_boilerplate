from fastapi import (
    Depends, 
    HTTPException, 
    APIRouter,
    status
    )
from sqlalchemy.orm import Session

from ..hashing import Hash

from .. import modals, sechams, database


router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=sechams.ShowUser, tags=['users'])
def create_user(request: sechams.User, db: Session = Depends(database.get_db)):

    # create the password hash before saving into the DB
    

    new_user = modals.User(
                            name=request.name, 
                            email=request.email, 
                            password=Hash.get_pass_bcrypt(request.password))

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user




@router.get('/user/{id}', response_model=sechams.ShowUser, tags=['users'])
def get_user(id, db: Session = Depends(database.get_db)):
    user = db.query(modals.User).filter(modals.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'User with ID {id} is not avaliable in the our Database.')

    return user

