import asyncio
import contextlib
from datetime import datetime, timezone
from typing import Any, Dict

from shared.config import (
    PRODUCER_CLIENT_ID,
    KAFKA_BOOTSTRAP_SERVERS,
    SERVICE_NAME,
    TOPIC_ORCH_EVENTS,
    TOPIC_ORDERS,
    TOPIC_INV_EVENTS,
    TOPIC_PAY_COMMANDS,
    TOPIC_PAY_EVENTS,
    GROUP_ORCHESTRATOR,
    CONSUMER_CLIENT_ID,
    encode_json,
    saga_partition_key,
    decode_json,
    TOPIC_INV_COMMANDS
)


from fastapi import FastAPI
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer # type: ignore


app = FastAPI(title="orchestrator")
procuder: AIOKafkaProdcuer | None = None # type: ignore
consumer: AIOKafkaConsumer | None = None # type: ignore
consumer_task: asyncio.Task | None = None 

saga_orders: Dict[str, Dict[str, Any]] = {} # order details for initiating payment


@app.on_event("startup")
async def on_startup() -> None:
    global producer, consumer, consumer_task
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        client_id = PRODUCER_CLIENT_ID
    )
    await producer.start()
    print(f"[{SERVICE_NAME}] producer started")

    consumer = AIOKafkaConsumer(
        TOPIC_ORDERS,
        TOPIC_INV_EVENTS,
        TOPIC_PAY_EVENTS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ORCHESTRATOR,
        client_id=CONSUMER_CLIENT_ID,
        enable_auto_commit=True,
        auto_offset_reset="earliest"
    )
    await consumer.start()
    print(f"[{SERVICE_NAME}] consumer started")

    consumer_task = asyncio.create_task(_consumer_loop())
    print(f"[{SERVICE_NAME}] consumer task started")

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
            payload = decode_json(message.value)
            saga_id = payload.get('sagaId')
            if message.topic == TOPIC_ORDERS:
                await _handle_order(saga_id, payload)
            elif message.topic == TOPIC_INV_EVENTS:
                await _handle_inventory_event(saga_id, payload)
            elif message.topic == TOPIC_PAY_EVENTS:
                await _handle_payment_event(saga_id, payload)
        except Exception as e:
            print(f"[{SERVICE_NAME}] error processing message: {e}")

async def _handle_order(saga_id: str, order: Dict[str, Any]) -> None:
    saga_orders[saga_id] = order

    command = {
        "sagaId": saga_id,
        "type": "reserve",
        "orderId": order["orderId"],
        "sku": order["sku"],
        "quantity": order["quantity"],
        "traceId": order["traceId"],
        "ts": datetime.now(timezone.utc).isoformat()
    }

    await _send(TOPIC_INV_COMMANDS, saga_id, command)
    print(f"[{SERVICE_NAME}] order received -> reserve inventory: {command}")
    
async def _handle_inventory_event(saga_id: str, inventory: Dict[str, Any]) -> None:

    status = inventory.get("status")
    order = saga_orders.get(saga_id)

    if status == "failed":
        compensation_event = {
            "sagaId": saga_id,
            "orderId": inventory.get("orderId"),
            "state": "failed",
            "reason": inventory.get("reason", "inventory failed"),
            "traceId": inventory.get("traceId"),
            "ts": datetime.now(timezone.utc).isoformat()
        }

        await _send(TOPIC_ORCH_EVENTS, saga_id, compensation_event)
        print(f"[{SERVICE_NAME}] inventory failed -> saga failed event: {compensation_event}")
        return

    command = {
        "sagaId": saga_id,
        "type": "charge",
        "orderId": order["orderId"],
        "amount": order["amount"],
        "currency": order["currency"],
        "traceId": order["traceId"],
        "ts": datetime.now(timezone.utc).isoformat()
    }

    await _send(TOPIC_PAY_COMMANDS, saga_id, command)
    print(f"[{SERVICE_NAME}] inventory reserved -> charge payment: {command}")
    
async def _handle_payment_event(saga_id: str, payment: Dict[str, Any]) -> None:

    status = payment.get("status")

    if status == "paid":
        final_event = {
            "sagaId": saga_id,
            "orderId": payment.get("orderId"),
            "state": "completed",
            "traceId": payment.get("traceId"),
            "ts": datetime.now(timezone.utc).isoformat()
        }

        await _send(TOPIC_ORCH_EVENTS, saga_id, final_event)
        print(f"[{SERVICE_NAME}] payment successful -> saga completed event: {final_event}")
        saga_orders.pop(saga_id, None)
        return

    # status failed
    order = saga_orders.get(saga_id)
    if order:
        release_cmd = {
            "sagaId": saga_id,
            "type": "release",
            "orderId": order["orderId"],
            "sku": order["sku"],
            "quantity": order["quantity"],
            "traceId": order["traceId"],
            "ts": datetime.now(timezone.utc).isoformat()
        }

        await _send(TOPIC_INV_COMMANDS, saga_id, release_cmd)
        print(f"[{SERVICE_NAME}] payment failed -> release inventory: {release_cmd}")
    
    final_evnet = {
        "sagaId": saga_id,
        "orderId": payment.get("orderId"),
        "state": "failed",
        "reason": payment.get("reason", "payment failed"),
        "traceId": payment.get("traceId"),
        "ts": datetime.now(timezone.utc).isoformat()
    }

    await _send(TOPIC_ORCH_EVENTS, saga_id, final_evnet)
    print(f"[{SERVICE_NAME}] payment failed -> saga failed event: {final_evnet}")
    saga_orders.pop(saga_id, None)


async def _send(topic: str, saga_id: str, event: Dict[str, Any]) -> None:

    assert procuder is not None

    await producer.send_and_wait(
        topic,
        value=encode_json(event),
        key=saga_partition_key(saga_id)
    )

