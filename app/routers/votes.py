from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import post
from app.models.post import Post
from app.schemas.vote import CreateVote
from app.models.vote import Vote
from app.models.user import User
from app.utils.oauth2 import get_current_user


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: CreateVote, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")
    
    existing_vote = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id).first()

    if vote.direction == 1: 
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    
    if vote.direction == 0:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist")
        db.delete(existing_vote)
        db.commit()
        return {"message": "Vote removed succesfully"}
    
    

        
    
    