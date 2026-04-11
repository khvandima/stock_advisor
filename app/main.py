from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from typing import AsyncGenerator
from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.api.routes import auth
from app.api.routes import portfolio
from app.api.routes import stocks
from app.api.routes import alerts
from app.api.routes import chat

from app.agent.graph import get_mcp_tools
from app.agent.graph import build_graph

from app.config import settings
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting lifespan")
    tools, client = await get_mcp_tools()
    async with AsyncPostgresSaver.from_conn_string(
            settings.DATABASE_URL.replace("+asyncpg", "")
    ) as checkpointer:
        await checkpointer.setup()
        graph = build_graph(tools, checkpointer=checkpointer)
        app.state.graph = graph
        app.state.mcp_client = client
        yield
    logger.info("Stopping lifespan")


app = FastAPI(
    title="Stock AI Advisor",
    version="0.1.0",
    description="AI assistant for Korean stock market KOSPI/KOSDAQ",
    lifespan=lifespan
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(stocks.router)
app.include_router(alerts.router)
app.include_router(chat.router)



@app.get("/health")
async def health_check():
    """Health check endpoint — проверяет доступность всех компонентов."""
    return {"status": "ok"}
