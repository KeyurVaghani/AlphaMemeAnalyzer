from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class ChainAnalysis(Base):
    __tablename__ = "chain_analysis"

    id = Column(Integer, primary_key=True, index=True)
    memecoin_id = Column(Integer, ForeignKey("memecoins.id", ondelete="CASCADE"))
    
    # Liquidity Analysis
    liquidity_usd = Column(Float)
    liquidity_change_24h = Column(Float)
    liquidity_locked_ratio = Column(Float)  # 0 to 1
    lock_duration_days = Column(Integer)
    
    # Holder Analysis
    total_holders = Column(Integer)
    holder_change_24h = Column(Integer)
    top_10_holders_ratio = Column(Float)  # 0 to 1
    whale_wallets = Column(JSON)  # Store whale wallet data
    
    # Smart Money Tracking
    smart_money_inflow = Column(Float)
    smart_money_wallets = Column(JSON)  # Store smart money wallet data
    smart_money_confidence = Column(Float)  # 0 to 1
    
    # Contract Analysis
    contract_verified = Column(Boolean, default=False)
    mint_disabled = Column(Boolean, default=False)
    ownership_renounced = Column(Boolean, default=False)
    security_score = Column(Float)  # 0 to 1
    risk_factors = Column(JSON)  # Store identified risk factors
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    memecoin = relationship("Memecoin", back_populates="chain_analysis")

    class Config:
        orm_mode = True 