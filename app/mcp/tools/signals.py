from app.mcp.tools.krx_data import get_stock_history
from collections import Counter
import pandas as pd

from app.logger import logger


def get_signal(ticker: str):
    """
    Analyze a Korean stock and return a trading signal (bullish/bearish/neutral).
    Calculates RSI, MACD, and Moving Averages based on the last 60 days of price data.
    Returns the signal along with indicator values.
    Use this when the user asks whether to buy or sell a stock, or wants a market signal.
    Args:
    ticker: Korean stock ticker (e.g. '005930' for Samsung Electronics)
    """
    logger.info(f"get_signal called: ticker={ticker}")
    try:
        df = pd.DataFrame(get_stock_history(ticker, days=90))

        # RSI
        delta = df['close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + gain / loss))
        rsi_value = rsi.iloc[-1]
        if rsi_value < 30:
            rsi_signal = 'bullish'
        elif rsi_value > 70:
            rsi_signal = 'bearish'
        else:
            rsi_signal = 'neutral'

        # MACD
        ema12 = df['close'].ewm(span=12).mean()
        ema26 = df['close'].ewm(span=26).mean()
        macd = ema12 - ema26
        signal_line = macd.ewm(span=9).mean()
        macd_value = macd.iloc[-1]
        signal_value = signal_line.iloc[-1]
        if macd_value > signal_value:
            macd_signal = 'bullish'
        else:
            macd_signal = 'bearish'

        # Moving avarage
        ma20 = df['close'].rolling(20).mean().iloc[-1]
        ma50 = df['close'].rolling(50).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        if current_price > ma20 and current_price > ma50:
            ma_signal = 'bullish'
        else:
            ma_signal = 'bearish'

        votes = [rsi_signal, macd_signal, ma_signal]
        signal = Counter(votes).most_common(1)[0][0]

        result = {
            'ticker': ticker,
            'signal': signal,
            'rsi': rsi_value,
            'macd': macd_value,
            'ma20': ma20,
            'ma50': ma50,
        }
        logger.info(f"get_signal result: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to calculate signal for {ticker}: {e}")
        raise