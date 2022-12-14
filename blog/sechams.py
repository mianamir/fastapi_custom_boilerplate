from blog.modals import Blog
from pydantic import BaseModel
from typing import Optional, List, Union



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class User(BaseModel):
    name: str
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str
    published: Optional[bool]

class Blog(BlogBase):
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    name: str
    email: str

    blogs: List[Blog] = []
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    author: ShowUser
    class Config():
        orm_mode = True


class Login(BaseModel):
    username:str
    password:str

    