#!/usr/bin/env python3
"""
SAGA Pattern – Orchestration Demo
=================================
Simulates a *happy-path* distributed transaction across three micro-services
(Order, Inventory, Payment) and shows how an **orchestrator** coordinates
steps, issuing *compensating* actions if a failure occurs.

Intent: keep everything **in-process & std-lib** so you can play with the
logic without external infra.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from typing import Callable, List

# ──────────────────────────────────────────────────────────────────────────────
# Fake service operations & compensations
# ──────────────────────────────────────────────────────────────────────────────

def order_create(ctx: dict) -> bool:
    ctx["order_id"] = random.randint(1000, 9999)
    print(f"[OrderService] ✅  Order created (id={ctx['order_id']})")
    return True  # success

def order_cancel(ctx: dict) -> None:
    print(f"[OrderService] ↩️  Order {ctx.get('order_id')} cancelled (compensation)")

def inventory_reserve(ctx: dict) -> bool:
    print("[InventoryService] Attempting to reserve items…")
    ctx["inventory_reserved"] = True
    print("[InventoryService] ✅  Items reserved")
    return True

def inventory_release(ctx: dict) -> None:
    if ctx.get("inventory_reserved"):
        print("[InventoryService] ↩️  Released reserved items (compensation)")

def payment_charge(ctx: dict) -> bool:
    print("[PaymentService] Attempting to charge card…")
    ctx["payment_id"] = random.randint(5000, 9000)
    print(f"[PaymentService] ✅  Charge successful (id={ctx['payment_id']})")
    return True

def payment_refund(ctx: dict) -> None:
    if ctx.get("payment_id"):
        print(f"[PaymentService] ↩️  Payment {ctx['payment_id']} refunded (compensation)")

# A registry we can use to refer by name
SERVICES = {
    "OrderService.create": order_create,
    "OrderService.cancel": order_cancel,
    "InventoryService.reserve": inventory_reserve,
    "InventoryService.release": inventory_release,
    "PaymentService.charge": payment_charge,
    "PaymentService.refund": payment_refund,
}


@dataclass
class SagaStep:
    forward: Callable[[dict], bool]
    compensate: Callable[[dict], None]
    name: str


class Orchestrator:
    """Runs saga steps sequentially and triggers compensations on failure."""

    def __init__(self, steps: List[SagaStep]):
        self.steps = steps

    def execute(self, ctx: dict, fail_at: int | None = None) -> None:
        completed: List[SagaStep] = []
        for idx, step in enumerate(self.steps, start=1):
            print(f"\n➡️  STEP {idx}: {step.name}")
            # Simulated failure injection
            if fail_at is not None and idx == fail_at:
                print("💥  Simulated failure before executing step!")
                self._compensate(completed, ctx)
                print("🛑  Saga FAILED – after compensation all systems consistent.")
                return

            ok = step.forward(ctx)
            if ok:
                completed.append(step)
            else:
                print("💥  Step returned failure status.")
                self._compensate(completed, ctx)
                print("🛑  Saga FAILED – after compensation all systems consistent.")
                return

        print("\n🎉  Saga COMPLETED successfully! All steps executed.")

    def _compensate(self, completed_steps: List[SagaStep], ctx: dict) -> None:
        print("\n↩️  Starting COMPENSATION in reverse order…")
        for step in reversed(completed_steps):
            step.compensate(ctx)
        print("↩️  Compensation complete.")


# ──────────────────────────────────────────────────────────────────────────────
# CLI helpers
# ──────────────────────────────────────────────────────────────────────────────

def build_default_orchestrator() -> Orchestrator:
    steps = [
        SagaStep(order_create, order_cancel, "Create Order"),
        SagaStep(inventory_reserve, inventory_release, "Reserve Inventory"),
        SagaStep(payment_charge, payment_refund, "Charge Payment"),
    ]
    return Orchestrator(steps)


MENU = """
SAGA DEMO – choose an option:
1. Run saga (all succeed)
2. Run saga and simulate failure at step 2 (inventory)
3. Run saga and simulate failure at step 3 (payment)
4. Exit
"""

def main() -> None:
    print("\n" + "=" * 80)
    print("📜  SAGA PATTERN DEMO – ORCHESTRATED COMPENSATION")
    print("=" * 80)

    orch = build_default_orchestrator()

    while True:
        print(MENU)
        choice = input("🔢  Enter choice: ").strip()

        if choice == "1":
            orch.execute(ctx={}, fail_at=None)

        elif choice == "2":
            orch.execute(ctx={}, fail_at=2)

        elif choice == "3":
            orch.execute(ctx={}, fail_at=3)

        elif choice == "4":
            print("\n👋  Exiting SAGA demo. Stay consistent!")
            break
        else:
            print("❌  Invalid choice; pick 1-4.")

        input("\n⏎  Press Enter to continue…")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n👋  Interrupted.") 