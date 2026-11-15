from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, SmallInteger
from .base import Base


class StudentGroup(Base):
    __tablename__ = "student_groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(50), nullable=False)
    stud_count: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    speciality: Mapped[str] = mapped_column(String(50), nullable=False)
