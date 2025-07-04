#!/usr/bin/env python3
"""
SQL vs NoSQL – Quick Start Launcher
----------------------------------
Run this script to explore hands-on demos comparing SQL and NoSQL concepts.

Demos include:
- CRUD operations
- Schema evolution
- Transaction consistency
- Scalability performance
- NEW: Join vs Aggregation (SQL JOIN, MongoDB aggregation, Redis app-side join)

Usage:
    python quick_start.py

Each menu entry auto-discovers scripts under *implementations/*.
If a script doesn't exist, a friendly message is shown so you know what to implement next.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
IMPL_DIR = BASE_DIR / "implementations"

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _banner() -> None:
    print("\n" + "=" * 80)
    print("🗄️  SQL vs NoSQL DEMO HUB")
    print("=" * 80)
    print("Experiment with hands-on demos for SQL and NoSQL concepts!")
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
    print("\n🗂️   PROJECT STRUCTURE (relative to SQL_VS_NOSQL):")
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
This launcher centralises all SQL vs NoSQL demos.

Add runnable Python scripts under *implementations/* (e.g. sql_vs_nosql_crud_demo.py).
Each script should be self-contained and print its own instructions.
"""
    )

# ──────────────────────────────────────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    _banner()
    while True:
        # Auto-discover all .py scripts in implementations/
        demo_scripts = sorted([f for f in IMPL_DIR.glob("*.py") if not f.name.startswith("__")])
        menu = [f"{i+1}. {script.stem.replace('_', ' ').title()}" for i, script in enumerate(demo_scripts)]
        menu.append(f"{len(demo_scripts)+1}. View Theory (README.md)")
        menu.append(f"{len(demo_scripts)+2}. Explore File Structure")
        menu.append(f"{len(demo_scripts)+3}. Help")
        menu.append(f"{len(demo_scripts)+4}. Exit")
        print("\n🗄️  SQL vs NoSQL – MAIN MENU\n")
        for line in menu:
            print(line)
        choice = input(f"\n🔢  Enter choice (1-{len(menu)}): ").strip()
        try:
            idx = int(choice) - 1
        except ValueError:
            idx = -1
        if 0 <= idx < len(demo_scripts):
            _launch(demo_scripts[idx])
        elif idx == len(demo_scripts):
            _readme_open()
        elif idx == len(demo_scripts) + 1:
            _explore_structure()
        elif idx == len(demo_scripts) + 2:
            _help_text()
        elif idx == len(demo_scripts) + 3:
            print("\n👋  Goodbye — happy learning!")
            break
        else:
            print(f"❌  Invalid choice. Please select 1–{len(menu)}.")
        input("\n⏎  Press Enter to continue…")

if __name__ == "__main__":
    main() 