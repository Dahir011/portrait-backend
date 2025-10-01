from pydantic import BaseModel
from typing import Optional, List

class LoginIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class GalleryBase(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None

class GalleryOut(GalleryBase):
    id: int
    image_url: str
    class Config:
        from_attributes = True

class GalleryListOut(BaseModel):
    items: list[GalleryOut]
