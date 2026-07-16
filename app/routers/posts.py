from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.post import Post
from app.models.user import User
from app.models.vote import Vote
from app.utils.oauth2 import get_current_user
from app.schemas.post import CreatePost, UpdatePost, PostOut
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# PUBLIC
@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db),
    limit: int = Query(default=10, le=50),
    skip: int = Query(default=0, ge=0),
    search: str = Query(default="")):
    posts = db.query(Post, func.count(Vote.post_id).label("votes"))\
              .join(Vote, Vote.post_id == Post.id, isouter=True)\
              .filter(Post.title.ilike(f"%{search}%"))\
              .group_by(Post.id)\
              .limit(limit)\
              .offset(skip)\
              .all()
    return posts

# PUBLIC
@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post, func.count(Vote.post_id).label("votes"))\
             .join(Vote, Vote.post_id == Post.id, isouter=True)\
             .filter(Post.id == id)\
             .group_by(Post.id)\
             .first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    return post

# PROTECTED
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(
    post: CreatePost,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} creating post")
    new_post = Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    result = db.query(Post, func.count(Vote.post_id).label("votes"))\
               .join(Vote, Vote.post_id == Post.id, isouter=True)\
               .filter(Post.id == new_post.id)\
               .group_by(Post.id)\
               .first()
    logger.info(f"Post {new_post.id} created by user {current_user.id}")
    return result

# PROTECTED
@router.put("/{id}", response_model=PostOut)
def update_post(
    id: int,
    updated_post: UpdatePost,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    result = db.query(Post, func.count(Vote.post_id).label("votes"))\
               .join(Vote, Vote.post_id == Post.id, isouter=True)\
               .filter(Post.id == id)\
               .group_by(Post.id)\
               .first()
    return result

# PROTECTED
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        logger.warning(f"User {current_user.id} tried to delete non-existent post {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        logger.warning(f"User {current_user.id} unauthorized delete attempt on post {id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    logger.info(f"Post {id} deleted by user {current_user.id}")
    return {f"Post {id} is deleted successfully"}

