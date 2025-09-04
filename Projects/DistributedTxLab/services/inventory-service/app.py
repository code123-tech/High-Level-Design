import asyncio
import contextlib
from datetime import datetime, timezone
from typing import Any, Dict, Tuple

from shared.config import (
    GROUP_INVENTORY,
    PRODUCER_CLIENT_ID,
    KAFKA_BOOTSTRAP_SERVERS,
    SERVICE_NAME,
    TOPIC_INV_EVENTS,
    CONSUMER_CLIENT_ID,
    encode_json,
    saga_partition_key,
    decode_json,
    TOPIC_INV_COMMANDS
)


from fastapi import FastAPI
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer # type: ignore


app = FastAPI(title="inventory-service")
producer: AIOKafkaProducer | None = None # type: ignore
consumer: AIOKafkaConsumer | None = None # type: ignore
consumer_task: asyncio.Task | None = None 

sku_stock: Dict[str, Any] = {"ABC": 5, "XYZ": 3}
reserved_by_saga: Dict[Tuple[str, str], int] = {} # (sagaId, sku) -> quantity

@app.on_event("startup")
async def on_startup() -> None:
    global producer, consumer, consumer_task
    try:
        temp_prod = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id=PRODUCER_CLIENT_ID,
        )
        await temp_prod.start()
        producer = temp_prod
        print(f"[{SERVICE_NAME}] producer started")
    except Exception as exc:
        producer = None
        print(f"[{SERVICE_NAME}] producer start skipped: {exc}")

    try:
        temp_cons = AIOKafkaConsumer(
            TOPIC_INV_COMMANDS,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=GROUP_INVENTORY,
            client_id=CONSUMER_CLIENT_ID,
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )
        await temp_cons.start()
        consumer = temp_cons
        print(f"[{SERVICE_NAME}] consumer started")
        consumer_task = asyncio.create_task(_consumer_loop())
        print(f"[{SERVICE_NAME}] consumer task started with stock: {sku_stock}")
    except Exception as exc:
        consumer = None
        print(f"[{SERVICE_NAME}] consumer start skipped: {exc}")

@app.on_event("shutdown")
async def on_shutdown() -> None:
    global producer, consumer, consumer_task

    if consumer_task:
        consumer_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await consumer_task
    
    if consumer:
        await consumer.stop()
    
    if producer:
        await producer.stop()
    
    print(f"[{SERVICE_NAME}] shutdown complete")

async def _consumer_loop() -> None:
    assert consumer is not None

    async for message in consumer:
        try:
            cmd = decode_json(message.value)
            saga_id = cmd.get('sagaId')
            cmd_type = cmd.get('type')
            order_id = cmd.get('orderId')
            sku = cmd.get('sku')
            quantity = int(cmd.get('quantity', 0))

            if cmd_type == "reserve":
                await handle_reserve(saga_id, order_id, sku, quantity, cmd)
            elif cmd_type == "release":
                await handle_release(saga_id, order_id, sku, quantity, cmd)
        except Exception as e:
            print(f"[{SERVICE_NAME}] error processing message: {e}")

async def handle_reserve(saga_id: str, order_id: str, sku: str, quantity: int, cmd: Dict[str, Any]) -> None:
    
    available = sku_stock.get(sku, 0)

    if available >= quantity and quantity > 0:
        sku_stock[sku] = available - quantity

        reserved_by_saga[(saga_id, sku)] = reserved_by_saga.get((saga_id, sku), 0) + quantity
        event = {
            "sagaId": saga_id,
            "status": "reserved",
            "orderId": order_id,
            "sku": sku,
            "traceId": cmd.get("traceId"),
            "ts": datetime.now(timezone.utc).isoformat()
        }
        await _send(TOPIC_INV_EVENTS, saga_id, event)
        print(f"[{SERVICE_NAME}] reserve {quantity} of {sku} for saga {saga_id} -> stock {sku_stock[sku]}")
    
    else:
        event = {
            "sagaId": saga_id,
            "status": "failed",
            "orderId": order_id,
            "reason": "not enough stock",
            "sku": sku,
            "traceId": cmd.get("traceId"),
            "ts": datetime.now(timezone.utc).isoformat()
        }
        await _send(TOPIC_INV_EVENTS, saga_id, event)
        print(f"[{SERVICE_NAME}] reserve failed for {sku}, need {quantity}, have {available}")

    
async def handle_release(saga_id: str, order_id: str, sku: str, quantity: int, cmd: Dict[str, Any]) -> None:

    reserved = reserved_by_saga.get((saga_id, sku), 0)
    if reserved > 0:
        sku_stock[sku] = sku_stock.get(sku, 0) + reserved
        reserved_by_saga[(saga_id, sku)] = 0
    
    event = {
        "sagaId": saga_id,
        "status": "released",
        "orderId": order_id,
        "sku": sku,
        "traceId": cmd.get("traceId"),
        "ts": datetime.now(timezone.utc).isoformat()
    }

    await _send(TOPIC_INV_EVENTS, saga_id, event)
    print(f"[{SERVICE_NAME}] released {reserved} of {sku} for saga {saga_id} -> stock {sku_stock[sku]}")
    
async def _send(topic: str, saga_id: str, event: Dict[str, Any]) -> None:

    assert producer is not None

    await producer.send_and_wait(
        topic,
        value=encode_json(event),
        key=saga_partition_key(saga_id)
    )

@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"service": "inventory-service", "status": "ok", "stock": sku_stock}
