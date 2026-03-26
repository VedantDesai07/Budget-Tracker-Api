from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import budgets, categories, transactions

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="💰 Budget Tracker API",
    description=(
        "A RESTful API for managing personal budgets, categories, and transactions.\n\n"
        "## Features\n"
        "- 📊 **Budgets** – Create and manage multiple budgets with spending limits\n"
        "- 🏷️ **Categories** – Organize expenses by category with optional caps\n"
        "- 💳 **Transactions** – Record income & expenses with filtering and pagination\n"
        "- 📈 **Summaries** – Real-time balance, income, and expense aggregations\n"
    ),
    version="1.0.0",
    contact={"name": "Budget Tracker", "email": "support@example.com"},
    license_info={"name": "MIT"},
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global error handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred.", "error": str(exc)},
    )


# Routers
app.include_router(budgets.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Budget Tracker API is running 🚀"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
