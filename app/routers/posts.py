from fastapi import APIRouter, HTTPException, status, Depends
from app.models import Post, User
from ..schemas import PostCreate, ReadPost
from ..database import SessionDep
from sqlmodel import select
from typing import List
from .auth import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@router.post("/", response_model=ReadPost, status_code=status.HTTP_201_CREATED)
async def create_post(post_in: PostCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    is_existing = session.exec(select(Post).where(Post.url == post_in.url)).first()
    if is_existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post already exists")
    post = Post(**post_in.model_dump())
    print(post)
    print(post_in)
    print(current_user)
    post.owner_id = current_user.id
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/", response_model=List[ReadPost])
async def list_post(session: SessionDep, current_user: User = Depends(get_current_user)):
    posts = session.exec(select(Post).where(Post.owner_id == current_user.id).order_by(Post.created_at)).all()
    return posts

@router.get("/{post_id}", response_model=ReadPost)
async def get_post(post_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    post = session.get(Post, post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found or not yours")
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    post = session.get(Post, post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found or not yours")
    session.delete(post)
    session.commit()
    return None


