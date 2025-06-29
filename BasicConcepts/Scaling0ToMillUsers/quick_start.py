#!/usr/bin/env python3
"""
Scaling Journey – Quick Start Launcher
-------------------------------------
Run this script to explore hands-on demos for each scaling milestone
(Single-Server, Split App & DB, Load Balancing, etc.).

Usage:
    python quick_start.py

Each menu entry looks for a corresponding script under *implementations/*
(e.g. implementations/single_server_demo.py).  If the script doesn't exist,
a friendly message is shown so you know what to implement next.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Paths & Constants
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
IMPL_DIR = BASE_DIR / "implementations"
DEMOS_DIR = BASE_DIR / "demos"

MENU = """
🚀  SCALING JOURNEY – MAIN MENU

1. Single-Server Implementation
2. Split App & DB Implementation
3. Load Balancing Implementation
4. Database Replication Implementation
5. Architecture Visualisation Demo
6. View Theory (README.md)
7. Explore File Structure
8. Help
9. Exit
"""

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _banner() -> None:
    print("\n" + "=" * 80)
    print("📈  SCALING JOURNEY DEMO HUB")
    print("=" * 80)
    print("Experiment with incremental architectures as you scale from 0 → 1M users!")
    print("=" * 80)


def _launch(script_path: Path) -> None:
    """Run *script_path* with current Python interpreter if it exists."""
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], cwd=str(script_path.parent))
    else:
        rel = script_path.relative_to(BASE_DIR)
        print(f"\n🔧 Demo '{rel}' not found. Create it to enable this option.")


def _readme_open() -> None:
    readme = BASE_DIR / "README.md"
    if sys.platform.startswith("win"):
        os.startfile(readme)  # type: ignore[arg-type]
    elif sys.platform.startswith("darwin"):
        subprocess.run(["open", str(readme)])
    else:
        subprocess.run(["xdg-open", str(readme)])


def _explore_structure() -> None:
    print("\n🗂️   PROJECT STRUCTURE (relative to Scaling0ToMillUsers):")
    for root, _dirs, files in os.walk(BASE_DIR):
        level = Path(root).relative_to(BASE_DIR).parts
        indent = "  " * len(level)
        print(f"{indent}{Path(root).name}/")
        subindent = "  " * (len(level) + 1)
        for f in files:
            if f.endswith((".py", ".md")):
                print(f"{subindent}{f}")


def _help_text() -> None:
    print(
        """
❓ HELP
-----
This launcher centralises all scaling-journey demos.

Add runnable Python scripts under *implementations/* named:
  • single_server_demo.py
  • split_app_db_demo.py
  • load_balancing_demo.py
  • db_replication_demo.py

Each script should be self-contained and print its own instructions.
"""
    )

# ──────────────────────────────────────────────────────────────────────────────
# Demo dispatchers
# ──────────────────────────────────────────────────────────────────────────────

def _single_server_demo():
    _launch(IMPL_DIR / "single_server_demo.py")

def _split_app_db_demo():
    _launch(IMPL_DIR / "split_app_db_demo.py")

def _load_balancing_demo():
    _launch(IMPL_DIR / "load_balancing_demo.py")

def _db_replication_demo():
    _launch(IMPL_DIR / "db_replication_demo.py")

def _visual_demo():
    """Launch an optional visualisation demo living under *demos/*."""
    _launch(DEMOS_DIR / "architecture_visual.py")

# ──────────────────────────────────────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    _banner()
    while True:
        print(MENU)
        choice = input("🔢  Enter choice (1-9): ").strip()
        if choice == "1":
            _single_server_demo()
        elif choice == "2":
            _split_app_db_demo()
        elif choice == "3":
            _load_balancing_demo()
        elif choice == "4":
            _db_replication_demo()
        elif choice == "5":
            _visual_demo()
        elif choice == "6":
            _readme_open()
        elif choice == "7":
            _explore_structure()
        elif choice == "8":
            _help_text()
        elif choice == "9":
            print("\n👋  Goodbye — happy scaling!")
            break
        else:
            print("❌  Invalid choice. Please select 1–9.")
        input("\n⏎  Press Enter to continue…")


if __name__ == "__main__":
    main() 