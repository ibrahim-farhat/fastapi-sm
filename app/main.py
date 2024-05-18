from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine

import models
from routers import posts, users, auth, votes

from config import settings

# validate and create the db according to the models we stablished
models.Base.metadata.create_all(bind=engine)

# initiate the fastapi application
app = FastAPI()

origins = [
    "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get('/')
def main():
    return {"message": "hello world!"}
