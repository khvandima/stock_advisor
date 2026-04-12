from pydantic import BaseModel, ConfigDict
from typing import Literal
from datetime import datetime
from uuid import UUID


class AlertCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ticker: str
    threshold: float
    condition: Literal["above", "below"]


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    ticker: str
    threshold: float
    condition: str
    is_active: bool
    created_at: datetime