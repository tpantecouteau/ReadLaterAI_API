from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List, Literal
from datetime import datetime

# --------------------------
# ENUM / LITERAL
# --------------------------
Status = Literal["pending", "scraped", "done", "error"]


# --------------------------
# POSTS
# --------------------------
class PostCreate(BaseModel):
    url: str
    owner_id: Optional[int] = None  # valeur par défaut, pas obligatoire


class ReadPost(BaseModel):
    id: int
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None   
    tags: Optional[List[str]] = None
    status: Status = "pending"
    created_at: datetime
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# --------------------------
# USERS
# --------------------------
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None


class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# --------------------------
# AUTH
# --------------------------
class LoginInput(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None  # username
