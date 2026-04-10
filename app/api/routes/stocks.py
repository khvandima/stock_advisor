from fastapi import HTTPException, APIRouter, status, Depends

from app.db.models import User
from app.core.dependencies import get_current_user

from app.mcp.tools.krx_data import get_stock_price, get_stock_history
from app.mcp.tools.signals import get_signal

from app.schemas.stock import StockPriceResponse, StockHistoryItem, SignalResponse

from app.logger import logger


router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get('/{ticker}')
async def stock_price(ticker: str, current_user: User = Depends(get_current_user)) -> StockPriceResponse:
    try:
        result =  get_stock_price(ticker)
        return result
    except Exception as e:
        logger.error(f"Failed to get stock price for {ticker}: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/{ticker}/history')
async def stock_history(ticker: str, days: int = 30, current_user: User = Depends(get_current_user)) -> list[StockHistoryItem]:
    try:
        result = get_stock_history(ticker, days=days)
        return result
    except Exception as e:
        logger.error(f"Failed to get stock history for {ticker}: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/{ticker}/signal')
async def signal(ticker: str, current_user: User = Depends(get_current_user)) -> SignalResponse:
    try:
        result = get_signal(ticker)
        return result
    except Exception as e:
        logger.error(f"Failed to get signal for {ticker}: {e}")
        raise HTTPException(status_code=404, detail=str(e))