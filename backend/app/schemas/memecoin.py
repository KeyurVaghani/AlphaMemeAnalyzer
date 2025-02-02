from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.memecoin import BlockchainType, MemeStatus

# Base Memecoin Schema
class MemecoinBase(BaseModel):
    name: str = Field(..., description="Name of the memecoin")
    symbol: str = Field(..., description="Token symbol")
    contract_address: str = Field(..., description="Contract address on the blockchain")
    blockchain: BlockchainType = Field(..., description="Blockchain platform")

# Create Request Schema
class MemecoinCreate(MemecoinBase):
    pass

# Update Request Schema
class MemecoinUpdate(BaseModel):
    name: Optional[str] = None
    symbol: Optional[str] = None
    total_supply: Optional[float] = None
    circulating_supply: Optional[float] = None
    holder_count: Optional[int] = None
    liquidity_usd: Optional[float] = None
    market_cap_usd: Optional[float] = None
    contract_verified: Optional[bool] = None
    status: Optional[MemeStatus] = None
    social_score: Optional[float] = None
    risk_score: Optional[float] = None
    potential_score: Optional[float] = None

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
    total_supply: Optional[float]
    circulating_supply: Optional[float]
    holder_count: Optional[int]
    liquidity_usd: Optional[float]
    market_cap_usd: Optional[float]
    contract_verified: bool
    creator_address: Optional[str]
    creation_tx_hash: Optional[str]
    contract_audit: Optional[dict]
    social_score: float
    risk_score: float
    potential_score: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

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