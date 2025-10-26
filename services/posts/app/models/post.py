from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, ForeignKey, String, Column, DateTime
from app.db import Base,db
from app.models.user import User
from app.models.likes import likes


class ImageKey(Base):
    __tablename__ = "image_key"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="image_keys",lazy=True)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    owner: Mapped["User"] = relationship(back_populates="posts")
    image_keys: Mapped[list["ImageKey"]] = relationship(
        back_populates="post",
        lazy=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    liked_users: Mapped[list["User"]] = relationship(
        "User",
        secondary=likes,
        back_populates="liked_posts",
        lazy=True
    )


