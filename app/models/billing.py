from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base
from models.user import User

class Billing(Base):
    __tablename__ = 'billing'
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    money_amount = Column(Float, default=0)
    energy_amount = Column(Float, default=0)
    addres = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    zip_code = Column(String(255), nullable=False)
    discount = Column(Float)  
    user_id = Column(Integer, ForeignKey(User.id), default=1, nullable=False)
    user__ = relationship(User, foreign_keys=[user_id], uselist=False)    