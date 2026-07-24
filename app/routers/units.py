from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.unit import Unit, UnitStatus
from app.models.property import Property
from app.schemas.unit import UnitCreate, UnitUpdate, UnitResponse
from app.routers.properties import get_owner
from app.models.user import UserRole

router = APIRouter(tags=["units"])

@router.get("/properties/{property_id}/units", response_model=list[UnitResponse])
def get_units(
    property_id: int,
    status: Optional[UnitStatus] = Query(None),
    db: Session = Depends(get_db),
    current_owner=Depends(get_owner)
):
    db_property = db.query(Property).filter(
        Property.id == property_id,
        Property.is_deleted == False
    ).first()

    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")

    if current_owner.role != UserRole.admin and db_property.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    query = db.query(Unit).filter(Unit.property_id == property_id)

    if status:
        query = query.filter(Unit.status == status)

    return query.all()

@router.post("/properties/{property_id}/units", response_model=UnitResponse, status_code=201)
def create_unit(
    property_id: int,
    unit_data: UnitCreate,
    db: Session = Depends(get_db),
    current_owner=Depends(get_owner)
):
    db_property = db.query(Property).filter(
        Property.id == property_id,
        Property.is_deleted == False
    ).first()

    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")

    if current_owner.role != UserRole.admin and db_property.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_unit = Unit(
        **unit_data.model_dump(),
        property_id=property_id
    )
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

@router.patch("/units/{unit_id}", response_model=UnitResponse)
def update_unit(
    unit_id: int,
    unit_data: UnitUpdate,
    db: Session = Depends(get_db),
    current_owner=Depends(get_owner)
):
    db_unit = db.query(Unit).filter(Unit.id == unit_id).first()

    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    db_property = db.query(Property).filter(
        Property.id == db_unit.property_id
    ).first()

    if current_owner.role != UserRole.admin and db_property.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for field, value in unit_data.model_dump(exclude_unset=True).items():
        setattr(db_unit, field, value)

    db.commit()
    db.refresh(db_unit)
    return db_unit