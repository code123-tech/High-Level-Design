from fastapi import FastAPI, HTTPException, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
import time
import logging

from .database import db_manager
from .models import Item

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Active-Passive Architecture Demo")

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency in seconds')
DB_FAILOVER_COUNT = Counter('db_failover_total', 'Total number of database failovers')
PRIMARY_DB_ERRORS = Counter('primary_db_errors_total', 'Total number of primary database errors')

@app.on_event("startup")
async def startup():
    """Initialize the database on startup"""
    db_manager.init_db()

@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
@REQUEST_LATENCY.time()
def health_check():
    """
    Check health of both primary and standby databases
    """
    health_status = {
        "status": "unhealthy",
        "primary_db": "down",
        "standby_db": "down",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Check primary
    if db_manager.check_primary_health():
        health_status["primary_db"] = "up"
    else:
        PRIMARY_DB_ERRORS.inc()

    # Check standby
    if db_manager.check_standby_health():
        health_status["standby_db"] = "up"

    # Overall status
    if health_status["primary_db"] == "up" or health_status["standby_db"] == "up":
        health_status["status"] = "healthy"
    else:
        raise HTTPException(status_code=503, detail="All databases are down")

    return health_status

@app.post("/items/")
@REQUEST_LATENCY.time()
def create_item(name: str, description: Optional[str] = None):
    """
    Create a new item (write operation - always uses primary)
    """
    REQUEST_COUNT.inc()
    try:
        with db_manager.get_write_session() as session:
            item = Item(name=name, description=description)
            session.add(item)
            session.commit()
            session.refresh(item)
            return item.to_dict()
    except SQLAlchemyError as e:
        PRIMARY_DB_ERRORS.inc()
        logger.error(f"Failed to create item: {e}")
        raise HTTPException(status_code=503, detail="Failed to create item")

@app.get("/items/")
@REQUEST_LATENCY.time()
def read_items(skip: int = 0, limit: int = 100):
    """
    Read items (read operation - uses primary with standby fallback)
    """
    REQUEST_COUNT.inc()
    try:
        with db_manager.get_read_session() as session:
            items = session.query(Item).offset(skip).limit(limit).all()
            return {
                "database": "primary" if isinstance(session, db_manager.PrimarySession) else "standby",
                "items": [item.to_dict() for item in items]
            }
    except SQLAlchemyError as e:
        logger.error(f"Failed to read items: {e}")
        raise HTTPException(status_code=503, detail="Failed to read items")

@app.get("/database/status")
@REQUEST_LATENCY.time()
def database_status():
    """
    Get detailed status of both databases
    """
    status = {
        "primary": {
            "status": "healthy" if db_manager.check_primary_health() else "unhealthy",
            "last_checked": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "standby": {
            "status": "healthy" if db_manager.check_standby_health() else "unhealthy",
            "last_checked": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    return status 