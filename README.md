# Inventory ML System

**A Machine Learning–Enhanced Inventory Management Web System with Hash-Chained Tamper-Evident Logging**

---

## Overview

This is a full-stack thesis project combining:
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **ML Pipeline**: scikit-learn (demand forecasting, anomaly detection)
- **Audit Trail**: Hash-chained tamper-evident logs
- **Background Jobs**: Celery + Redis
- **Containerization**: Docker + docker-compose

---

## Features

### A) Inventory Management Core
- **Product Management**: SKU, name, category, cost, price, min stock, reorder point, lead time
- **Stock Movements**: Purchase (IN), Sale (OUT), Transfer (MOVE), Adjustment (ADJUST)
- **Multi-Warehouse Support**: Organize inventory by location
- **Search, Filters, Pagination**: Browse and manage thousands of products efficiently
- **CSV Import/Export**: Bulk product and movement operations

### B) Machine Learning Enhancements
1. **Demand Forecasting**
   - Historical analysis of OUT movements per product
   - Multiple algorithms: moving average, linear regression
   - Per-product forecast endpoint: `GET /ml/forecast?product_id=1&horizon=30`
   - Scheduled daily retraining via Celery Beat

2. **Anomaly Detection** (placeholder framework)
   - Identify unusual sale patterns
   - Flag suspicious stock adjustments

3. **Reorder Point Recommendations**
   - Auto-calculated based on lead time + forecast uncertainty

### C) Audit & Compliance
- **Hash-Chained Logs**: Every operation appends a tamper-evident record
- **Immutable Trail**: SHA-256 hash chain prevents tampering
- **Audit API**: Retrieve and verify audit logs
- **Compliance Dashboard**: View all system changes by timestamp

### D) User & Access Control
- **JWT Authentication**: Stateless token-based auth
- **Role-Based Access Control (RBAC)**: Admin, Manager, Staff, Auditor roles
- **Activity Logging**: Track who did what and when

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app + routing
│   │   ├── db.py             # SQLAlchemy config
│   │   ├── models.py         # ORM models (Product, Movement, AuditLog)
│   │   ├── schemas.py        # Pydantic request/response schemas
│   │   ├── crud.py           # CRUD helpers
│   │   ├── auth.py           # JWT helpers
│   │   ├── audit.py          # Hash-chained audit logging
│   │   ├── ml.py             # ML forecast endpoints
│   │   ├── ml_train.py       # Training module (scikit-learn)
│   │   └── api/
│   │       ├── products.py   # Products router
│   │       ├── movements.py  # Movements router
│   │       └── ml.py         # ML training & models router
│   ├── tests/
│   │   ├── conftest.py       # Pytest fixtures
│   │   ├── test_health.py    # Health check test
│   │   └── test_products.py  # Product/movement integration tests
│   ├── celery_worker.py      # Celery tasks + Beat schedule
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Main React app (products + movements demo)
│   │   ├── api.ts            # API client
│   │   ├── main.tsx          # React entry point
│   │   └── index.css         # Tailwind entry
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.cjs
│   ├── postcss.config.cjs
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
├── docker-compose.yml        # Multi-container orchestration
├── pytest.ini
└── README.md (this file)
```

---

## Quick Start

### Prerequisites
- Docker + Docker Compose (recommended for full stack)
- OR Python 3.11+ + Node.js 20+ (for local dev)

### Option 1: Docker Compose (Recommended)

```bash
# Navigate to project root
cd path/to/Thesis

# Start all services (backend, frontend, postgres, redis)
docker-compose up --build

# Services will be available at:
#   Backend:  http://localhost:8000
#   Frontend: http://localhost:5173
#   Postgres: localhost:5432 (postgres/postgres)
#   Redis:    localhost:6379
```

### Option 2: Local Development

#### Backend Setup

```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # on Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt pytest

# Configure environment
cd backend
cp .env .env.local  # adjust DATABASE_URL if using local postgres

# Run database migrations (creates tables)
cd ../
python -m app.main  # or: uvicorn app.main:app --reload

# In another terminal: run tests
pytest backend/tests -v

# Run Celery worker (requires Redis running)
celery -A celery_worker worker -B
```

#### Frontend Setup

```bash
# From frontend/ directory
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## API Endpoints

