
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
class UserCreate(BaseModel):
    email:EmailStr
    password: str
    class Config:

        orm_mode = True
class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:

        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserOut

    class Config:

        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int


    class Config:

        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] =None

    
class vote(BaseModel):
    post_id :int
    dir: conint (le=1) #This will open negative number too . find a way to restrict only 0 or 1




