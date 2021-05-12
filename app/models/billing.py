from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base
from models.balance import Balance
from models.user import User

class Billing(Base):
    __tablename__ = 'billing'
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    addres = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    zip_code = Column(String(255), nullable=False)
    discount = Column(Float)
    balance_id = Column(Integer, ForeignKey(Balance.id), default=1, nullable=False)
    balance__ = relationship(Balance, foreign_keys=[balance_id], uselist=False)    
    user_id = Column(Integer, ForeignKey(User.id), default=1, nullable=False)
    user__ = relationship(User, foreign_keys=[user_id], uselist=False)    