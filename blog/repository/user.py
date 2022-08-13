from fastapi import (
    HTTPException, 
    status
    )
from sqlalchemy.orm import Session


from ..hashing import Hash
from .. import modals, sechams


def create(request: sechams.User, db: Session):
    # create the password hash before saving into the DB

    obj = modals.User(
                            name=request.name, 
                            email=request.email, 
                            password=Hash.get_pass_bcrypt(request.password))

    db.add(obj)
    db.commit()

    db.refresh(obj)

    return obj


def show(id: int, db: Session):
    obj = db.query(modals.User).filter(modals.User.id == id).first()

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'User with ID {id} is not avaliable in the our Database.')

    return obj