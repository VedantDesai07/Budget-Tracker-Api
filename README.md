# 💰 Budget Tracker API

A production-ready REST API for managing personal budgets, categories, and transactions — built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

---

## 📁 Project Structure

```
budget_tracker/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── database.py              # DB engine, session, Base
│   ├── models/
│   │   └── models.py            # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py           # Pydantic request/response schemas
│   ├── routers/
│   │   ├── budgets.py           # /api/v1/budgets endpoints
│   │   ├── categories.py        # /api/v1/budgets/{id}/categories endpoints
│   │   └── transactions.py      # /api/v1/budgets/{id}/transactions endpoints
│   └── services/
│       ├── budget_service.py    # Business logic for budgets
│       ├── category_service.py  # Business logic for categories
│       └── transaction_service.py # Business logic for transactions
├── tests/
│   └── test_api.py              # Full test suite (20 tests)
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
uvicorn app.main:app --reload
```

Server starts at: **http://localhost:8000**

### 3. Explore the API docs

| Interface | URL |
|-----------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

### 4. Run tests

```bash
python -m pytest tests/ -v
```

---

## 📚 API Reference

### 🏦 Budgets  `prefix: /api/v1/budgets`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List all budgets |
| POST | `/` | Create a budget |
| GET | `/{id}` | Get budget + financial summary |
| PUT | `/{id}` | Update a budget |
| DELETE | `/{id}` | Delete budget (cascades) |
| GET | `/{id}/summary` | Income / expense / balance totals |

**Create budget example:**
```json
POST /api/v1/budgets
{
  "name": "Monthly Budget",
  "description": "My April budget",
  "total_limit": 5000.00
}
```

---

### 🏷️ Categories  `prefix: /api/v1/budgets/{budget_id}/categories`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List categories in a budget |
| POST | `/` | Create a category |
| GET | `/{id}` | Get category + spending stats |
| PUT | `/{id}` | Update a category |
| DELETE | `/{id}` | Delete a category |
| GET | `/{id}/spending` | Spending breakdown + limit remaining |

**Create category example:**
```json
POST /api/v1/budgets/1/categories
{
  "name": "Groceries",
  "color": "#22C55E",
  "spending_limit": 400.00
}
```

---

### 💳 Transactions  `prefix: /api/v1/budgets/{budget_id}/transactions`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List transactions (filtered + paginated) |
| POST | `/` | Record a transaction |
| GET | `/{id}` | Get a transaction |
| PUT | `/{id}` | Update a transaction |
| DELETE | `/{id}` | Delete a transaction |

**Query parameters for listing:**

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number (default: 1) |
| `page_size` | int | Items per page (default: 20, max: 100) |
| `type` | string | Filter: `income` or `expense` |
| `category_id` | int | Filter by category |
| `start_date` | datetime | ISO 8601 start date filter |
| `end_date` | datetime | ISO 8601 end date filter |

**Create transaction example:**
```json
POST /api/v1/budgets/1/transactions
{
  "title": "Monthly Salary",
  "amount": 4500.00,
  "type": "income",
  "note": "April paycheck",
  "date": "2024-04-01T09:00:00",
  "category_id": null
}
```

---

## 🗃️ Data Models

```
Budget
  ├── id, name, description, total_limit
  ├── created_at, updated_at
  ├── categories[]
  └── transactions[]

Category
  ├── id, name, color (hex), spending_limit
  ├── budget_id (FK)
  └── transactions[]

Transaction
  ├── id, title, amount, type (income|expense)
  ├── note, date
  ├── budget_id (FK)
  └── category_id (FK, optional)
```

---

## ✅ Test Coverage

```
test_root                           PASSED
test_health                         PASSED
test_create_budget                  PASSED
test_list_budgets                   PASSED
test_get_budget_with_summary        PASSED
test_update_budget                  PASSED
test_delete_budget                  PASSED
test_budget_not_found               PASSED
test_create_category                PASSED
test_list_categories                PASSED
test_category_spending              PASSED
test_delete_category                PASSED
test_create_income_transaction      PASSED
test_create_expense_transaction     PASSED
test_list_transactions_paginated    PASSED
test_filter_by_type                 PASSED
test_update_transaction             PASSED
test_delete_transaction             PASSED
test_invalid_transaction_amount     PASSED
test_transaction_wrong_budget_category PASSED

20 passed in 4.47s
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI 0.115 |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite (swap to PostgreSQL by changing `DATABASE_URL`) |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Tests | Pytest + HTTPX |

---

## 🔌 Switch to PostgreSQL

Change one line in `app/database.py`:

```python
# SQLite (default)
DATABASE_URL = "sqlite:///./budget_tracker.db"

# PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost:5432/budget_db"
```

Then install the driver: `pip install psycopg2-binary`
