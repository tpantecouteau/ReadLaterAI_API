
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import select

from app.database import SessionDep
from app.models import Post, User
from app.routers.auth import get_current_user
from app.schemas import ReadPost, UserRead


router = APIRouter(prefix='/users', tags=['users'])

@router.get('/me', response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get('/me/posts', response_model=List[ReadPost])
async def get_my_posts(session: SessionDep, current_user: User = Depends(get_current_user)):
    posts = session.exec(select(Post).where(Post.owner_id == current_user.id).order_by(Post.created_at)).all()
    return posts
