from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, SmallInteger
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_password: Mapped[str] = mapped_column(String(100), nullable=False)
