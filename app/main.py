from fastapi import FastAPI

from database import engine, get_db

import models
from routers import posts, users, auth

# validate and create the db according to the models we stablished
models.Base.metadata.create_all(bind=engine)

# initiate the fastapi application
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
