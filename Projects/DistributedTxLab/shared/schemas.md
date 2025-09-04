# Event contracts

Common fields (present in all messages):
- sagaId: UUID string for partitioning and correlation
- orderId: business identifier
- traceId: optional for observability
- ts: ISO timestamp (producer time)

## orders (produced by order-service)
```json
{ "sagaId": "uuid", "orderId": "o-123", "sku": "ABC", "quantity": 2, "amount": 500, "currency": "USD", "traceId": "uuid", "ts": "2025-01-01T00:00:00Z" }
```

## inventory.commands (consumed by inventory-service)
- type = "reserve" | "release"
```json
{ "sagaId": "uuid", "type": "reserve", "orderId": "o-123", "sku": "ABC", "quantity": 2, "traceId": "uuid", "ts": "..." }
```
```json
{ "sagaId": "uuid", "type": "release", "orderId": "o-123", "sku": "ABC", "quantity": 2, "traceId": "uuid", "ts": "..." }