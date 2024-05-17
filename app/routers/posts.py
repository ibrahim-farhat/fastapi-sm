from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

import schemas, models, oauth2
from database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

# get all posts
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
def list_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # get all the posts from the database, joining with votes table to count number of votes for each post
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # return all the posts to the client
    return posts

# create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # create the db model of the new post, submiting that the owner of the post is the current user within the token
    new_post = models.Post(owner_id=current_user.id, **post.dict())       # **post.dict() is equivalent to the incomming line
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # add the new post to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 

    # return the new post that was created
    return new_post

# get specific post
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # search for the post within our database, if it exists, return it
    db_response = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # validate that the post is existing
    if not db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found!")
    
    # things are going well, return the post
    return db_response

# update specific post
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # compose the query that gets the post with its id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # find that post, and return it if it exists
    db_response = post_query.first()

    # validate that the post is existing
    if not db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found!")
    
    # validate that the post owner is the same as the current user
    if db_response.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action.")

    # synch our database with the updated post
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    updated_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    # things are going well, return the post after update
    return updated_post

# delete specific post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # compose the query that gets the post with its id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # find that post, and return it if it exists
    db_response = post_query.first()

    # validate that the post is existing
    if not db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found!")
    
    # validate that the post owner is the same as the current user
    if db_response.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action.")
    
    # delete the post from the db using its query
    post_query.delete(synchronize_session=False)
    db.commit()

    # things are going well, return
    return