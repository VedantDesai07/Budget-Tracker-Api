from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import TransactionType
from app.schemas.schemas import (
    TransactionCreate, TransactionUpdate,
    TransactionResponse, PaginatedTransactions, MessageResponse
)
from app.services import transaction_service

router = APIRouter(prefix="/budgets/{budget_id}/transactions", tags=["Transactions"])


@router.get("", response_model=PaginatedTransactions)
def list_transactions(
    budget_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: Optional[TransactionType] = Query(None),
    category_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    """
    List transactions for a budget with filtering and pagination.

    - **type**: Filter by `income` or `expense`
    - **category_id**: Filter by category
    - **start_date** / **end_date**: Filter by date range (ISO 8601)
    """
    return transaction_service.get_transactions(
        db, budget_id, page, page_size, type, category_id, start_date, end_date
    )


@router.post("", response_model=TransactionResponse, status_code=201)
def create_transaction(budget_id: int, data: TransactionCreate, db: Session = Depends(get_db)):
    """Record a new income or expense transaction."""
    return transaction_service.create_transaction(db, budget_id, data)


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(budget_id: int, transaction_id: int, db: Session = Depends(get_db)):
    """Get a single transaction."""
    return transaction_service.get_transaction(db, budget_id, transaction_id)


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    budget_id: int, transaction_id: int, data: TransactionUpdate, db: Session = Depends(get_db)
):
    """Update a transaction."""
    return transaction_service.update_transaction(db, budget_id, transaction_id, data)


@router.delete("/{transaction_id}", response_model=MessageResponse)
def delete_transaction(budget_id: int, transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction."""
    transaction_service.delete_transaction(db, budget_id, transaction_id)
    return {"message": f"Transaction {transaction_id} deleted successfully"}
