from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
