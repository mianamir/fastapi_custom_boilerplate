from pydantic import BaseModel
from typing import Optional

class BlogModal(BaseModel):
    title: str
    body: str
    published: Optional[bool]