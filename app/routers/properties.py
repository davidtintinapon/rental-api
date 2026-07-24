from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.property import Property
from app.models.user import User, UserRole
from app.schemas.property import PropertyCreate, PropertyResponse, PropertyUpdate
from app.core.security import get_current_user

router = APIRouter(prefix="/properties", tags=["properties"])

def get_owner(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[PropertyResponse])
def get_properties(
    city: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_owner: User = Depends(get_owner)
):
    query = db.query(Property).filter(Property.is_deleted == False)

    if current_owner.role != UserRole.admin:
        query = query.filter(Property.owner_id == current_owner.id)

    if city:
        query = query.filter(Property.city == city)

    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

@router.post("/", response_model=PropertyResponse, status_code=201)
def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    current_owner: User = Depends(get_owner)
):
    new_property = Property(
        **property_data.model_dump(),
        owner_id=current_owner.id
    )

    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_owner: User = Depends(get_owner)
):
    property = db.query(Property).filter(
        Property.id == property_id,
        Property.is_deleted == False
    ).first()

    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    if current_owner.role != UserRole.admin and property.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return property

@router.patch("/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    db: Session = Depends(get_db),
    current_owner: User = Depends(get_owner)
):
    property = db.query(Property).filter(
        Property.id == property_id,
        Property.is_deleted == False
    ).first()

    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    if current_owner.role != UserRole.admin and property.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for field, value in property_data.model_dump(exclude_unset=True).items():
        setattr(property, field, value)

    db.commit()
    db.refresh(property)
    return property

@router.delete("/{property_id}", status_code=204)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_owner: User = Depends(get_owner)
):
    property = db.query(Property).filter(
        Property.id == property_id,
        Property.is_deleted == False
    ).first()

    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    if current_owner.role != UserRole.admin and property.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    property.is_deleted = True
    db.commit()
    return None