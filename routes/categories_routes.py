from db.database import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models.models import Category
from schemas.schemas import CategoryCreate, CategoryOut

router = APIRouter(tags=["Categories"])


@router.post("/categories/", response_model=CategoryCreate)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Add a new category."""
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/list/categories/", response_model=list[CategoryOut])
def list_all_categories(db: Session = Depends(get_db)):
    """List all categories."""
    return db.query(Category).all()


@router.get("/categories/{id}", response_model=CategoryOut)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return {"error": "Category not found"}, status.HTTP_404_NOT_FOUND
    return category


@router.put("/categories/{id}", response_model=CategoryOut)
def update_category_by_id(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    """Update a category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        return {"error": "Category not found"}, status.HTTP_404_NOT_FOUND

    category.name = category.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        return {"error": "Category not found"}, status.HTTP_404_NOT_FOUND

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}


