# 💰 Expense Tracker API

A REST API for personal expense tracking built with FastAPI and PostgreSQL, featuring JWT authentication and real-time analytics.

![API Documentation](screenshots/swagger-ui.png)

---

## 📌 Overview

This project is a production-ready backend API that allows users to:
- Track income and expenses with categories
- View spending analytics and monthly summaries
- Manage their financial data securely with JWT authentication

Built as part of my journey to master backend development and cloud technologies.

---

## 🛠️ Tech Stack

**Backend Framework:**
- FastAPI 0.104 - Modern Python web framework
- Pydantic - Data validation using Python type hints

**Database:**
- PostgreSQL 14 - Relational database
- SQLAlchemy 2.0 - SQL toolkit and ORM

**Authentication & Security:**
- JWT (python-jose) - Token-based authentication
- Passlib with bcrypt - Password hashing

**Server:**
- Uvicorn - ASGI server for production deployment

---

## ✨ Features

### Core Functionality
- 🔐 **Secure Authentication** - JWT token-based auth with bcrypt password hashing
- 💰 **Expense Management** - Complete CRUD operations for expenses
- 📁 **Category Organization** - Organize expenses by income/expense categories
- 📊 **Analytics Dashboard** - Real-time spending insights and trends

### Technical Highlights
- ✅ 16 RESTful endpoints with proper HTTP status codes
- ✅ Automatic API documentation (Swagger UI)
- ✅ User data isolation (query-level security)
- ✅ Input validation with Pydantic schemas
- ✅ SQL injection protection via ORM
- ✅ Normalized database design (3NF)

---

## 📋 Prerequisites

Before running this project, ensure you have:

- **Python 3.11+** installed
- **PostgreSQL 14+** installed and running
- **pip** (Python package manager)
- **Git** (for cloning the repository)

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/BhavanaBasavaraj/expense-tracker-api.git
cd expense-tracker-api
2. Create virtual environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
bashpip install -r requirements.txt
4. Set up PostgreSQL database
bashcreatedb expense_tracker
5. Configure environment variables
Create a .env file in the project root:
envDATABASE_URL=postgresql://yourusername@localhost/expense_tracker
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
6. Run the application
bashuvicorn app.main:app --reload
The API will be available at http://localhost:8000
View API Documentation: http://localhost:8000/docs

📊 API Endpoints
Authentication

POST /auth/register - Register new user
POST /auth/login - Login and get JWT token
GET /auth/me - Get current user info

Categories

POST /categories/ - Create category
GET /categories/ - Get all categories
GET /categories/{id} - Get specific category
PUT /categories/{id} - Update category
DELETE /categories/{id} - Delete category

Expenses

POST /expenses/ - Create expense
GET /expenses/ - Get all expenses (with pagination)
GET /expenses/{id} - Get specific expense
PUT /expenses/{id} - Update expense
DELETE /expenses/{id} - Delete expense

Analytics

GET /analytics/dashboard - Overall summary (total income, expenses, net balance)
GET /analytics/by-category - Spending breakdown by category
GET /analytics/monthly?months=6 - Monthly summaries (last N months)


🔮 Future Enhancements
Planned features and improvements:
Phase 1: CI/CD & Deployment

 Dockerize the application
 Set up CI/CD pipeline with GitHub Actions
 Deploy to AWS ECS/Fargate
 Infrastructure as Code with Terraform
 Automated testing in pipeline

Phase 2: Microservices Architecture

 Refactor into microservices (Auth, Expense, Analytics services)
 Event-driven communication using AWS SQS
 API Gateway for service orchestration
 Database per service pattern


 🤝 Contributing
This is a personal learning project, but suggestions and feedback are welcome!

👤 Author
Bhavana Basavaraj

GitHub: @BhavanaBasavaraj
LinkedIn: MB Bhavana
Email: bhavanabasavaraj4@gmail.com