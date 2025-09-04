from datetime import datetime, timezone
from typing import Any, Dict
import uuid

from shared.config import (
    PRODUCER_CLIENT_ID,
    KAFKA_BOOTSTRAP_SERVERS,
    SERVICE_NAME,
    TOPIC_ORDERS,
    encode_json,
    saga_partition_key
)


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from aiokafka import AIOKafkaProducer # type: ignore


app = FastAPI(title="order-service")
procuder: AIOKafkaProdcuer = None # type: ignore

class OrderRequest(BaseModel):
    ordeId: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    quantity: int = Field(..., ge = 1)
    amount: float = Field(..., gt = 0)
    currency: str = Field(..., min_length = 3, max_length = 3)


@app.on_event("startup")
async def on_startup() -> None:
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        client_id = PRODUCER_CLIENT_ID
    )
    await producer.start()
    print(f"[{SERVICE_NAME}] producer started")

@app.on_event("shutdown")
async def on_shutdown() -> None:
    global producer
    if procuder:
        await producer.stop()
        print(f"[{SERVICE_NAME}] producer stopped")


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"service" : "order-service", "status" : "healthy"}

@app.post("/orders")
async def create_order(body: OrderRequest) -> Dict[str, Any]:
    
    if producer is None:
        raise HTTPException(status_code=503, detail="Producer not initialized")


    saga_id = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())

    event = {
        "sagaId": saga_id,
        "orderId": body.orderId,
        "sku": body.sku,
        "quantity": body.quantity,
        "amount": body.amount,
        "currency": body.currency,
        "traceId": trace_id,
        "ts": datetime.now(timezone.utc).isoformat()
    }

    await producer.send_and_wait(
        TOPIC_ORDERS,
        value = encode_json(event),
        key=saga_partition_key(saga_id)
    )

    print(f"[{SERVICE_NAME}] published order: {event}")
    return {"sagaId": saga_id, "orderId": body.orderId}
