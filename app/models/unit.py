from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class UnitStatus(enum.Enum):
    vacant = "vacant"
    occupied = "occupied"

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    unit_number = Column(String, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    monthly_rent = Column(Float, nullable=False)
    status = Column(Enum(UnitStatus), default=UnitStatus.vacant, nullable=False)

    property = relationship("Property", back_populates="units")
    leases = relationship("Lease", back_populates="unit")