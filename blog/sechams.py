from pydantic import BaseModel
from typing import Optional

class BlogModal(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class ShowBlog(BaseModel):
    title: str
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True
