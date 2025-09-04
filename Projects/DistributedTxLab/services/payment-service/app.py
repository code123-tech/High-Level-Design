import asyncio
import os
import contextlib
from datetime import datetime, timezone
import random
from typing import Any, Dict, Tuple

from shared.config import (
    GROUP_PAYMENT,
    PRODUCER_CLIENT_ID,
    KAFKA_BOOTSTRAP_SERVERS,
    SERVICE_NAME,
    TOPIC_INV_EVENTS,
    CONSUMER_CLIENT_ID,
    TOPIC_PAY_EVENTS,
    encode_json,
    saga_partition_key,
    decode_json,
    TOPIC_PAY_COMMANDS
)


from fastapi import FastAPI
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer # type: ignore

FAILURE_RATE = float(os.getenv("PAYMENT_FAILURE_RATE", "0.3"))

app = FastAPI(title="payment-service")
producer: AIOKafkaProducer | None = None # type: ignore
consumer: AIOKafkaConsumer | None = None # type: ignore
consumer_task: asyncio.Task | None = None 


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
            TOPIC_PAY_COMMANDS,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=GROUP_PAYMENT,
            client_id=CONSUMER_CLIENT_ID,
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )
        await temp_cons.start()
        consumer = temp_cons
        print(f"[{SERVICE_NAME}] consumer started")
        consumer_task = asyncio.create_task(_consumer_loop())
        print(f"[{SERVICE_NAME}] consumer task started with FAILURE_RATE: {FAILURE_RATE}")
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
            order_id = cmd.get('orderId')
            amount = float(cmd.get('amount', 0))
            currency = cmd.get('currency')
            trace_id = cmd.get('traceId')

            if random.random() < FAILURE_RATE:
                event = {
                    "sagaId": saga_id,
                    "status": "failed",
                    "orderId": order_id,
                    "reason": "payment declined",
                    "traceId": trace_id,
                    "ts": datetime.now(timezone.utc).isoformat()
                }
                await _send(TOPIC_PAY_EVENTS, saga_id, event)
                print(f"[{SERVICE_NAME}] payment failed for {order_id} amount {amount} {currency}")
            else:
                event = {
                    "sagaId": saga_id,
                    "status": "paid",
                    "orderId": order_id,
                    "traceId": trace_id,
                    "ts": datetime.now(timezone.utc).isoformat()
                }
                await _send(TOPIC_PAY_EVENTS, saga_id, event)
                print(f"[{SERVICE_NAME}] payment successful for {order_id} amount {amount} {currency}")

        except Exception as e:
            print(f"[{SERVICE_NAME}] error processing payment: {e}")

async def _send(topic: str, saga_id: str, event: Dict[str, Any]) -> None:

    assert producer is not None

    await producer.send_and_wait(
        topic,
        value=encode_json(event),
        key=saga_partition_key(saga_id)
    )

@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"service": "payment-service", "status": "ok", "failureRate": FAILURE_RATE}
