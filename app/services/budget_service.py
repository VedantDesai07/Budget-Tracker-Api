from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.models import Budget, Transaction, TransactionType
from app.schemas.schemas import BudgetCreate, BudgetUpdate, BudgetSummary
from fastapi import HTTPException


def get_all_budgets(db: Session) -> List[Budget]:
    return db.query(Budget).order_by(Budget.created_at.desc()).all()


def get_budget(db: Session, budget_id: int) -> Budget:
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail=f"Budget {budget_id} not found")
    return budget


def create_budget(db: Session, data: BudgetCreate) -> Budget:
    budget = Budget(**data.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def update_budget(db: Session, budget_id: int, data: BudgetUpdate) -> Budget:
    budget = get_budget(db, budget_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(budget, field, value)
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, budget_id: int) -> None:
    budget = get_budget(db, budget_id)
    db.delete(budget)
    db.commit()


def get_budget_summary(db: Session, budget_id: int) -> BudgetSummary:
    get_budget(db, budget_id)  # ensure exists

    income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.budget_id == budget_id,
        Transaction.type == TransactionType.income
    ).scalar()

    expenses = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.budget_id == budget_id,
        Transaction.type == TransactionType.expense
    ).scalar()

    count = db.query(func.count(Transaction.id)).filter(
        Transaction.budget_id == budget_id
    ).scalar()

    income = Decimal(str(income))
    expenses = Decimal(str(expenses))

    return BudgetSummary(
        total_income=income,
        total_expenses=expenses,
        balance=income - expenses,
        transaction_count=count or 0,
    )
