from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models, database
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# Initialize FastAPI app
app = FastAPI(title="Architecture Patterns Demo")

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency in seconds')

# Database initialization
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
@REQUEST_LATENCY.time()  # This decorator automatically tracks request duration
def read_root():
    REQUEST_COUNT.inc()
    return {"message": "Welcome to Architecture Patterns Demo"}

@app.get("/health")
@REQUEST_LATENCY.time()
def health_check(db: Session = Depends(get_db)):
    try:
        # Simple database check using the items table
        db.query(models.Item).first()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Example CRUD endpoints
@app.post("/items/")
@REQUEST_LATENCY.time()
def create_item(name: str, db: Session = Depends(get_db)):
    REQUEST_COUNT.inc()
    try:
        item = models.Item(name=name)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/")
@REQUEST_LATENCY.time()
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    REQUEST_COUNT.inc()
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items 