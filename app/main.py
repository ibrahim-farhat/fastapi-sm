from fastapi import FastAPI, Response, status, HTTPException, Depends

from fastapi.params import Body # to get the body of the post request

from typing import Optional, List     # for Optional class

from sqlalchemy.orm import Session

from database import engine, get_db

import models, schemas

# validate and create the db according to the models we stablished
models.Base.metadata.create_all(bind=engine)

# initiate the fastapi application
app = FastAPI()

# get all posts
@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def list_posts(db: Session = Depends(get_db)):
    
    # get all the posts from the database
    posts = db.query(models.Post).all()

    # return all the posts to the client
    return posts

# create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

    # create the db model of the new post
    new_post = models.Post(**post.dict())       # **post.dict() is equivalent to the incomming line
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # add the new post to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 

    # return the new post that was created
    return new_post

# get specific post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    
    # search for the post within our database, if it exists, return it
    db_response = db.query(models.Post).filter(models.Post.id == id).first()
    
    # validate that the post is existing
    if not db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found!")
    
    # things are going well, return the post
    return db_response

# update specific post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    # compose the query that gets the post with its id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # validate that the post is existing
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found!")
    
    # synch our database with the updated post
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    updated_post = post_query.first()
    
    # things are going well, return the post after update
    return updated_post

# delete specific post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # compose the query that gets the post with its id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # validate that the post is existing
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found!")
    
    # delete the post from the db using its query
    post_query.delete(synchronize_session=False)
    db.commit()

    # things are going well, return
    return