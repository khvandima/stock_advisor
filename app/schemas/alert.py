from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class AlertCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ticker: str
    threshold: float
    condition: str


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    ticker: str
    threshold: float
    condition: str
    is_active: bool
    created_at: datetime