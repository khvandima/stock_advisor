from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from app.api.routes import auth

from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting lifespan")
    yield
    logger.info("Stopping lifespan")


app = FastAPI(
    title="Stock AI Advisor",
    version="0.1.0",
    description="AI assistant for Korean stock market KOSPI/KOSDAQ",
    lifespan=lifespan
)


app.include_router(auth.router)


@app.get("/health")
async def health_check():
    """Health check endpoint — проверяет доступность всех компонентов."""
    return {"status": "ok"}
