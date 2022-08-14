from fastapi import (
            APIRouter, 
            Depends, 
            HTTPException, 
            status
            )

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .. import database, modals, token
from ..hashing import Hash


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(modals.User).filter(modals.User.email == request.username).first()

    if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail = f'These are invalid credentials.')    
    
    # verify password
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail = f'Username or password is not correct.')

    # generate JWT token

    access_token = token.create_access_token(data={"sub": user.email}) 
    return {"access_token": access_token, "token_type": "bearer"} 