### Products
- `POST /products/` — Create product
  ```json
  {
    "sku": "PROD-001",
    "name": "Widget A",
    "category": "Electronics",
    "unit_cost": 10.0,
    "selling_price": 25.0,
    "min_stock": 5,
    "reorder_point": 20,
    "lead_time_days": 7
  }
  ```
- `GET /products/` — List products (with pagination)
- `GET /products/{product_id}` — Get product details

### Movements
- `POST /movements/?product_id=1&type=OUT&quantity=5` — Create movement
- `GET /movements/` — List movements

### ML
- `GET /ml/forecast?product_id=1&horizon=30` — Demand forecast for next 30 days
- `POST /ml/train?async_task=true` — Trigger model retraining (Celery task)
- `GET /ml/models` — List trained model artifacts

### Health
- `GET /health` — Health check

---

## Testing

Run the backend test suite:

```bash
cd path/to/Thesis
.venv\Scripts\pytest.exe backend\tests -v  # Windows
pytest backend/tests -v                     # Linux/Mac
```

Expected output:
```
backend/tests/test_health.py::test_health PASSED
backend/tests/test_products.py::test_create_product_and_movement PASSED
```

---

## ML Features in Detail

### Demand Forecasting Pipeline
1. **Data Collection**: Historical OUT movements stored in `movements` table
2. **Training**: Celery task daily loads per-product time series, fits linear regression model
3. **Model Persistence**: Trained models pickled to `backend/models_artifacts/`
4. **Inference**: `/ml/forecast` endpoint loads model + predicts next N days
5. **Retraining**: Scheduled via Celery Beat (daily at 00:00 UTC, configurable)

### Example Forecast Response
```json
{
  "product_id": 1,
  "horizon": 7,
  "moving_average": [5.2, 5.3, 5.1, 5.4, 5.2, 5.3, 5.1],
  "linear_regression": [5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7]
}
```

---

## Audit Trail & Tampering Prevention

Every inventory operation (create product, movement, adjustment) is logged with hash chaining:

```
AuditLog(
  id=1,
  prev_hash=None,
  record_hash="abc123def...",
  data="create_product:1",
  timestamp="2024-01-08T12:00:00"
)

AuditLog(
  id=2,
  prev_hash="abc123def...",
  record_hash="xyz789...",
  data="movement:1:OUT:5",
  timestamp="2024-01-08T12:01:00"
)
```

Each record's hash depends on the previous record's hash, making it impossible to alter past records without breaking the chain.

---

## Development Notes

- **Database**: Default SQLite in dev, PostgreSQL in production (via docker-compose)
- **ML Models**: Stored in `backend/models_artifacts/` as pickle files
- **Environment**: Copy `backend/.env` and customize DATABASE_URL, REDIS_URL, SECRET_KEY
- **CORS**: Frontend can call backend; configured in docker-compose network

---

## Troubleshooting

### Postgres Connection Error
```bash
# Ensure postgres container is running
docker-compose ps

# Check logs
docker-compose logs db
```

### Redis Connection Error
```bash
# Restart Redis
docker-compose restart redis
```

### Frontend Can't Reach Backend
```bash
# Check if backend is running on port 8000
curl http://localhost:8000/health

# Update VITE_API_BASE in frontend/.env if needed
```

### Test Failures
```bash
# Ensure pytest and dependencies installed
pip install -r backend/requirements.txt pytest

# Run with verbose output
pytest backend/tests -vv --tb=long
```

---

## Next Steps / Future Enhancements

1. **Advanced ML**: Add seasonal decomposition, Prophet models, XGBoost
2. **Advanced Anomaly Detection**: Isolation forests, one-class SVM
3. **Real-time Notifications**: WebSocket alerts for low stock
4. **Multi-tenant Support**: Separate data per company/warehouse group
5. **Mobile App**: React Native frontend
6. **Advanced Analytics**: Dashboards, drill-down reports, KPI tracking
7. **Supplier Integration**: API connections to supplier systems
8. **RBAC Refinement**: Fine-grained permissions per warehouse/product category
9. **Backup & Recovery**: Automated PostgreSQL backups, point-in-time recovery
10. **Performance Optimization**: Caching, query optimization, pagination improvements

---

## Author & License

This is a thesis project for MSCS (Master of Science in Computer Science).

---

## Contact & Support

For issues, questions, or feedback on the thesis project, please contact the author or refer to the project documentation.


