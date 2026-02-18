from sqlmodel import SQLModel
from pydantic import EmailStr, BaseModel
from datetime import datetime
from typing import Literal

class UserCreate(SQLModel):
    email : EmailStr 
    password : str 

class UserOut(SQLModel):
    id : int
    email : str

    model_config = {
        "from_attributes": True
    }


class PostCreate(SQLModel):
    title: str
    content: str
    published: bool = True

class PostView(PostCreate):
    id : int
    owner : UserOut
    created_at : datetime

    model_config = {
        "from_attributes": True
    }

class PostOut(SQLModel):
    Post: PostView
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: int | None = None


class Vote(SQLModel):
    post_id: int
    direction: Literal[0,1]