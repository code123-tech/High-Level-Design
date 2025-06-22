#!/usr/bin/env python3
"""
Strangler Pattern – Interactive Console Demo
===========================================
This lightweight simulation illustrates the **Strangler Fig** migration
pattern used to incrementally replace endpoints of a monolithic application
with new micro-services.

Goals of this demo:
1. Show how a *controller* (a.k.a. facade / API-gateway) routes requests.
2. Gradually migrate individual routes away from the monolith.
3. Observe live traffic flow to confirm the monolith is slowly "strangled".

The entire demo is **in-process** and leverages **only the Python std-lib** to
keep setup friction near zero.  No actual network calls are made – the focus
is on visualising the routing & migration logic.
"""

from __future__ import annotations

import random
import sys
from typing import Callable, Dict

# ──────────────────────────────────────────────────────────────────────────────
# Fake back-end handlers (monolith + micro-services)
# ──────────────────────────────────────────────────────────────────────────────

def monolith_handler(path: str) -> str:
    """Represents the original monolithic application handling *path*."""
    return f"[MONOLITH] 200 OK – response for {path}"


def order_service(path: str) -> str:
    return f"[OrderService] 200 OK – order endpoint {path}"


def inventory_service(path: str) -> str:
    return f"[InventoryService] 200 OK – inventory endpoint {path}"


def payment_service(path: str) -> str:
    return f"[PaymentService] 200 OK – payment endpoint {path}"


# Map service names → handler functions (used when we migrate routes)
SERVICES: Dict[str, Callable[[str], str]] = {
    "monolith": monolith_handler,
    "order_service": order_service,
    "inventory_service": inventory_service,
    "payment_service": payment_service,
}


# ──────────────────────────────────────────────────────────────────────────────
# Controller / Router
# ──────────────────────────────────────────────────────────────────────────────

class Controller:
    """Simple router that forwards paths to handlers based on *route_map*.

    route_map example::
        {
            "/api/orders": "order_service",   # handled by microservice
            "/api/*": "monolith",            # default catch-all
        }
    """

    def __init__(self) -> None:
        # start with everything pointing to monolith
        self.route_map: Dict[str, str] = {"/*": "monolith"}

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def add_route(self, path: str, service_name: str) -> None:
        if service_name not in SERVICES:
            raise ValueError(f"Unknown service '{service_name}'.")
        self.route_map[path] = service_name

    def remove_route(self, path: str) -> None:
        self.route_map.pop(path, None)

    def handle_request(self, path: str) -> str:
        """Return response after routing *path* according to the map."""
        # longest prefix match
        matching = [p for p in self.route_map if path.startswith(p.rstrip("*"))]
        if not matching:
            return "404 Not Found – no route"
        chosen_pattern = max(matching, key=len)  # most specific
        service_name = self.route_map[chosen_pattern]
        handler = SERVICES[service_name]
        return handler(path)

    def show_routes(self) -> None:
        print("\nCurrent Routing Table:")
        for pattern, svc in sorted(self.route_map.items()):
            print(f"  {pattern:<15} → {svc}")


# ──────────────────────────────────────────────────────────────────────────────
# Interactive CLI
# ──────────────────────────────────────────────────────────────────────────────

def print_banner() -> None:
    print("\n" + "=" * 80)
    print("🌳  STRANGLER PATTERN – MIGRATION SIMULATOR")
    print("=" * 80)
    print("Gradually migrate endpoints away from the monolith and watch traffic flow!")
    print("=" * 80)


MENU = """
What would you like to do?
1. Simulate random traffic
2. Migrate an endpoint to a micro-service
3. View routing table
4. Reset to monolith-only
5. Exit
"""

# sample endpoints to generate traffic for demonstration
SAMPLE_PATHS = [
    "/api/orders", "/api/orders/123", "/api/inventory/sku99", "/api/payments",
    "/api/users/42", "/health", "/metrics",
]


def main() -> None:
    ctrl = Controller()
    print_banner()

    while True:
        ctrl.show_routes()
        print(MENU)
        choice = input("🔢  Enter choice (1-5): ").strip()

        if choice == "1":
            path = random.choice(SAMPLE_PATHS)
            print(f"\n➡️  Incoming request: GET {path}")
            print(ctrl.handle_request(path))

        elif choice == "2":
            path = input("Enter endpoint path (e.g. /api/orders): ").strip()
            print("Choose service: order_service | inventory_service | payment_service")
            svc = input("Service name: ").strip()
            try:
                ctrl.add_route(path, svc)
                print(f"✅  Route {path} → {svc} added")
            except ValueError as e:
                print(f"❌  {e}")

        elif choice == "3":
            ctrl.show_routes()

        elif choice == "4":
            ctrl = Controller()  # reset
            print("🔄  Routing table reset – all paths now go to the monolith.")

        elif choice == "5":
            print("\n👋  Exiting Strangler demo. Happy migrating!")
            break
        else:
            print("❌  Invalid choice; pick 1-5.")

        input("\n⏎  Press Enter to continue…")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n👋  Interrupted.") 