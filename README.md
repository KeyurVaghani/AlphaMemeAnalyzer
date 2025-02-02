# Memecoin Alpha Hunter System (MAHS)

A sophisticated system for identifying high-potential memecoins using AI-driven analysis, on-chain data, and social sentiment tracking.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technical Documentation](#technical-documentation)
  - [Architecture](#architecture)
  - [Tech Stack](#tech-stack)
  - [API Integrations](#api-integrations)
- [Developer Guide](#developer-guide)
  - [Getting Started](#getting-started)
  - [Codebase Structure](#codebase-structure)
- [Project Status](#project-status)
- [Contributing](#contributing)
- [License](#license)
- [Detailed Code Documentation](#detailed-code-documentation)
  - [Core Components](#core-components)
    - [Database Models (`app/models/`)](#database-models-appmodels)
    - [API Endpoints (`app/api/api_v1/endpoints/`)](#api-endpoints-appapiapiv1endpoints)
    - [Services (`app/services/`)](#services-appservices)
    - [Configuration (`app/core/`)](#configuration-appcore)
  - [Infrastructure](#infrastructure)
    - [`docker-compose.yml`](#dockercomposeyml)
    - [`Dockerfile`](#dockerfile)
  - [Dependencies (`requirements.txt`)](#dependencies-requirementstxt)
  - [API Structure](#api-structure)
    - [Base URL: `/api/v1`](#base-url-apiv1)
    - [Memecoin Endpoints](#memecoin-endpoints)

## Overview

MAHS is an intelligent system that combines social media sentiment, on-chain metrics, and market data to identify promising memecoin opportunities before significant price movements occur.

## Features

### Social Analysis
- Real-time sentiment tracking across Twitter, Reddit, and Telegram
- Influencer activity monitoring
- Engagement spike detection
- Community growth analytics

### On-Chain Analysis
- Smart contract security scanning
- Liquidity analysis
- Holder distribution tracking
- Whale wallet monitoring

### Risk Assessment
- Contract vulnerability detection
- Team verification
- Scam pattern recognition
- Community authenticity checks

### Trading Tools
- Automated DEX integration
- Portfolio management
- Risk balancing
- Performance tracking

### Memecoin Sniping System
- **Social Hype Detection**
  - AI-powered sentiment analysis
  - Viral keyword tracking
  - Influencer endorsement monitoring
  - Engagement spike alerts (>500% in 24h)

- **On-Chain Analytics**
  - New token launch detection
  - Smart money wallet tracking
  - Liquidity analysis
  - Holder concentration metrics

- **Market Analysis**
  - Volume/FDV ratio tracking
  - DEX liquidity monitoring
  - CEX listing probability
  - Technical indicators

- **Risk Scoring**
  - Contract audit automation
  - Team verification
  - Community authenticity check
  - Scam pattern detection

- **Trading Automation**
  - Sniper bot integration
  - Auto-buy/sell triggers
  - Portfolio rebalancing
  - Risk management

## Technical Documentation

### Architecture

The system consists of five core modules:

1. **Data Collection Engine**
   - Social media API integrations
   - Blockchain data collectors
   - Market data aggregators
   - Influencer tracking system

2. **Analysis Engine**
   - Sentiment analysis system
   - On-chain metrics processor
   - Risk assessment models
   - Scoring algorithms

3. **Alert System**
   - Price movement detection
   - Social spike monitoring
   - Risk factor notifications
   - Portfolio alerts

4. **Trading Integration**
   - DEX interaction layer
   - Order management
   - Position tracking
   - Risk management

5. **Sniping System**
   - Real-time token detection
   - Smart money tracking
   - Auto-execution engine
   - Portfolio optimization

### Tech Stack

**Backend**
- Python 3.11+ with FastAPI
- PostgreSQL for data persistence
- Redis for caching
- Machine Learning (PyTorch, TensorFlow)
- Web3 for blockchain interaction

**Frontend**
- React with TypeScript
- Redux Toolkit
- Material-UI
- TradingView charts

**Infrastructure**
- Docker containers
- AWS cloud hosting
- Kubernetes orchestration
- GitHub Actions CI/CD

**Data Processing**
- Pandas for data manipulation
- NumPy for numerical operations
- Scikit-learn for ML models
- TextBlob for sentiment analysis

**Blockchain Integration**
- Web3.py for Ethereum
- Solana.py for Solana
- Brownie for smart contracts
- CCXT for exchange APIs

**Trading Tools**
- Technical analysis (TA-Lib)
- Binance API integration
- DEX aggregator integration
- Custom sniper bot framework

### API Integrations

**Blockchain**
- DexScreener
- Etherscan/BSCScan
- Solana RPC
- Nansen

**Market Data**
- CoinGecko
- DexTools
- LunarCrush
- CoinMarketCap

## Developer Guide

### Getting Started

1. **Prerequisites**
```bash
- Python 3.9+
- Node.js 16+
- Docker
- PostgreSQL 13+
- Redis
```

2. **Installation**
```bash
# Clone repository
git clone https://github.com/yourusername/memecoin-alpha-hunter.git

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

3. **Configuration**
Create `.env` file:
```env
# API Keys
TWITTER_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
ETHERSCAN_API_KEY=your_key
BSCSCAN_API_KEY=your_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mahs

# Redis
REDIS_URL=redis://localhost:6379
```

### Codebase Structure

**Backend Components**
- `app/main.py` - Application entry point
- `app/core/` - Core configuration and settings
- `app/api/` - API endpoints and routing
- `app/services/` - Business logic implementation
- `app/models/` - Database models and schemas
- `app/db/` - Database configuration

**Key Services**
- `memecoin_hunter.py` - Core analysis engine
- `analysis.py` - Risk assessment service
- `notifications.py` - Alert system

## Project Status

Current development phase: Alpha
- [x] Development environment setup
- [x] Basic API structure
- [x] Database models and relationships
- [x] Core analysis service implementation
- [ ] Sentiment analysis system
- [ ] On-chain analysis
- [ ] Frontend dashboard
- [ ] Trading integration

## Recent Updates

### 2024-04-03
1. Fixed SQLAlchemy model issues:
   - Renamed `metadata` to `coin_metadata` to avoid reserved keyword conflicts
   - Added proper relationship mappings between models
   - Added missing imports for SQLAlchemy relationships

2. Implemented comprehensive memecoin analysis:
   - Added parallel analysis functionality
   - Implemented contract analysis
   - Added social scoring system
   - Integrated risk assessment
   - Added potential score calculation

3. Enhanced error handling and validation:
   - Added proper exception handling in analysis service
   - Improved validation in API endpoints
   - Added comprehensive logging

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License
MIT License - see [LICENSE.md](LICENSE.md)

## Detailed Code Documentation

### Core Components

#### Database Models (`app/models/`)

**`memecoin.py`**
- Core data models for the application
- Key Models:
  - `Memecoin`: Main token entity with blockchain details and analysis scores
    - Market data (price, market cap, supply)
    - Analysis scores (social, security, potential)
    - Social metrics (followers, engagement)
    - Additional data (coin_metadata, timestamps)
  - `PriceHistory`: Historical price and volume data
  - `SocialMetrics`: Platform-specific social engagement metrics
  - `Alert`: Notification configurations for price/social movements
- Relationships:
  - One-to-many between Memecoin and PriceHistory
  - One-to-many between Memecoin and SocialMetrics
  - One-to-many between Memecoin and Alert

#### API Endpoints (`app/api/api_v1/endpoints/`)

**`memecoins.py`**
- CRUD operations for memecoin management
- Endpoints:
  - `POST /`: Create new memecoin tracking
  - `GET /`: List memecoins with filtering options
  - `GET /{memecoin_id}`: Detailed memecoin information
  - `PUT /{memecoin_id}`: Update memecoin data

**`analysis.py`**
- Memecoin analysis and scoring endpoints
- Key Features:
  - Contract analysis
  - Social sentiment calculation
  - Risk assessment
  - Potential score computation
- Endpoints:
  - `POST /{memecoin_id}/analyze`: Trigger comprehensive analysis
  - `GET /top-potential`: List high-potential tokens
  - `GET /{memecoin_id}/risk-factors`: Detailed risk analysis
  - `GET /market-sentiment`: Overall market metrics

**`social.py`**
- Social media metrics management
- Endpoints:
  - `POST /metrics`: Record new social metrics
  - `GET /metrics/{memecoin_id}`: Retrieve historical metrics
- Supports multiple platforms (Twitter, Telegram, Reddit)

**`alerts.py`**
- Alert system configuration and management
- Endpoints:
  - `POST /{memecoin_id}`: Create new price/social alert
  - `GET /active`: List all active alerts
- Supports multiple notification channels

#### Services (`app/services/`)

**`analysis.py`**
- Comprehensive memecoin analysis service
- Key Features:
  - Parallel analysis execution
  - Contract security scanning
  - Social sentiment calculation
  - Risk assessment
  - Potential score computation
  - CEX listing probability
  - Viral trend detection
- Helper Functions:
  - `analyze_contract`: Smart contract analysis
  - `calculate_social_score`: Social metrics scoring
  - `calculate_risk_score`: Risk assessment
  - `calculate_potential_score`: Overall potential calculation
  - `generate_analysis_summary`: Human-readable analysis summary

**`memecoin_hunter.py`**
- Main business logic for memecoin sniping
- Features:
  - Social sentiment analysis
  - On-chain metrics tracking
  - Liquidity monitoring
  - Whale wallet detection
  - Auto-buy execution
  - Risk management
- Configuration:
  - Minimum liquidity: $50,000
  - Minimum holders: 500
  - Engagement spike threshold: 500%
  - Whale threshold: 5 wallets
  - Auto-buy limits: 1-5% portfolio per coin
  - Stop-loss: 15% from peak
  - Take-profit: 2x initial investment

#### Configuration (`app/core/`)

**`config.py`**
- Application configuration management
- Settings:
  - API versioning
  - CORS configuration
  - Database connections
  - External service credentials
- Environment Variables:
  - Database configuration
  - API keys
  - Service endpoints

### Infrastructure

**`docker-compose.yml`**
- Container orchestration
- Services:
  - Backend (FastAPI)
  - PostgreSQL database
  - Redis cache
  - pgAdmin interface
- Network Configuration:
  - Internal network: mahs-network
  - Exposed ports:
    - Backend: 8000
    - Database: 5432
    - Redis: 6379
    - pgAdmin: 5050

**`Dockerfile`**
- Backend service configuration
- Base Image: Python 3.9-slim
- Dependencies:
  - System packages
  - Python requirements
  - Development tools
- Runtime Configuration:
  - Working directory: /app
  - Environment variables
  - Entry point: uvicorn

### Dependencies (`requirements.txt`)

**Core Framework**
- FastAPI 0.104.1
- Uvicorn 0.24.0
- SQLAlchemy 2.0.23
- Alembic 1.12.1

**External APIs**
- Tweepy 4.14.0
- Python-Telegram-Bot 20.6
- PRAW 7.7.1
- Web3 6.11.1

**Data Processing**
- Pandas 2.1.3
- NumPy 1.26.2
- Scikit-learn 1.3.2
- TextBlob 0.17.1

**Development Tools**
- Black 23.11.0
- Flake8 6.1.0
- isort 5.12.0
- pytest 7.4.3

### API Structure

#### Base URL: `/api/v1`

**Memecoin Endpoints**

- POST /memecoins Create new memecoin
- GET /memecoins List memecoins
- GET /memecoins/{id} Get memecoin details
- PUT /memecoins/{id} Update memecoin

**Analysis Endpoints**

- POST /analysis/{id}/analyze Trigger analysis
- GET /analysis/top-potential Get top tokens
- GET /analysis/{id}/risk-factors Get risk analysis
- GET /analysis/market-sentiment Get market overview

**Social Endpoints**

- POST /social/metrics Record metrics
- GET /social/metrics/{id} Get historical data

**Alert Endpoints**

- POST /alerts/{id} Create alert
- GET /alerts/active List active alerts

## Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Virtual Environment (venv)

### Backend Setup
1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up local PostgreSQL:
- Install PostgreSQL
- Create database named 'mahs'
- Update .env with your database credentials

4. Set up local Redis:
- Install Redis
- Default configuration in .env should work (localhost:6379)

5. Run migrations:
```bash
alembic upgrade head
```

6. Start the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API Documentation: http://localhost:8000/docs
- Alternative API Documentation: http://localhost:8000/redoc
- API Root: http://localhost:8000