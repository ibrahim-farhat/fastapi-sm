from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import schemas, models, utils
from database import get_db


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # bug: you have to validate that the new user email does not already exist

    # hash the password
    user.password = utils.hash(user.password)

    # create the db model for the new user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    # db.refresh()

    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # compose the query that gets the user with its id, search for it, and receive the db response
    db_response = db.query(models.User).filter(models.User.id == id).first()

    # validate that the user is existing
    if not db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist.")
    
    # if the user exists, return its data
    return db_response 