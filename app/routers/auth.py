from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import schemas, models, utils, oauth2
from database import get_db


router = APIRouter(tags=["Authenticatoin"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # search for the email within the db, and if it exists, return its data
    db_response = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # validate that the email exists
    if not db_response:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")
    
    # verify that the encrypted password is the same as the inputed password
    if not utils.verify(user_credentials.password, db_response.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")

    # create the access token to be returned to the user
    access_token = oauth2.create_access_token(data = {"user_id": db_response.id})
    
    # return the token
    return {"access_token": access_token, "token_type": "bearer"}