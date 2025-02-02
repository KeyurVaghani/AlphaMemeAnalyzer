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

## Technical Documentation

### Architecture

The system consists of four core modules:

1. **Data Collection Engine**
   - Social media API integrations
   - Blockchain data collectors
   - Market data aggregators

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

### Tech Stack

**Backend**
- Python 3.9+ with FastAPI
- PostgreSQL for data persistence
- Redis for caching
- RabbitMQ for message queuing

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

Current development phase: Foundation
- [x] Development environment setup
- [x] Basic API structure
- [ ] Sentiment analysis system
- [ ] On-chain analysis
- [ ] Frontend dashboard
- [ ] Trading integration

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
  - `PriceHistory`: Historical price and volume data
  - `SocialMetrics`: Platform-specific social engagement metrics
  - `Alert`: Notification configurations for price/social movements
- Enums:
  - `BlockchainType`: Supported chains (ETHEREUM, BSC, SOLANA)
  - `MemeStatus`: Token lifecycle states (NEW, ANALYZING, VERIFIED, etc.)

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
- Core analysis functionality
- Key Components:
  - Contract Analysis
    - Security pattern detection
    - Vulnerability scanning
    - Token distribution analysis
  - Social Score Calculation
    - Platform-specific metrics
    - Engagement analysis
    - Sentiment scoring
  - Risk Assessment
    - Contract risk factors
    - Liquidity analysis
    - Holder concentration
  - Potential Score Computation
    - Market metrics
    - Growth indicators
    - Technical analysis

**`memecoin_hunter.py`**
- Main business logic for memecoin analysis
- Features:
  - Social sentiment analysis
  - On-chain metrics tracking
  - Liquidity monitoring
  - Whale wallet detection
- Configuration:
  - Minimum liquidity: $50,000
  - Minimum holders: 500
  - Engagement spike threshold: 500%
  - Whale threshold: 5 wallets

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