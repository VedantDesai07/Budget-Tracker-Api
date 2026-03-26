from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import (
    BudgetCreate, BudgetUpdate, BudgetResponse,
    BudgetDetailResponse, BudgetSummary, MessageResponse
)
from app.services import budget_service

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("", response_model=List[BudgetResponse])
def list_budgets(db: Session = Depends(get_db)):
    """List all budgets."""
    return budget_service.get_all_budgets(db)


@router.post("", response_model=BudgetResponse, status_code=201)
def create_budget(data: BudgetCreate, db: Session = Depends(get_db)):
    """Create a new budget."""
    return budget_service.create_budget(db, data)


@router.get("/{budget_id}", response_model=BudgetDetailResponse)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    """Get a single budget with its financial summary."""
    budget = budget_service.get_budget(db, budget_id)
    summary = budget_service.get_budget_summary(db, budget_id)
    return BudgetDetailResponse(**budget.__dict__, summary=summary)


@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(budget_id: int, data: BudgetUpdate, db: Session = Depends(get_db)):
    """Update a budget."""
    return budget_service.update_budget(db, budget_id, data)


@router.delete("/{budget_id}", response_model=MessageResponse)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    """Delete a budget and all associated data."""
    budget_service.delete_budget(db, budget_id)
    return {"message": f"Budget {budget_id} deleted successfully"}


@router.get("/{budget_id}/summary", response_model=BudgetSummary)
def budget_summary(budget_id: int, db: Session = Depends(get_db)):
    """Get financial summary for a budget."""
    return budget_service.get_budget_summary(db, budget_id)
