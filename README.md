## Sales Insights Backend

Backend service for managing sales data and generating insights, based on the project PRD (`Sales Insights Backend PRD.pdf`).

### Tech Stack
- **Framework**: FastAPI  
- **ORM**: SQLAlchemy 2.0 (async)  
- **Validation**: Pydantic v2  
- **Database**: SQLite (via aiosqlite)

### Project Structure
- `app/main.py` – FastAPI application instance and root route  
- `app/database.py` – SQLAlchemy async engine and session factory  
- `app/models/` – ORM models (Sale model implemented)  
- `app/schemas/` – Pydantic schemas (to be implemented)  
- `app/routes/` – API routers (to be implemented)  
- `app/services/` – Business logic and aggregation (to be implemented)  
- `app/utils/` – Shared utility functions (to be implemented)  

### Installation

1. **Navigate to project directory:**
```bash
cd sales_insight
```

2. **Create virtual environment (optional but recommended):**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Server

**Start the development server:**
```bash
uvicorn app.main:app --reload
```

The server will start on `http://127.0.0.1:8000`

### Testing the Application

#### 1. **Health Check Endpoint**
Open your browser or use curl:
```bash
curl http://localhost:8000/
```

Expected response:
```json
{"message": "Sales Insights Backend Running"}
```

#### 2. **Interactive API Documentation (Swagger UI)**
FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These pages show all available endpoints, request/response schemas, and allow you to test APIs directly from the browser.

#### 3. **Verify Database Creation**
The database file `sales_insights.db` will be created automatically when the server starts. You can verify it exists:
```bash
ls -lh sales_insights.db
```

To inspect the database structure (optional):
```bash
sqlite3 sales_insights.db ".schema sales"
```

### Current Status

✅ **Completed:**
- Project structure setup
- Database configuration (SQLAlchemy 2.0 async)
- Sale model with all fields and indexes
- Root health check endpoint

🚧 **In Progress:**
- Pydantic schemas
- CRUD API routes
- Insights API endpoints

### Development Tips

- The `--reload` flag enables auto-reload on code changes
- Check the terminal for startup logs and any errors
- Database tables are created automatically on first startup
- Use the `/docs` endpoint to explore and test APIs interactively


