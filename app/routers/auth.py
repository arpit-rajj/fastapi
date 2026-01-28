from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schema
from ..databases import get_db
from sqlalchemy.orm import Session
import app.utils as utils
import app.oauth2 as oauth2
router = APIRouter(   
    tags=["Auth"]
)

@router.post("/login",response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if(not utils.verify_password(user_credentials.password, db_user.password)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    #create a token and return it
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}