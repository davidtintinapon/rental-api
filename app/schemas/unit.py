from pydantic import BaseModel
from typing import Optional
from app.models.unit import UnitStatus

class UnitCreate(BaseModel):
    unit_number: str
    bedrooms: int
    monthly_rent: float
    status: UnitStatus = UnitStatus.vacant

class UnitUpdate(BaseModel):
    unit_number: Optional[str] = None
    bedrooms: Optional[int] = None
    monthly_rent: Optional[float] = None
    status: Optional[UnitStatus] = None

class UnitResponse(BaseModel):
    id: int
    property_id: int
    unit_number: str
    bedrooms: int
    monthly_rent: float
    status: UnitStatus

    model_config = {"from_attributes": True}