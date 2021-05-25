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
    role_id_1 = Column(Integer, ForeignKey(Role.id), default=1, nullable=True)
    role__1 = relationship(Role, foreign_keys=[role_id_1], uselist=False)
    role_id_2 = Column(Integer, ForeignKey(Role.id), default=1, nullable=True)
    role__2 = relationship(Role, foreign_keys=[role_id_2], uselist=False)
    role_id_3 = Column(Integer, ForeignKey(Role.id), default=1, nullable=True)
    role__3 = relationship(Role, foreign_keys=[role_id_3], uselist=False)