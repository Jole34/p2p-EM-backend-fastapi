from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, func, ForeignKey, JSON
from sqlalchemy.orm import relationship
from models.user import User
from db.base_class import Base

class EnergyBalance(Base):
    __tablename__ = 'energy_balance'
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    current_balance = Column(Float)
    best_balance = Column(Float)
    best_monthly_balance = Column(JSON)
    user_id = Column(Integer, ForeignKey(User.id), default=1, nullable=False)
    user__ = relationship(User, foreign_keys=[user_id], uselist=False)    
 
