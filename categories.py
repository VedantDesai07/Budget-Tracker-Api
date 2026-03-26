from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    CategoryDetailResponse, CategorySpending, MessageResponse
)
from app.services import category_service

router = APIRouter(prefix="/budgets/{budget_id}/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryResponse])
def list_categories(budget_id: int, db: Session = Depends(get_db)):
    """List all categories for a budget."""
    return category_service.get_categories(db, budget_id)


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(budget_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a category within a budget."""
    return category_service.create_category(db, budget_id, data)


@router.get("/{category_id}", response_model=CategoryDetailResponse)
def get_category(budget_id: int, category_id: int, db: Session = Depends(get_db)):
    """Get a category with its spending stats."""
    cat = category_service.get_category(db, budget_id, category_id)
    spending = category_service.get_category_spending(db, budget_id, category_id)
    return CategoryDetailResponse(**cat.__dict__, spending=spending)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(budget_id: int, category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    """Update a category."""
    return category_service.update_category(db, budget_id, category_id, data)


@router.delete("/{category_id}", response_model=MessageResponse)
def delete_category(budget_id: int, category_id: int, db: Session = Depends(get_db)):
    """Delete a category."""
    category_service.delete_category(db, budget_id, category_id)
    return {"message": f"Category {category_id} deleted successfully"}


@router.get("/{category_id}/spending", response_model=CategorySpending)
def category_spending(budget_id: int, category_id: int, db: Session = Depends(get_db)):
    """Get spending breakdown for a category."""
    return category_service.get_category_spending(db, budget_id, category_id)
