from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, expenses, categories
from app.routers import auth, expenses, categories, analytics
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="A REST API for tracking personal expenses with user authentication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://bhavanabasavaraj.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(categories.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Expense Tracker API",
        "docs": "Visit /docs for interactive API documentation"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
