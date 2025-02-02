from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.memecoin import Memecoin, SocialMetrics
from app.schemas.memecoin import SocialMetricsCreate, SocialMetricsResponse

router = APIRouter()

@router.post("/metrics", response_model=SocialMetricsResponse)
def create_social_metrics(
    *,
    db: Session = Depends(get_db),
    metrics_in: SocialMetricsCreate
):
    """
    Create new social metrics entry for a memecoin.
    """
    # Verify memecoin exists
    memecoin = db.query(Memecoin).filter(Memecoin.id == metrics_in.memecoin_id).first()
    if not memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    
    # Create social metrics
    db_metrics = SocialMetrics(**metrics_in.dict())
    db.add(db_metrics)
    db.commit()
    db.refresh(db_metrics)
    return db_metrics

@router.get("/metrics/{memecoin_id}", response_model=List[SocialMetricsResponse])
def get_social_metrics(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int,
    platform: str = None
):
    """
    Get social metrics history for a memecoin.
    """
    query = db.query(SocialMetrics).filter(SocialMetrics.memecoin_id == memecoin_id)
    if platform:
        query = query.filter(SocialMetrics.platform == platform)
    
    metrics = query.order_by(SocialMetrics.created_at.desc()).all()
    return metrics

@router.get("/trending", response_model=List[dict])
def get_trending_social(
    *,
    db: Session = Depends(get_db),
    min_mentions: int = 100,
    min_sentiment: float = 0.6
):
    """
    Get trending memecoins based on social metrics.
    """
    # Get latest social metrics for each memecoin
    trending = db.query(
        SocialMetrics.memecoin_id,
        Memecoin.name,
        Memecoin.symbol,
        SocialMetrics.mentions_count,
        SocialMetrics.sentiment_score,
        SocialMetrics.engagement_rate
    ).join(
        Memecoin
    ).filter(
        SocialMetrics.mentions_count >= min_mentions,
        SocialMetrics.sentiment_score >= min_sentiment
    ).order_by(
        SocialMetrics.engagement_rate.desc()
    ).limit(20).all()
    
    return [
        {
            "memecoin_id": t.memecoin_id,
            "name": t.name,
            "symbol": t.symbol,
            "mentions": t.mentions_count,
            "sentiment": t.sentiment_score,
            "engagement": t.engagement_rate
        }
        for t in trending
    ]

@router.get("/influencers/{memecoin_id}")
def get_influencer_mentions(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int
):
    """
    Get influencer mentions for a specific memecoin.
    """
    metrics = db.query(SocialMetrics).filter(
        SocialMetrics.memecoin_id == memecoin_id,
        SocialMetrics.influencer_mentions.is_not(None)
    ).order_by(
        SocialMetrics.created_at.desc()
    ).first()
    
    if not metrics:
        return {"influencers": []}
    
    return {"influencers": metrics.influencer_mentions} 