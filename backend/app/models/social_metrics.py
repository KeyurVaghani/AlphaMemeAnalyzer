from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class Platform(str, enum.Enum):
    TWITTER = "twitter"
    TELEGRAM = "telegram"
    REDDIT = "reddit"

class SocialMetrics(Base):
    __tablename__ = "social_metrics"

    id = Column(Integer, primary_key=True, index=True)
    memecoin_id = Column(Integer, ForeignKey("memecoins.id", ondelete="CASCADE"))
    platform = Column(Enum(Platform))
    mentions_count = Column(Integer, default=0)
    engagement_rate = Column(Float)
    sentiment_score = Column(Float)  # -1 to 1
    follower_count = Column(Integer, default=0)
    influencer_mentions = Column(JSON)  # Store influencer data
    viral_posts = Column(JSON)  # Store viral post data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    memecoin = relationship("Memecoin", back_populates="social_metrics")

    class Config:
        orm_mode = True 