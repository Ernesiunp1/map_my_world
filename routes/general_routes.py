from datetime import datetime
from db.database import get_db
from fastapi import HTTPException, Request
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, selectinload
from utils.fresh_recommendations import get_fresh_recommendations
from models.models import Location, Category, LocationCategoryReviewed
from schemas.schemas import LocationSchema, CategoryCreate, LocationCreate, CategoryOut, RecommendationOut
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["Generals"])
# Templates

templates = Jinja2Templates(directory="templates")


# main route (server map)
@router.get("/", response_class=HTMLResponse)
def serve_map(request: Request, db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    print("request: ", request, "categories: ", categories)
    return templates.TemplateResponse("map.html", {
        "request": request,
        "categories": categories
    })


@router.post("/reviews/", response_model=dict)
def mark_location_as_reviewed(location_id: int, db: Session = Depends(get_db)):
    """Mark a location-category combination as reviewed."""

    association = db.query(LocationCategoryReviewed).filter(
        LocationCategoryReviewed.location_id == location_id).first()

    if not association:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Location-Category association not found")

    # look if there is an existing review
    existing_review = db.query(LocationCategoryReviewed).filter(
        LocationCategoryReviewed.location_id == location_id).first()

    if existing_review:
        existing_review.last_reviewed = datetime.utcnow()
    else:
        new_review = LocationCategoryReviewed(
            location_id=location_id,
            last_reviewed=datetime.utcnow()
        )
        db.add(new_review)

    db.commit()
    return {"status": "success",
            "message": "Marked as reviewed successfully"}


@router.get("/recommendations/", response_model=list[RecommendationOut])
def get_recommendations_needs_review(db: Session = Depends(get_db)):
    """Get 10 location-category combinations that need review."""
    return get_fresh_recommendations(db)   # you can found this in utils/fresh_recommendations.py
