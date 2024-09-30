from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str
    telegram_id: Optional[int] = Field(unique=True)
    username: Optional[str]
    role: str = Field(nullable=False, foreign_key="role.role_names")
    signup_at: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    urls: List["Url"] = Relationship(back_populates="user")
    posts: List["Post"] = Relationship(back_populates="user")
    token: Optional["Token"] = Relationship(back_populates="user")

class Url(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    url: str
    user_id: int = Field(foreign_key="user.id")

    # Relationships
    post: Optional["Post"] = Relationship(back_populates="url")
    user: User = Relationship(back_populates="urls")

class Post(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    url_id: int = Field(foreign_key="url.id")
    post_order: int = Field(default=1, description="Order of the post for custom sorting")
    platform: str = Field(foreign_key="platform.platform_names")
    title: Optional[str] = None
    body: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tags: List["Tag"] = Relationship(back_populates="post")
    url: Url = Relationship(back_populates="post")
    user: User = Relationship(back_populates="posts")

class Token(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    key: str # TODO: store the hash
    user_id: int = Field(unique=True, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="token")

class Tag(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    post_id: int = Field(foreign_key="post.id")
    tag_name: str = Field(foreign_key="segmentation.tag_names")

    post: Post = Relationship(back_populates="tags")

class Segmentation(SQLModel, table=True):
    tag_names: str = Field(primary_key=True)

class Platform(SQLModel, table=True):
    platform_names: str = Field(primary_key=True)

class Role(SQLModel, table=True):
    role_names: str = Field(primary_key=True)