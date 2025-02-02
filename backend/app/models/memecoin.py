from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class BlockchainType(str, enum.Enum):
    ETHEREUM = "ethereum"
    BSC = "bsc"
    SOLANA = "solana"

class MemeStatus(str, enum.Enum):
    NEW = "new"
    ANALYZING = "analyzing"
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
    
    # Market Data
    current_price = Column(Float)
    market_cap = Column(Float)
    total_supply = Column(Float)
    holders_count = Column(Integer)
    liquidity_usd = Column(Float)
    
    # Analysis Scores
    social_score = Column(Float)
    security_score = Column(Float)
    potential_score = Column(Float)
    
    # Social Metrics
    twitter_followers = Column(Integer)
    telegram_members = Column(Integer)
    social_mentions = Column(Integer)
    social_engagement = Column(Integer)
    
    # Additional Data
    coin_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

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