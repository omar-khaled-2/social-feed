from sqlalchemy import Table, ForeignKey, String, Column, DateTime
from app.db import Base,db
likes = Table(
    "likes",
    Base.metadata,
    Column("user_id", ForeignKey("posts.id")),
    Column("post_id", ForeignKey("users.id")),
)
