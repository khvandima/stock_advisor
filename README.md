# 📈 Stock AI Advisor

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.35-orange)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

AI assistant for retail investors on the Korean stock market (KOSPI/KOSDAQ). Helps make buy/sell decisions based on technical analysis, official corporate disclosures, and real-time news.

---

## Features

- **Portfolio + P&L** — track your stocks and real-time profit/loss
- **Price Charts** — interactive candlestick charts with volume via Recharts
- **AI Signals** — bullish / bearish / neutral based on RSI, MACD, Moving Averages
- **News + AI Analysis** — news aggregation with AI explanation of price impact
- **AI Advisor** — chat agent that analyzes the market and gives data-backed recommendations
- **Morning Digest** — automated daily summary at 9:00 KST via APScheduler
- **Alerts** — notifications when a stock reaches your target price

---

## Tech Stack

| Category | Technologies |
|---|---|
| Backend | FastAPI, Uvicorn |
| AI Agent | LangGraph, LangChain, Groq (llama-3.3-70b-versatile) |
| MCP | mcp SDK (stdio transport) |
| Database | PostgreSQL, SQLAlchemy 2.0 async, Alembic |
| Auth | JWT (python-jose), bcrypt |
| Scheduler | APScheduler |
| Data Sources | pykrx, DART API, Tavily |
| Frontend | React 18 + Vite + Recharts + Zustand + Tailwind CSS |
| Testing | pytest, pytest-asyncio |
| CI/CD | GitHub Actions |
| Deploy | Docker, Docker Compose |

---

## Project Structure

```
stock_advisor/
├── app/
│   ├── agent/          # LangGraph agent
│   │   ├── graph.py    # ReAct graph
│   │   └── state.py    # AgentState
│   ├── api/routes/     # FastAPI routes
│   │   ├── auth.py
│   │   ├── portfolio.py
│   │   ├── stocks.py
│   │   ├── alerts.py
│   │   └── chat.py
│   ├── mcp/
│   │   ├── server.py   # MCP server (stdio)
│   │   └── tools/      # Agent tools
│   │       ├── krx_data.py      # pykrx market data
│   │       ├── signals.py       # RSI, MACD, MA
│   │       ├── dart.py          # DART API disclosures
│   │       ├── tavily_news.py   # News search
│   │       └── portfolio.py     # User portfolio tool
│   ├── scheduler/
│   │   └── morning_digest.py   # Morning digest + alert checker
│   ├── db/
│   │   ├── models.py   # User, PortfolioItem, Alert, Signal, Digest
│   │   └── session.py
│   ├── core/
│   │   ├── security.py      # JWT, bcrypt
│   │   └── dependencies.py  # get_current_user
│   ├── schemas/        # Pydantic models
│   ├── config.py       # Pydantic Settings
│   ├── constants.py    # SYSTEM_PROMPT
│   └── main.py         # FastAPI app + lifespan
├── frontend/           # React + Vite
│   └── src/
│       ├── components/
│       │   ├── Auth/       # Login + Register
│       │   ├── Dashboard/  # Sidebar layout
│       │   ├── Portfolio/  # CRUD + P&L
│       │   ├── StockChart/ # Recharts charts
│       │   ├── Signals/    # RSI/MACD/MA
│       │   ├── News/       # News + AI analysis
│       │   └── AIChat/     # Chat with agent
│       ├── api/client.js   # Axios + JWT interceptor
│       └── store/          # Zustand global state
├── tests/
│   ├── unit/           # Security tests
│   └── integration/    # Portfolio tests
├── alembic/            # DB migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── start.sh
```

---

## Quick Start

### Requirements

- Python 3.12+
- Node.js 20+
- PostgreSQL (or Docker)

### 1. Clone the repository

```bash
git clone https://github.com/khvandima/stock-advisor.git
cd stock_advisor
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Fill in `.env`:

```env
APP_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/stock_advisor

GROQ_API_KEY=your-groq-api-key
DART_API_KEY=your-dart-api-key
TAVILY_API_KEY=your-tavily-api-key

LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2048
```

### 3. Start PostgreSQL

```bash
docker run -d \
  --name stock-postgres \
  -e POSTGRES_DB=stock_advisor \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5433:5432 \
  postgres:16-alpine
```

### 4. Install dependencies and run migrations

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```

### 5. Start the backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Start the frontend

```bash
cd frontend
cp .env.example .env    # set VITE_API_URL=http://your-server-ip:8000
npm install
npm run dev -- --host 0.0.0.0
```

### Or with one command

```bash
chmod +x start.sh
./start.sh
```

---

## Docker Compose

```bash
docker-compose up -d --build
```

App will be available at `http://localhost:8000`.

---

## API Keys

| Service | Where to get | Description |
|---|---|---|
| Groq | [console.groq.com](https://console.groq.com) | LLM for the agent |
| DART | [opendart.fss.or.kr](https://opendart.fss.or.kr) | Korean corporate disclosures |
| Tavily | [tavily.com](https://tavily.com) | Real-time news search |

---

## Running Tests

```bash
pytest tests/ -v --cov=app
```

---

## Agent MCP Tools

| Tool | Description |
|---|---|
| `get_stock_price` | Current stock price by ticker |
| `get_stock_history` | Historical OHLCV data |
| `get_signal` | Technical signal: RSI, MACD, MA |
| `get_dart_disclosures` | Official DART filings |
| `get_financial_statements` | Financial statements (revenue, profit) |
| `tavily_search` | Real-time news search |
| `search_ticker_by_name` | Find ticker by company name |
| `get_user_portfolio` | Current user's portfolio |

---

## Architecture Principles

- `PostgresSaver` for agent session persistence
- `config.py` layer via Pydantic Settings — no direct `os.getenv()` calls
- JWT authentication on all endpoints
- Pydantic models for all input/output data
- Conversation summarization — old messages compressed by LLM to save tokens
- `thread_id` scoped per-user: `f"{user_id}_{session_id}"`
- Heavy objects (graph, MCP client) initialized in FastAPI `lifespan`

---

## Author

GitHub: [khvandima](https://github.com/khvandima)