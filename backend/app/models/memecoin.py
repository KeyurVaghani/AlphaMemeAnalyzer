from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum
from .base import Base

class BlockchainType(enum.Enum):
    ETHEREUM = "ethereum"
    BSC = "binance-smart-chain"
    SOLANA = "solana"

class MemeStatus(enum.Enum):
    NEW = "new"
    ANALYZING = "analyzing"
    POTENTIAL = "potential"
    VERIFIED = "verified"
    REJECTED = "rejected"

class Memecoin(Base):
    __tablename__ = "memecoins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    symbol = Column(String, index=True)
    contract_address = Column(String, unique=True, index=True)
    blockchain = Column(Enum(BlockchainType))
    status = Column(Enum(MemeStatus), default=MemeStatus.NEW)
    
    # Token Info
    total_supply = Column(Float)
    circulating_supply = Column(Float)
    holder_count = Column(Integer)
    liquidity_usd = Column(Float)
    market_cap_usd = Column(Float)
    
    # Contract Info
    contract_verified = Column(Boolean, default=False)
    creator_address = Column(String)
    creation_tx_hash = Column(String)
    contract_audit = Column(JSON)  # Store audit results
    
    # Analysis Data
    social_score = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    potential_score = Column(Float, default=0.0)
    
    # Relationships
    price_history = relationship("PriceHistory", back_populates="memecoin")
    social_metrics = relationship("SocialMetrics", back_populates="memecoin")
    alerts = relationship("Alert", back_populates="memecoin")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    memecoin_id = Column(Integer, ForeignKey("memecoins.id"))
    
    price_usd = Column(Float)
    volume_24h = Column(Float)
    liquidity_change_24h = Column(Float)
    holder_change_24h = Column(Integer)
    
    memecoin = relationship("Memecoin", back_populates="price_history")

class SocialMetrics(Base):
    __tablename__ = "social_metrics"

    id = Column(Integer, primary_key=True, index=True)
    memecoin_id = Column(Integer, ForeignKey("memecoins.id"))
    
    platform = Column(String)  # twitter, telegram, reddit
    mentions_count = Column(Integer)
    sentiment_score = Column(Float)
    engagement_rate = Column(Float)
    follower_count = Column(Integer)
    influencer_mentions = Column(JSON)  # Store influencer data
    
    memecoin = relationship("Memecoin", back_populates="social_metrics")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    memecoin_id = Column(Integer, ForeignKey("memecoins.id"))
    
    alert_type = Column(String)  # price_spike, volume_spike, social_spike
    alert_data = Column(JSON)
    is_active = Column(Boolean, default=True)
    
    memecoin = relationship("Memecoin", back_populates="alerts") 