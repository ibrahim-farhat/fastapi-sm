from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models, oauth2, database

router = APIRouter(prefix="/votes", tags=["votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    # validate that the post exists
    post_response = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} does not exist.")
    
    # search for the vote instance within our data base
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_response = vote_query.first()

    # deal with the vote response
    if vote.direction == 1:
        
        # validate that the current user has not voted to the same post before
        if vote_response:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}.")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

    elif vote.direction == 0:
        
        # validate that the current user has already voted to the same post before
        if not vote_response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {current_user.id} has not voted on post {vote.post_id} before.")

        vote_query.delete(synchronize_session=False)
        db.commit()

    return {"message": "you request has been successfully performed."}
