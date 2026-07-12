from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.post import Post
from app.models.user import User
from app.models.vote import Vote
from app.utils.oauth2 import get_current_user
from app.schemas.post import CreatePost, UpdatePost, PostOut

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# PUBLIC
@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post, func.count(Vote.post_id).label("votes"))\
              .join(Vote, Vote.post_id == Post.id, isouter=True)\
              .group_by(Post.id)\
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
    new_post = Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    result = db.query(Post, func.count(Vote.post_id).label("votes"))\
               .join(Vote, Vote.post_id == Post.id, isouter=True)\
               .filter(Post.id == new_post.id)\
               .group_by(Post.id)\
               .first()
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    


    