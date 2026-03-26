from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.models import Transaction, TransactionType
from app.schemas.schemas import TransactionCreate, TransactionUpdate, PaginatedTransactions
from app.services.budget_service import get_budget
from app.services.category_service import get_category


def get_transactions(
    db: Session,
    budget_id: int,
    page: int = 1,
    page_size: int = 20,
    type_filter: Optional[TransactionType] = None,
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> PaginatedTransactions:
    get_budget(db, budget_id)

    query = db.query(Transaction).filter(Transaction.budget_id == budget_id)

    if type_filter:
        query = query.filter(Transaction.type == type_filter)
    if category_id is not None:
        query = query.filter(Transaction.category_id == category_id)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    total = query.count()
    pages = max(1, -(-total // page_size))  # ceiling division
    items = query.order_by(Transaction.date.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedTransactions(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


def get_transaction(db: Session, budget_id: int, transaction_id: int) -> Transaction:
    txn = db.query(Transaction).filter(
        Transaction.id == transaction_id, Transaction.budget_id == budget_id
    ).first()
    if not txn:
        raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")
    return txn


def create_transaction(db: Session, budget_id: int, data: TransactionCreate) -> Transaction:
    get_budget(db, budget_id)

    if data.category_id is not None:
        get_category(db, budget_id, data.category_id)

    payload = data.model_dump()
    if payload.get("date") is None:
        payload["date"] = datetime.utcnow()

    txn = Transaction(**payload, budget_id=budget_id)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


def update_transaction(db: Session, budget_id: int, transaction_id: int, data: TransactionUpdate) -> Transaction:
    txn = get_transaction(db, budget_id, transaction_id)

    updates = data.model_dump(exclude_none=True)
    if "category_id" in updates and updates["category_id"] is not None:
        get_category(db, budget_id, updates["category_id"])

    for field, value in updates.items():
        setattr(txn, field, value)

    db.commit()
    db.refresh(txn)
    return txn


def delete_transaction(db: Session, budget_id: int, transaction_id: int) -> None:
    txn = get_transaction(db, budget_id, transaction_id)
    db.delete(txn)
    db.commit()
