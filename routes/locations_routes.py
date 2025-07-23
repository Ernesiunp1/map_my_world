from db.database import get_db
from fastapi import HTTPException
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, selectinload
from models.models import Location, Category, LocationCategoryReviewed
from schemas.schemas import LocationSchema, LocationCreate, LocationOut

router = APIRouter(tags=["Locations"])



@router.post("/locations/", response_model=LocationSchema)
def create_new_location(location: LocationCreate, db: Session = Depends(get_db)):
    """Create a new location."""
    new_location = Location(
        latitude=location.latitude,
        longitude=location.longitude,
        name=location.name,
        rate=location.rate,
        description=location.description
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    # relate categories to the new location
    for category_id in location.category_ids:
        association = LocationCategoryReviewed(
            location_id=new_location.id,
            category_id=category_id
        )
        db.add(association)

    # Create new categories if they are specified on this request
    for category_name in location.new_categories:
        existing = db.query(Category).filter(Category.name == category_name).first()
        if not existing:
            new_category = Category(name=category_name)
            db.add(new_category)
            db.commit()
            db.refresh(new_category)

            # asociate with the location
            association = LocationCategoryReviewed(
                location_id=new_location.id,
                category_id=new_category.id
            )
            db.add(association)

    db.commit()
    return new_location


@router.get("/list/locations", response_model=list[LocationOut])
def list_all_locations(db: Session = Depends(get_db)):
    """List all locations with their associated categories."""

    locations = db.query(Location).options(selectinload(Location.categories)).all()
    return locations


@router.get("/locations/{id}", response_model=LocationOut)
def get_location_by_id(location_id: int, db: Session = Depends(get_db)):
    """Get a specific location by ID."""

    location = db.query(Location).filter(Location.id == location_id).options(selectinload(Location.categories)).first()

    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Location not found")

    return location


@router.put("/locations/{id}", response_model=LocationSchema)
def update_location_by_id(location_id: int, location: LocationCreate, db: Session = Depends(get_db)):
    """Update a specific location by ID."""

    existing_location = db.query(Location).filter(Location.id == location_id).first()

    if not existing_location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Location not found")

    existing_location.latitude = location.latitude
    existing_location.longitude = location.longitude
    existing_location.name = location.name

    # Clear previous associations
    db.query(LocationCategoryReviewed).filter(LocationCategoryReviewed.location_id == location_id).delete()

    # relate categories to the updated location
    for category_id in location.category_ids:
        association = LocationCategoryReviewed(
            location_id=existing_location.id,
            category_id=category_id
        )
        db.add(association)

    # Create new categories if they are specified on this request
    for category_name in location.new_categories:
        existing = db.query(Category).filter(Category.name == category_name).first()
        if not existing:
            new_category = Category(name=category_name)
            db.add(new_category)
            db.commit()
            db.refresh(new_category)

            # asociate with the location
            association = LocationCategoryReviewed(
                location_id=existing_location.id,
                category_id=new_category.id
            )
            db.add(association)

    db.commit()
    db.refresh(existing_location)

    return existing_location


@router.delete("/locations/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a specific location by ID."""

    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Location not found")

    db.delete(location)
    db.commit()
    return {"detail": "Location deleted successfully"}