from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class LeaseStatus(str, enum.Enum):
    active = "active"
    terminated = "terminated"

class Lease(Base):
    __tablename__ = "leases"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    monthly_rent = Column(Float, nullable=False)
    status = Column(Enum(LeaseStatus), default=LeaseStatus.active, nullable=False)

    unit = relationship("Unit", back_populates="leases")
    tenant = relationship("Tenant", back_populates="leases")