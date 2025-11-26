## Sales Insights Backend

Backend service for managing sales data and generating insights, based on the project PRD (`Sales Insights Backend PRD.pdf`).

### Tech Stack
- **Framework**: FastAPI  
- **ORM**: SQLAlchemy  
- **Validation**: Pydantic v2  

### Project Structure
- `app/main.py` – FastAPI application instance and root route  
- `app/database.py` – SQLAlchemy engine and session factory  
- `app/models/` – ORM models (to be implemented)  
- `app/schemas/` – Pydantic schemas (to be implemented)  
- `app/routes/` – API routers (to be implemented)  
- `app/services/` – Business logic and aggregation (to be implemented)  
- `app/utils/` – Shared utility functions (to be implemented)  

### Installation
```bash
cd sales_insight
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### Running the Server
```bash
uvicorn app.main:app --reload
```

Then open `http://localhost:8000/` to see:
```json
{"message": "Sales Insights Backend Running"}
```


