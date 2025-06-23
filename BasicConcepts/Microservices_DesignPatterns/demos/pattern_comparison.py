#!/usr/bin/env python3
"""
Pattern Comparison Tool – Microservices Design Patterns
=======================================================
A convenience script that *programmatically* showcases each pattern side-by-
side using the in-process simulations found in `implementations/`.

It is **non-interactive** by default––you just pick a menu option and it
prints the highlights so you can see the differences quickly without having
to step through every CLI.
"""

from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Microservices_DesignPatterns/
sys.path.append(str(BASE_DIR / "implementations"))  # allow relative imports

# Import demos lazily inside functions to avoid circular CLI prompts

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def banner() -> None:
    print("\n" + "=" * 80)
    print("📊  MICRO-PATTERN COMPARISON TOOL – QUICK SNAPSHOTS")
    print("=" * 80)


MENU = """
Choose a comparison showcase:
1. Strangler – before vs after route migration
2. SAGA – success vs failure & compensation
3. CQRS – read lag before/after projector sync
4. Exit
"""


# ---------------------------------------------------------------------------
# Strangler showcase
# ---------------------------------------------------------------------------

def show_strangler_demo() -> None:
    from strangler_demo import Controller  # type: ignore

    print("\n🪵  STRANGLER PATTERN DEMO (automated)")
    ctrl = Controller()
    sample_path = "/api/orders"

    print("\n• Initial request (all traffic hits monolith):")
    print(ctrl.handle_request(sample_path))

    print("\n• Migrating /api/orders to order_service …")
    ctrl.add_route("/api/orders", "order_service")

    print("\n• Same request **after** migration:")
    print(ctrl.handle_request(sample_path))

    print("\nRouting table now:")
    ctrl.show_routes()


# ---------------------------------------------------------------------------
# SAGA showcase
# ---------------------------------------------------------------------------

def show_saga_demo() -> None:
    from saga_demo import build_default_orchestrator  # type: ignore

    orch = build_default_orchestrator()

    print("\n🧩  SAGA PATTERN – HAPPY PATH")
    orch.execute(ctx={}, fail_at=None)

    print("\n🧨  SAGA PATTERN – FAILURE AT STEP 3 (payment) with compensation")
    orch.execute(ctx={}, fail_at=3)


# ---------------------------------------------------------------------------
# CQRS showcase
# ---------------------------------------------------------------------------

def show_cqrs_demo() -> None:
    import cqrs_demo as cqrs  # type: ignore

    print("\n🔄  CQRS PATTERN – EVENTUAL CONSISTENCY SNAPSHOT")

    # create a post
    cqrs.cmd_create_post("Hello CQRS", "Initial content")

    post_id = 1  # first event gets id 1

    print("\n• Query *before* projector sync (should be missing):")
    cqrs.query_post(post_id)

    print("\n• Running projector sync …")
    cqrs.project_new_events()

    print("\n• Query *after* projector sync (should be present):")
    cqrs.query_post(post_id)

    print("\n• Updating post content and demonstrating lag …")
    cqrs.cmd_update_post(post_id, "Updated via command side")

    print("\n  – Read immediately (stale):")
    cqrs.query_post(post_id)

    print("\n  – Sync projector again:")
    cqrs.project_new_events()

    print("\n  – Read after sync (fresh):")
    cqrs.query_post(post_id)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    banner()
    while True:
        print(MENU)
        choice = input("🔢  Enter choice: ").strip()
        if choice == "1":
            show_strangler_demo()
        elif choice == "2":
            show_saga_demo()
        elif choice == "3":
            show_cqrs_demo()
        elif choice == "4":
            print("\n👋  Goodbye – explore patterns further via individual demos!")
            break
        else:
            print("❌  Invalid choice, pick 1–4.")
        input("\n⏎  Press Enter to continue…")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n👋  Interrupted.") 