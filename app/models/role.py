
from sqlalchemy import Column, Integer, String

from app import db
Base = db.base_class

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
