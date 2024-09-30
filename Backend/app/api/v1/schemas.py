from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class UserCreate(BaseModel):
    name: str
    telegram_id: int
    username: str

class UrlTelegramCreate(BaseModel):
    url: HttpUrl
    telegram_id: int

class UrlRead(BaseModel):
    id: int
    url: str
    user_id: int
    post_id: Optional[int]

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    post_order: int
    platform: str
    title: Optional[str]
    body: Optional[str]
    user_id: int

class PostRead(BaseModel):
    id: int
    post_order: int
    platform: str
    title: Optional[str]
    body: Optional[str]
    user_id: int
    created_at: datetime

class TokenCreate(BaseModel):
    user_id: int

class TokenRead(BaseModel):
    key: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class TagCreate(BaseModel):
    post_id: str
    tag_name: str

class TagRead(BaseModel):
    post_id: str
    tag_name: str

    class Config:
        orm_mode = True

class SegmentationCreate(BaseModel):
    tag_names: str

class SegmentationRead(BaseModel):
    tag_names: str

    class Config:
        orm_mode = True

class PlatformCreate(BaseModel):
    platform_names: str

class PlatformRead(BaseModel):
    platform_names: str

    class Config:
        orm_mode = True