from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.models import Category, Transaction, TransactionType
from app.schemas.schemas import CategoryCreate, CategoryUpdate, CategorySpending
from app.services.budget_service import get_budget


def get_categories(db: Session, budget_id: int) -> List[Category]:
    get_budget(db, budget_id)
    return db.query(Category).filter(Category.budget_id == budget_id).all()


def get_category(db: Session, budget_id: int, category_id: int) -> Category:
    category = db.query(Category).filter(
        Category.id == category_id, Category.budget_id == budget_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found in budget {budget_id}")
    return category


def create_category(db: Session, budget_id: int, data: CategoryCreate) -> Category:
    get_budget(db, budget_id)
    category = Category(**data.model_dump(), budget_id=budget_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, budget_id: int, category_id: int, data: CategoryUpdate) -> Category:
    category = get_category(db, budget_id, category_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, budget_id: int, category_id: int) -> None:
    category = get_category(db, budget_id, category_id)
    db.delete(category)
    db.commit()


def get_category_spending(db: Session, budget_id: int, category_id: int) -> CategorySpending:
    category = get_category(db, budget_id, category_id)

    total_spent = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.category_id == category_id,
        Transaction.type == TransactionType.expense
    ).scalar()

    count = db.query(func.count(Transaction.id)).filter(
        Transaction.category_id == category_id,
    ).scalar()

    total_spent = Decimal(str(total_spent))
    limit_remaining = None
    if category.spending_limit is not None:
        limit_remaining = Decimal(str(category.spending_limit)) - total_spent

    return CategorySpending(
        total_spent=total_spent,
        transaction_count=count or 0,
        limit_remaining=limit_remaining,
    )
