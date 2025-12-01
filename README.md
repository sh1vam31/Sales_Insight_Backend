## Sales Insights Backend

Backend service for managing sales data and generating insights, based on the project PRD (`Sales Insights Backend PRD.pdf`).

### 🌐 Live Deployment

**Production API**: [https://sales-insight-backend.onrender.com](https://sales-insight-backend.onrender.com)

- **API Base URL**: `https://sales-insight-backend.onrender.com`
- **Interactive API Docs**: [https://sales-insight-backend.onrender.com/docs](https://sales-insight-backend.onrender.com/docs)
- **ReDoc Documentation**: [https://sales-insight-backend.onrender.com/redoc](https://sales-insight-backend.onrender.com/redoc)

### Tech Stack
- **Framework**: FastAPI  
- **ORM**: SQLAlchemy 2.0 (async)  
- **Validation**: Pydantic v2  
- **Database**: 
  - Development: SQLite (via aiosqlite)
  - Production: PostgreSQL (via asyncpg)

### Project Structure
- `app/main.py` – FastAPI application instance and root route  
- `app/database.py` – SQLAlchemy async engine and session factory  
- `app/models/` – ORM models (Sale model implemented)  
- `app/schemas/` – Pydantic schemas for validation and serialization  
- `app/routes/` – API routers for sales CRUD operations  
- `app/services/` – Business logic and database operations  
- `app/utils/` – Shared utility functions  

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

**Local Development:**
```bash
curl http://localhost:8000/
```

**Production:**
```bash
curl https://sales-insight-backend.onrender.com/
```

Expected response:
```json
{"message": "Sales Insights Backend Running"}
```

#### 2. **Interactive API Documentation (Swagger UI)**
FastAPI automatically generates interactive API documentation:

**Local Development:**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Production:**
- **Swagger UI**: [https://sales-insight-backend.onrender.com/docs](https://sales-insight-backend.onrender.com/docs)
- **ReDoc**: [https://sales-insight-backend.onrender.com/redoc](https://sales-insight-backend.onrender.com/redoc)

These pages show all available endpoints, request/response schemas, and allow you to test APIs directly from the browser.

#### 3. **Test API Endpoints**

**Create a Sale (Production):**
```bash
curl -X POST https://sales-insight-backend.onrender.com/api/sales \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop",
    "quantity": 2,
    "price": 999.99,
    "sale_date": "2024-11-27"
  }'
```

**List All Sales:**
```bash
curl https://sales-insight-backend.onrender.com/api/sales
```

#### 4. **Verify Database Creation (Local Development)**
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
- Database configuration (SQLAlchemy 2.0 async) with PostgreSQL support
- Sale model with all fields, constraints, and indexes
- Pydantic schemas (SaleCreate, SaleUpdate, SaleResponse)
- Complete CRUD API routes for sales management
- Service layer for business logic
- Health check endpoint
- **Deployed to Render** - Production API live at [https://sales-insight-backend.onrender.com](https://sales-insight-backend.onrender.com)

🚧 **In Progress:**
- Insights/analytics API endpoints (total revenue, best-selling products, etc.)

### API Endpoints

All endpoints are prefixed with `/api/sales`:

- `POST /api/sales` - Create a new sale
- `GET /api/sales` - List all sales (with optional filters: `start_date`, `end_date`, `product_name`)
- `GET /api/sales/{sale_id}` - Get a specific sale by ID
- `PUT /api/sales/{sale_id}` - Update a sale
- `DELETE /api/sales/{sale_id}` - Delete a sale

### Deployment

This application is deployed on [Render](https://render.com):
- **Service**: [sales-insight-backend.onrender.com](https://sales-insight-backend.onrender.com)
- **Database**: PostgreSQL (automatically configured via Render)
- **Auto-deploy**: Enabled on push to `sales-review` branch

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

### Development Tips

- The `--reload` flag enables auto-reload on code changes
- Check the terminal for startup logs and any errors
- Database tables are created automatically on first startup
- Use the `/docs` endpoint to explore and test APIs interactively
- For production, the app automatically uses PostgreSQL when `DATABASE_URL` is set


