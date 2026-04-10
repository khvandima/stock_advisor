from pydantic import BaseModel, ConfigDict


class StockPriceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ticker: str
    name: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    change_rate: float


class StockHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    change_rate: float
    date: str


class SignalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ticker: str
    signal: str
    rsi: float
    macd: float
    ma20: float
    ma50: float