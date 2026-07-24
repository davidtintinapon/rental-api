from pydantic import BaseModel
from typing import Optional

class PropertyCreate(BaseModel):
    name: str
    address: str
    city: str

class PropertyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None

class PropertyResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    owner_id: int
    is_deleted: bool

    model_config = {"from_attributes": True}