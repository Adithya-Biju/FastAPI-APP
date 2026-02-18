from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from sqlalchemy import text


class User(SQLModel, table=True):

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("current_timestamp")}
    )

    posts: list["Post"] = Relationship(back_populates="owner")


class Post(SQLModel, table=True):

    __tablename__ = "posts"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(
        foreign_key="users.id",
        ondelete="CASCADE",
        nullable=False
    )

    title: str
    content: str
    published: bool = Field(default=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("current_timestamp")}
    )

    owner: User | None = Relationship(back_populates="posts")


class Votes(SQLModel, table = True):

    __tablename__ = "votes"

    user_id: int = Field(
        foreign_key="users.id",
        ondelete="CASCADE",
        nullable=False,
        primary_key=True
    )

    post_id: int = Field(
        foreign_key="posts.id",
        ondelete="CASCADE",
        nullable=False,
        primary_key= True
    )

    voted_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("current_timestamp")}
    )