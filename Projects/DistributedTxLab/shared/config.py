import os
import json
from typing import Dict, Any


def get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value is not None and value.strip() != "" else default

# Kafka Bootstrap servers
KAFKA_BOOTSTRAP_SERVERS: str = get_env("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Topics
TOPIC_ORDERS: str = get_env("TOPIC_ORDERS", "orders")
TOPIC_ORCH_EVENTS: str = get_env("TOPIC_ORCH_EVENTS", "orchestrator.events")
TOPIC_INV_COMMANDS: str = get_env("TOPIC_INV_COMMANDS", "inventory.commands")
TOPIC_INV_EVENTS: str = get_env("TOPIC_INV_EVENTS", "inventory.events")
TOPIC_PAY_COMMANDS: str = get_env("TOPIC_PAY_COMMANDS", "payments.commands")
TOPIC_PAY_EVENTS: str = get_env("TOPIC_PAY_EVENTS", "payment.events")

# Consumer groups
GROUP_ORCHESTRATOR: str = get_env("GROUP_ORCHESTRATOR", "orchestrator-group")
GROUP_INVENTORY: str = get_env("GROUP_INVENTORY", "inventory-group")
GROUP_PAYMENT: str = get_env("GROUP_PAYMENT", "payment-group")

# service identity
SERVICE_NAME: str = get_env("SERVICE_NAME", "unknown-service")

#  Client IDs
PRODUCER_CLIENT_ID: str = get_env("PRODUCER_CLIENT_ID", f"{SERVICE_NAME}-producer")
CONSUMER_CLIENT_ID: str = get_env("CONSUMER_CLIENT_ID", f"{SERVICE_NAME}-consumer")


def encode_json(value: Dict[str, Any]) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def decode_json(value: bytes) -> Dict[str, Any]:
    return json.loads(value.decode("utf-8"))

def saga_partition_key(saga_id: str) -> str:
    return saga_id.encode("utf-8")
