from pykrx import stock
import pandas as pd
from datetime import datetime, timedelta
from app.logger import logger


def get_stock_price(ticker: str) -> dict:
    """
    Get the latest market price for a Korean stock by ticker.
    Returns OHLCV data (open, high, low, close, volume) for the most recent trading day,
    along with the company name.
    Use this when the user asks about the current price of a specific stock.
    """
    try:
        today = datetime.today().strftime("%Y%m%d")
        week_ago = (datetime.today() - timedelta(days=7)).strftime("%Y%m%d")
        df = stock.get_market_ohlcv_by_date(week_ago, today, ticker)
        df = df.rename(columns={
            "시가": "open",
            "고가": "high",
            "저가": "low",
            "종가": "close",
            "거래량": "volume",
            "등락률": "change_rate"
        })
        name = stock.get_market_ticker_name(ticker)
        result = df.iloc[-1].to_dict()
        result["name"] = name
        result["ticker"] = ticker
        return result
    except Exception as e:
        logger.error(f"Failed to get stock price for {ticker}: {e}")
        raise


def get_stock_history(ticker: str, days: int = 30) -> list[dict]:
    """
    Get historical OHLCV price data for a Korean stock by ticker.
    Returns a list of daily price records for the specified number of days.
    Use this when the user wants to see price trends or charts for a stock.
    """
    try:
        today = datetime.today().strftime("%Y%m%d")
        from_date = (datetime.today() - timedelta(days=days)).strftime("%Y%m%d")
        df = stock.get_market_ohlcv_by_date(from_date, today, ticker)
        df = df.rename(columns={
            "시가": "open",
            "고가": "high",
            "저가": "low",
            "종가": "close",
            "거래량": "volume",
            "등락률": "change_rate"
        })
        df["ticker"] = ticker
        df["date"] = df.index.strftime("%Y-%m-%d")
        return df.reset_index(drop=True).to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to get stock history for {ticker}: {e}")
        raise