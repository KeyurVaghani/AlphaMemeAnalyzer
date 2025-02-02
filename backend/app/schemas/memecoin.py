from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.memecoin import BlockchainType, MemeStatus

# Base Memecoin Schema
class MemecoinBase(BaseModel):
    name: str
    symbol: str
    contract_address: str
    blockchain: BlockchainType
    
    # Market Data
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    total_supply: Optional[float] = None
    holders_count: Optional[int] = None
    liquidity_usd: Optional[float] = None
    
    # Analysis Scores
    social_score: Optional[float] = None
    security_score: Optional[float] = None
    potential_score: Optional[float] = None
    
    # Social Metrics
    twitter_followers: Optional[int] = None
    telegram_members: Optional[int] = None
    social_mentions: Optional[int] = None
    social_engagement: Optional[int] = None

# Create Request Schema
class MemecoinCreate(MemecoinBase):
    pass

# Update Request Schema
class MemecoinUpdate(BaseModel):
    name: Optional[str] = None
    symbol: Optional[str] = None
    status: Optional[MemeStatus] = None
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    total_supply: Optional[float] = None
    holders_count: Optional[int] = None
    liquidity_usd: Optional[float] = None
    social_score: Optional[float] = None
    security_score: Optional[float] = None
    potential_score: Optional[float] = None
    twitter_followers: Optional[int] = None
    telegram_members: Optional[int] = None
    social_mentions: Optional[int] = None
    social_engagement: Optional[int] = None

# List Response Schema
class MemecoinList(MemecoinBase):
    id: int
    status: MemeStatus
    holder_count: Optional[int]
    liquidity_usd: Optional[float]
    market_cap_usd: Optional[float]
    potential_score: float
    created_at: datetime
    
    class Config:
        orm_mode = True

# Detailed Response Schema
class MemecoinResponse(MemecoinBase):
    id: int
    status: MemeStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Price History Schema
class PriceHistoryBase(BaseModel):
    price_usd: float
    volume_24h: float
    liquidity_change_24h: float
    holder_change_24h: int

class PriceHistoryCreate(PriceHistoryBase):
    memecoin_id: int

class PriceHistoryResponse(PriceHistoryBase):
    id: int
    memecoin_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Social Metrics Schema
class SocialMetricsBase(BaseModel):
    platform: str
    mentions_count: int
    sentiment_score: float
    engagement_rate: float
    follower_count: int
    influencer_mentions: dict

class SocialMetricsCreate(SocialMetricsBase):
    memecoin_id: int

class SocialMetricsResponse(SocialMetricsBase):
    id: int
    memecoin_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True 