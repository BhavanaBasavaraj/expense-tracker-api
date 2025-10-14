from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, expenses, categories
from app.routers import auth, expenses, categories, analytics

# Create all database tables based on models
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Expense Tracker API",
    description="A REST API for tracking personal expenses with user authentication",
    version="1.0.0"
)

# Include routers - organizes endpoints by feature
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(categories.router)
app.include_router(analytics.router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Expense Tracker API",
        "docs": "Visit /docs for interactive API documentation"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
