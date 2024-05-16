from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "fosaifanmdfoijoi083204u0293jr8t92j958u230jen98sdgh9w03492-"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=str(id))

    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # verify the token received
    token = verify_access_token(token, credentials_exception)

    # get the user from the db with its id
    user = db.query(models.User).filter(models.User.id == token.id).first()

    # return the user data
    return user