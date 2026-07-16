from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comments import CommentCreate, CommentUpdate, CommentResponse
from app.utils.oauth2 import get_current_user
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(tags=["Comments"])

# PUBLIC — get all comments on a post
@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

# PROTECTED — create comment on a post
@router.post("/posts/{post_id}/comments",
             status_code=status.HTTP_201_CREATED,
             response_model=CommentResponse)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    new_comment = Comment(
        owner_id=current_user.id,
        post_id=post_id,
        **comment.model_dump()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    logger.info(f"User {current_user.id} commented on post {post_id}")
    return new_comment

# PROTECTED — update your own comment
@router.put("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    updated_comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment_query = db.query(Comment).filter(Comment.id == comment_id)
    comment = comment_query.first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found"
        )
    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment"
        )
    comment_query.update(
        updated_comment.model_dump(exclude_unset=True),
        synchronize_session=False
    )
    db.commit()
    return comment_query.first()

# PROTECTED — delete your own comment
@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment_query = db.query(Comment).filter(Comment.id == comment_id)
    comment = comment_query.first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found"
        )
    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )
    comment_query.delete(synchronize_session=False)
    db.commit()
    logger.info(f"Comment {comment_id} deleted by user {current_user.id}")




    