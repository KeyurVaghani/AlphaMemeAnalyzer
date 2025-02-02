from typing import Dict, List, Optional
import tweepy
import telegram
import asyncpraw
from textblob import TextBlob
from app.core.config import settings
from app.models.social_metrics import Platform, SocialMetrics
from sqlalchemy.orm import Session
import json
import asyncio
from datetime import datetime, timedelta

class SocialMonitor:
    def __init__(self):
        # Initialize API clients
        self.twitter_client = tweepy.Client(
            bearer_token=settings.TWITTER_API_KEY,
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET
        )
        
        self.telegram_bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
        
        self.reddit_client = asyncpraw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent="MemecoinAlphaHunter/1.0"
        )

    async def analyze_social_metrics(self, db: Session, memecoin_id: int, symbol: str) -> Dict:
        """
        Analyze social metrics across platforms for a memecoin
        """
        tasks = [
            self.analyze_twitter(symbol),
            self.analyze_telegram(symbol),
            self.analyze_reddit(symbol)
        ]
        
        results = await asyncio.gather(*tasks)
        twitter_data, telegram_data, reddit_data = results
        
        # Combine metrics
        total_mentions = sum(d.get('mentions_count', 0) for d in [twitter_data, telegram_data, reddit_data])
        avg_sentiment = sum(d.get('sentiment_score', 0) * d.get('mentions_count', 0) for d in [twitter_data, telegram_data, reddit_data]) / total_mentions if total_mentions > 0 else 0
        
        # Store metrics for each platform
        for platform_data in [
            (Platform.TWITTER, twitter_data),
            (Platform.TELEGRAM, telegram_data),
            (Platform.REDDIT, reddit_data)
        ]:
            platform, data = platform_data
            metrics = SocialMetrics(
                memecoin_id=memecoin_id,
                platform=platform,
                mentions_count=data.get('mentions_count', 0),
                engagement_rate=data.get('engagement_rate', 0),
                sentiment_score=data.get('sentiment_score', 0),
                follower_count=data.get('follower_count', 0),
                influencer_mentions=data.get('influencer_mentions', {}),
                viral_posts=data.get('viral_posts', {})
            )
            db.add(metrics)
        
        db.commit()
        
        return {
            "total_mentions": total_mentions,
            "average_sentiment": avg_sentiment,
            "platform_data": {
                "twitter": twitter_data,
                "telegram": telegram_data,
                "reddit": reddit_data
            }
        }

    async def analyze_twitter(self, symbol: str) -> Dict:
        """
        Analyze Twitter metrics for a memecoin
        """
        try:
            # Search for tweets
            query = f"#{symbol} OR ${symbol} -is:retweet"
            tweets = self.twitter_client.search_recent_tweets(
                query=query,
                max_results=100,
                tweet_fields=['public_metrics', 'created_at']
            )
            
            if not tweets.data:
                return self._empty_metrics()
            
            # Calculate metrics
            mentions_count = len(tweets.data)
            total_engagement = sum(t.public_metrics['like_count'] + t.public_metrics['retweet_count'] for t in tweets.data)
            engagement_rate = total_engagement / mentions_count if mentions_count > 0 else 0
            
            # Sentiment analysis
            sentiments = [TextBlob(tweet.text).sentiment.polarity for tweet in tweets.data]
            avg_sentiment = sum(sentiments) / len(sentiments)
            
            # Track viral posts
            viral_posts = [
                {
                    'text': tweet.text,
                    'metrics': tweet.public_metrics,
                    'created_at': tweet.created_at.isoformat()
                }
                for tweet in tweets.data
                if tweet.public_metrics['like_count'] > 1000 or tweet.public_metrics['retweet_count'] > 500
            ]
            
            return {
                'mentions_count': mentions_count,
                'engagement_rate': engagement_rate,
                'sentiment_score': avg_sentiment,
                'viral_posts': viral_posts
            }
        except Exception as e:
            print(f"Twitter analysis error: {str(e)}")
            return self._empty_metrics()

    async def analyze_telegram(self, symbol: str) -> Dict:
        """
        Analyze Telegram metrics for a memecoin
        """
        try:
            # Get group info and messages
            chat = await self.telegram_bot.get_chat(settings.TELEGRAM_CHAT_ID)
            messages = await self.telegram_bot.get_chat_history(
                chat_id=settings.TELEGRAM_CHAT_ID,
                limit=100
            )
            
            # Calculate metrics
            symbol_messages = [msg for msg in messages if symbol.lower() in msg.text.lower()]
            mentions_count = len(symbol_messages)
            
            if mentions_count == 0:
                return self._empty_metrics()
            
            total_views = sum(msg.views for msg in symbol_messages if hasattr(msg, 'views'))
            engagement_rate = total_views / mentions_count if mentions_count > 0 else 0
            
            # Sentiment analysis
            sentiments = [TextBlob(msg.text).sentiment.polarity for msg in symbol_messages]
            avg_sentiment = sum(sentiments) / len(sentiments)
            
            return {
                'mentions_count': mentions_count,
                'engagement_rate': engagement_rate,
                'sentiment_score': avg_sentiment,
                'follower_count': chat.members_count if hasattr(chat, 'members_count') else 0
            }
        except Exception as e:
            print(f"Telegram analysis error: {str(e)}")
            return self._empty_metrics()

    async def analyze_reddit(self, symbol: str) -> Dict:
        """
        Analyze Reddit metrics for a memecoin
        """
        try:
            # Search for posts
            subreddits = ['CryptoMoonShots', 'CryptoCurrency', 'SatoshiStreetBets']
            posts = []
            
            for subreddit_name in subreddits:
                subreddit = await self.reddit_client.subreddit(subreddit_name)
                async for post in subreddit.search(symbol, limit=100):
                    posts.append(post)
            
            if not posts:
                return self._empty_metrics()
            
            # Calculate metrics
            mentions_count = len(posts)
            total_score = sum(post.score for post in posts)
            engagement_rate = total_score / mentions_count if mentions_count > 0 else 0
            
            # Sentiment analysis
            sentiments = [TextBlob(post.title + ' ' + post.selftext).sentiment.polarity for post in posts]
            avg_sentiment = sum(sentiments) / len(sentiments)
            
            # Track viral posts
            viral_posts = [
                {
                    'title': post.title,
                    'url': post.url,
                    'score': post.score,
                    'created_utc': post.created_utc
                }
                for post in posts
                if post.score > 100
            ]
            
            return {
                'mentions_count': mentions_count,
                'engagement_rate': engagement_rate,
                'sentiment_score': avg_sentiment,
                'viral_posts': viral_posts
            }
        except Exception as e:
            print(f"Reddit analysis error: {str(e)}")
            return self._empty_metrics()

    def _empty_metrics(self) -> Dict:
        """
        Return empty metrics structure
        """
        return {
            'mentions_count': 0,
            'engagement_rate': 0,
            'sentiment_score': 0,
            'follower_count': 0,
            'viral_posts': []
        } 