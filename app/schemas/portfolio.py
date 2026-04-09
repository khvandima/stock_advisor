from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class PortfolioItemCreate(BaseModel):
    ticker: str
    quantity: int
    purchase_price: float


class PortfolioItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    ticker: str
    quantity: int
    purchase_price: float
    created_at: datetime