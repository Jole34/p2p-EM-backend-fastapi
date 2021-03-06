from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import relationship
from models.role import Role
from db.base_class import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    status = Column(String(100), nullable=False, default='Active')
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)
    role__ = relationship(Role, foreign_keys=[role_id], uselist=False)