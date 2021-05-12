from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import relationship
from models.user import User
from db.base_class import Base

class Balance(Base):
    __tablename__ = 'balance'
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    ammount = Column(Float)
    user_id = Column(Integer, ForeignKey(User.id), default=1, nullable=False)
    user__ = relationship(User, foreign_keys=[user_id], uselist=False)    
