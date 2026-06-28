from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from starlette.status import HTTP_404_NOT_FOUND
from app.database import get_db
from app.models.post import Post
from app.schemas.post import CreatePost, PostResponse , UpdatePost

router = APIRouter(prefix="/posts",
                    tags=["Posts"])

@router.get("/",response_model= List[PostResponse])
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@router.get("/{id}", response_model=PostResponse)
def get_post(id:int,db : Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post :
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"post with this {id} not found"
        )
    return post

@router.post("/", response_model=PostResponse)
def create_post(post : CreatePost, db : Session = Depends(get_db)):
    new_post = Post(owner_id=1,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=PostResponse)
def update_post(id:int,updated_post:UpdatePost,db: Session= Depends(get_db)):
    post_query = db.query(Post).filter(Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code= HTTP_404_NOT_FOUND,
            detail = f"Post with this {id} is not found"
        )
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)  # ✅
    db.commit()
    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  
def delete_post(id:int, db : Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail = f"Post with this {id} doen't exist"
        )
    post_query.delete()
    db.commit()
    




