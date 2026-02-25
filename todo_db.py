from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)
from datetime import datetime, timezone
from db import Base


class Todo(Base):
    __tablename__ = "todo_list"

    id : int = Column(Integer, primary_key=True)
    user_id : int = Column(Integer, nullable=False)
    work : str = Column(String, nullable=False)
    is_completed : bool= Column(Boolean, default=False)
    date : datetime = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )


class Register(Base):
    __tablename__ = "register"

    id : int= Column(Integer, primary_key=True, autoincrement=True)
    user_name : str = Column(String, nullable=False, unique=True)
    hash_password : str = Column(String, nullable=False)