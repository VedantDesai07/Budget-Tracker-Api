# Budget Tracker API

A REST API for managing personal budgets, categories, and transactions. Built with FastAPI, SQLAlchemy, and SQLite — includes a full test suite and an interactive Swagger UI out of the box.

---

## Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Framework  | FastAPI 0.115       |
| ORM        | SQLAlchemy 2.0      |
| Database   | SQLite              |
| Validation | Pydantic v2         |
| Server     | Uvicorn             |
| Tests      | Pytest + HTTPX      |

---

## Project Structure

```
Budget-Tracker-Api/
├── app/
│   ├── main.py                     # App entry point, CORS, routers
│   ├── database.py                 # DB engine and session
│   ├── models/
│   │   └── models.py               # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py              # Pydantic schemas
│   ├── routers/
│   │   ├── budgets.py              # Budget endpoints
│   │   ├── categories.py           # Category endpoints
│   │   └── transactions.py         # Transaction endpoints
│   └── services/
│       ├── budget_service.py       # Budget business logic
│       ├── category_service.py     # Category business logic
│       └── transaction_service.py  # Transaction business logic
├── tests/
│   └── test_api.py                 # 20 tests
├── index.html                      # Frontend UI
└── requirements.txt
```

---

## Quick Start

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Start the server**

```bash
uvicorn app.main:app --reload
```

Server runs at `http://localhost:8000`

**3. Open the API docs**

| Interface  | URL                         |
|------------|-----------------------------|
| Swagger UI | http://localhost:8000/docs  |
| ReDoc      | http://localhost:8000/redoc |

**4. Run tests**

```bash
python -m pytest tests/ -v
```

---

## API Reference

### Budgets &nbsp;`/api/v1/budgets`

| Method | Path           | Description                        |
|--------|----------------|------------------------------------|
| GET    | `/`            | List all budgets                   |
| POST   | `/`            | Create a budget                    |
| GET    | `/{id}`        | Get budget with financial summary  |
| PUT    | `/{id}`        | Update a budget                    |
| DELETE | `/{id}`        | Delete budget and all related data |
| GET    | `/{id}/summary`| Income / expense / balance totals  |

**Example request:**

```json
POST /api/v1/budgets
{
  "name": "Monthly Budget",
  "description": "April budget",
  "total_limit": 5000.00
}
```

---

### Categories &nbsp;`/api/v1/budgets/{budget_id}/categories`

| Method | Path             | Description                         |
|--------|------------------|-------------------------------------|
| GET    | `/`              | List all categories in a budget     |
| POST   | `/`              | Create a category                   |
| GET    | `/{id}`          | Get category with spending stats    |
| PUT    | `/{id}`          | Update a category                   |
| DELETE | `/{id}`          | Delete a category                   |
| GET    | `/{id}/spending` | Spending breakdown + limit remaining|

**Example request:**

```json
POST /api/v1/budgets/1/categories
{
  "name": "Groceries",
  "color": "#22C55E",
  "spending_limit": 400.00
}
```

---

### Transactions &nbsp;`/api/v1/budgets/{budget_id}/transactions`

| Method | Path    | Description                          |
|--------|---------|--------------------------------------|
| GET    | `/`     | List transactions (filtered + paginated) |
| POST   | `/`     | Create a transaction                 |
| GET    | `/{id}` | Get a single transaction             |
| PUT    | `/{id}` | Update a transaction                 |
| DELETE | `/{id}` | Delete a transaction                 |

**Query parameters:**

| Param         | Type     | Default | Description                   |
|---------------|----------|---------|-------------------------------|
| `page`        | int      | 1       | Page number                   |
| `page_size`   | int      | 20      | Items per page (max 100)      |
| `type`        | string   | —       | Filter: `income` or `expense` |
| `category_id` | int      | —       | Filter by category            |
| `start_date`  | datetime | —       | ISO 8601 start filter         |
| `end_date`    | datetime | —       | ISO 8601 end filter           |

**Example request:**

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

## Data Models

```
Budget
  ├── id, name, description, total_limit
  ├── created_at, updated_at
  ├── categories[]
  └── transactions[]

Category
  ├── id, name, color (hex), spending_limit
  ├── budget_id (FK → Budget)
  └── transactions[]

Transaction
  ├── id, title, amount, type (income | expense)
  ├── note, date
  ├── budget_id (FK → Budget)
  └── category_id (FK → Category, optional)
```

---

## Test Coverage

```
test_root                              PASSED
test_health                            PASSED
test_create_budget                     PASSED
test_list_budgets                      PASSED
test_get_budget_with_summary           PASSED
test_update_budget                     PASSED
test_delete_budget                     PASSED
test_budget_not_found                  PASSED
test_create_category                   PASSED
test_list_categories                   PASSED
test_category_spending                 PASSED
test_delete_category                   PASSED
test_create_income_transaction         PASSED
test_create_expense_transaction        PASSED
test_list_transactions_paginated       PASSED
test_filter_by_type                    PASSED
test_update_transaction                PASSED
test_delete_transaction                PASSED
test_invalid_transaction_amount        PASSED
test_transaction_wrong_budget_category PASSED

20 passed in 4.47s
```

---

## Switch to PostgreSQL

Change one line in `app/database.py`:

```python
# SQLite (default)
DATABASE_URL = "sqlite:///./budget_tracker.db"

# PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost:5432/budget_db"
```

Then install the driver:

```bash
pip install psycopg2-binary
```
