from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.memecoin import Memecoin, MemeStatus
from app.services.analysis import (
    analyze_contract,
    calculate_social_score,
    calculate_risk_score,
    calculate_potential_score,
    analyze_memecoin,
    get_top_potential_coins
)

router = APIRouter()

@router.post("/{memecoin_id}/analyze")
async def analyze(
    memecoin_id: int,
    db: Session = Depends(get_db)
):
    """
    Trigger comprehensive analysis for a specific memecoin.
    """
    memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
    if not memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    
    # Update status to analyzing
    memecoin.status = MemeStatus.ANALYZING
    db.commit()
    
    try:
        # Perform analysis
        analysis_result = await analyze_memecoin(memecoin)
        
        # Update memecoin with analysis results
        memecoin.social_score = analysis_result.get("social_score")
        memecoin.security_score = analysis_result.get("security_score")
        memecoin.potential_score = analysis_result.get("potential_score")
        memecoin.status = MemeStatus.VERIFIED
        
        db.commit()
        return analysis_result
    except Exception as e:
        memecoin.status = MemeStatus.REJECTED
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-potential")
async def get_top_coins(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top memecoin opportunities based on potential score.
    """
    return await get_top_potential_coins(db, limit)

@router.get("/top-potential", response_model=List[dict])
def get_top_potential(
    *,
    db: Session = Depends(get_db),
    min_score: float = 0.7,
    limit: int = 10
):
    """
    Get top memecoins by potential score.
    """
    top_coins = db.query(
        Memecoin.id,
        Memecoin.name,
        Memecoin.symbol,
        Memecoin.potential_score,
        Memecoin.social_score,
        Memecoin.risk_score
    ).filter(
        Memecoin.potential_score >= min_score,
        Memecoin.status == MemeStatus.VERIFIED
    ).order_by(
        Memecoin.potential_score.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": coin.id,
            "name": coin.name,
            "symbol": coin.symbol,
            "potential_score": coin.potential_score,
            "social_score": coin.social_score,
            "risk_score": coin.risk_score
        }
        for coin in top_coins
    ]

@router.get("/{memecoin_id}/risk-factors")
def get_risk_factors(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int
):
    """
    Get detailed risk analysis for a memecoin.
    """
    memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
    if not memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    
    # Analyze various risk factors
    risk_factors = {
        "contract_verified": memecoin.contract_verified,
        "liquidity_risk": "HIGH" if memecoin.liquidity_usd < 50000 else "LOW",
        "holder_concentration": analyze_holder_concentration(memecoin),
        "social_authenticity": analyze_social_authenticity(memecoin),
        "contract_risks": memecoin.contract_audit if memecoin.contract_audit else {}
    }
    
    return risk_factors

@router.get("/market-sentiment")
def get_market_sentiment(
    *,
    db: Session = Depends(get_db)
):
    """
    Get overall market sentiment for memecoins.
    """
    # Calculate average sentiment scores
    sentiment = db.query(
        func.avg(Memecoin.social_score).label('avg_social_score'),
        func.avg(Memecoin.potential_score).label('avg_potential_score'),
        func.count(Memecoin.id).label('total_coins')
    ).filter(
        Memecoin.status == MemeStatus.VERIFIED
    ).first()
    
    return {
        "average_social_score": round(sentiment.avg_social_score, 2),
        "average_potential": round(sentiment.avg_potential_score, 2),
        "tracked_coins": sentiment.total_coins,
        "market_status": get_market_status(sentiment.avg_social_score)
    }

def analyze_holder_concentration(memecoin: Memecoin) -> str:
    """
    Analyze wallet concentration risk.
    """
    # This would be implemented with actual blockchain data analysis
    return "MEDIUM"  # Placeholder

def analyze_social_authenticity(memecoin: Memecoin) -> str:
    """
    Analyze if social engagement is authentic.
    """
    # This would be implemented with social media analysis
    return "AUTHENTIC"  # Placeholder

def get_market_status(avg_sentiment: float) -> str:
    """
    Determine overall market status.
    """
    if avg_sentiment >= 0.8:
        return "BULLISH"
    elif avg_sentiment >= 0.5:
        return "NEUTRAL"
    else:
        return "BEARISH" 