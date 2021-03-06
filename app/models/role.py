
from sqlalchemy import Column, Integer, String, Boolean
from db.base_class import Base


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
