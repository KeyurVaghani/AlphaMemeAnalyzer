from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, AnyHttpUrl, ConfigDict
from datetime import datetime
from app.models.memecoin import BlockchainType, MemeStatus
import re

# Base Memecoin Schema
class MemecoinBase(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Name of the memecoin"
    )
    symbol: str = Field(
        ..., 
        min_length=1, 
        max_length=20,
        description="Trading symbol of the memecoin"
    )
    contract_address: str = Field(
        ..., 
        min_length=42, 
        max_length=44,
        pattern="^(0x)?[0-9a-fA-F]{40}$",
        description="Smart contract address of the memecoin (42-44 characters, must be valid hex for Ethereum/BSC)"
    )
    blockchain: BlockchainType = Field(
        ...,
        description="Blockchain network where the memecoin is deployed"
    )
    
    # Market Data
    current_price: Optional[float] = Field(None, ge=0)
    market_cap: Optional[float] = Field(None, ge=0)
    total_supply: Optional[float] = Field(None, ge=0)
    holders_count: Optional[int] = Field(None, ge=0)
    liquidity_usd: Optional[float] = Field(None, ge=0)
    
    # Analysis Scores
    social_score: Optional[float] = Field(None, ge=0, le=1)
    security_score: Optional[float] = Field(None, ge=0, le=1)
    potential_score: Optional[float] = Field(None, ge=0, le=1)
    
    # Social Metrics
    twitter_followers: Optional[int] = Field(None, ge=0)
    telegram_members: Optional[int] = Field(None, ge=0)
    social_mentions: Optional[int] = Field(None, ge=0)
    social_engagement: Optional[int] = Field(None, ge=0)

    @field_validator('contract_address')
    def validate_contract_address(cls, v: str, values: Dict) -> str:
        # Remove '0x' prefix if present for length validation
        clean_address = v[2:] if v.startswith('0x') else v
        
        # Check length of clean address
        if len(clean_address) != 40:
            raise ValueError('Contract address must be 40 characters long (excluding 0x prefix)')
        
        # Validate hex format
        if not re.match('^[0-9a-fA-F]{40}$', clean_address):
            raise ValueError('Contract address must contain only valid hexadecimal characters')
        
        # Blockchain-specific validation
        blockchain = values.get('blockchain')
        if blockchain in [BlockchainType.ETHEREUM, BlockchainType.BSC]:
            if not v.startswith('0x'):
                raise ValueError(f'{blockchain.value} contract address must start with 0x')
        
        # Add 0x prefix if missing for ETH/BSC
        if blockchain in [BlockchainType.ETHEREUM, BlockchainType.BSC] and not v.startswith('0x'):
            v = f'0x{v}'
        
        return v

    @field_validator('symbol')
    def validate_symbol(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Symbol must contain only alphanumeric characters')
        return v.upper()

# Create Request Schema
class MemecoinCreate(MemecoinBase):
    pass

# Update Request Schema
class MemecoinUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    symbol: Optional[str] = Field(None, min_length=1, max_length=20)
    status: Optional[MemeStatus] = None
    current_price: Optional[float] = Field(None, ge=0)
    market_cap: Optional[float] = Field(None, ge=0)
    total_supply: Optional[float] = Field(None, ge=0)
    holders_count: Optional[int] = Field(None, ge=0)
    liquidity_usd: Optional[float] = Field(None, ge=0)
    social_score: Optional[float] = Field(None, ge=0, le=1)
    security_score: Optional[float] = Field(None, ge=0, le=1)
    potential_score: Optional[float] = Field(None, ge=0, le=1)
    twitter_followers: Optional[int] = Field(None, ge=0)
    telegram_members: Optional[int] = Field(None, ge=0)
    social_mentions: Optional[int] = Field(None, ge=0)
    social_engagement: Optional[int] = Field(None, ge=0)

# List Response Schema
class MemecoinList(MemecoinBase):
    id: int = Field(..., gt=0)
    status: MemeStatus
    holder_count: Optional[int] = Field(None, ge=0)
    liquidity_usd: float = Field(..., ge=0)
    market_cap_usd: Optional[float] = Field(None, ge=0)
    potential_score: float = Field(..., ge=0, le=1)
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Detailed Response Schema
class MemecoinResponse(MemecoinBase):
    id: int = Field(..., gt=0)
    status: MemeStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Price History Schema
class PriceHistoryBase(BaseModel):
    price_usd: float = Field(..., ge=0)
    volume_24h: float = Field(..., ge=0)
    liquidity_change_24h: float
    holder_change_24h: int

class PriceHistoryCreate(PriceHistoryBase):
    memecoin_id: int = Field(..., gt=0)

class PriceHistoryResponse(PriceHistoryBase):
    id: int = Field(..., gt=0)
    memecoin_id: int = Field(..., gt=0)
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Social Metrics Schema
class SocialMetricsBase(BaseModel):
    platform: str = Field(..., pattern='^(twitter|telegram|reddit)$')
    mentions_count: int = Field(..., ge=0)
    sentiment_score: float = Field(..., ge=-1, le=1)
    engagement_rate: float = Field(..., ge=0, le=1)
    follower_count: int = Field(..., ge=0)
    influencer_mentions: Dict[str, Any]

class SocialMetricsCreate(SocialMetricsBase):
    memecoin_id: int = Field(..., gt=0)

class SocialMetricsResponse(SocialMetricsBase):
    id: int = Field(..., gt=0)
    memecoin_id: int = Field(..., gt=0)
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True) 