from sqlalchemy.orm import Mapped, mapped_column , relationship
from app.db import Base
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.likes import likes


class User(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()


    posts: Mapped[list["Post"]] = relationship(back_populates="owner")

        
    liked_posts: Mapped[list["Post"]] = relationship(
        "Post",
        secondary=likes,
        back_populates="liked_users",
        lazy="subquery"
    )
