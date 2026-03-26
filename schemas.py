from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from app.models.models import TransactionType


# ──────────────── Budget Schemas ────────────────

class BudgetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    total_limit: Decimal = Field(..., gt=0, decimal_places=2)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    total_limit: Optional[Decimal] = Field(None, gt=0, decimal_places=2)


class BudgetSummary(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    transaction_count: int

    model_config = {"from_attributes": True}


class BudgetResponse(BudgetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BudgetDetailResponse(BudgetResponse):
    summary: Optional[BudgetSummary] = None


# ──────────────── Category Schemas ────────────────

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(default="#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$")
    spending_limit: Optional[Decimal] = Field(None, gt=0, decimal_places=2)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    spending_limit: Optional[Decimal] = Field(None, gt=0, decimal_places=2)


class CategorySpending(BaseModel):
    total_spent: Decimal
    transaction_count: int
    limit_remaining: Optional[Decimal] = None

    model_config = {"from_attributes": True}


class CategoryResponse(CategoryBase):
    id: int
    budget_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CategoryDetailResponse(CategoryResponse):
    spending: Optional[CategorySpending] = None


# ──────────────── Transaction Schemas ────────────────

class TransactionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    type: TransactionType
    note: Optional[str] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    type: Optional[TransactionType] = None
    note: Optional[str] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None


class TransactionResponse(TransactionBase):
    id: int
    budget_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ──────────────── General ────────────────

class MessageResponse(BaseModel):
    message: str


class PaginatedTransactions(BaseModel):
    items: List[TransactionResponse]
    total: int
    page: int
    page_size: int
    pages: int
