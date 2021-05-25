from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import relationship
from models.user import User
from db.base_class import Base

class Trade(Base):
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_on = Column(DateTime, server_default=func.now(), index=True)
    description = Column(String(255), nullable=False)
    action = Column(String, nullable=False)
    amount = Column(Float)
    price = Column(Float)
    moment_balance = Column(Float)
    trade_id = Column(String(255), nullable=False)
    currency = Column(String(3), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), default=1, nullable=False)
    user__ = relationship(User, foreign_keys=[user_id], uselist=False)    
    blockchain_trade__ = relationship("BlockchainTrade", uselist=False)

class BlockchainTrade(Base):
    __tablename__ = 'blockchain_trade'
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    created_on = Column(DateTime, server_default=func.now(), index=True)
    transaction_id = Column(String(128), nullable=False, index=True)
    record_id = Column(String(128), nullable=False, index=True)
    trade_id = Column(Integer, ForeignKey(Trade.id), nullable=False)
    trade__ = relationship(Trade, foreign_keys=[trade_id], uselist=False)
