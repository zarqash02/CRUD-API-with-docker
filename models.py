from sqlalchemy import Boolean, Column, Integer, String, func
from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    title = Column(String)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())