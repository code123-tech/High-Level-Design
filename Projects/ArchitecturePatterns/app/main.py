from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models, database
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# Initialize FastAPI app
app = FastAPI(title="Architecture Patterns Demo")

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
RESPONSE_TIME = Counter('http_response_time_seconds', 'Response time in seconds')

# Database initialization
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    REQUEST_COUNT.inc()
    return {"message": "Welcome to Architecture Patterns Demo"}

@app.get("/health")
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
def create_item(name: str, db: Session = Depends(get_db)):
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    try:
        item = models.Item(name=name)
        db.add(item)
        db.commit()
        db.refresh(item)
        
        RESPONSE_TIME.inc(time.time() - start_time)
        return item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    items = db.query(models.Item).offset(skip).limit(limit).all()
    RESPONSE_TIME.inc(time.time() - start_time)
    return items 