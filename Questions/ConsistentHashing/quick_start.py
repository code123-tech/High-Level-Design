#!/usr/bin/env python3
"""
Consistent Hashing – Quick Start Launcher
========================================
Run small simulations that illustrate how consistent hashing behaves.

Usage:
    python quick_start.py

Each menu entry maps to a script under *implementations/*.
If a script is missing, you will see a friendly reminder so you can add it.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
IMPL_DIR = BASE_DIR / "implementations"

MENU = """
🔗 CONSISTENT HASHING – MAIN MENU

1. Load-distribution demo
2. Explore file structure
3. Open README
4. Help
5. Exit
"""

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _banner() -> None:
    print("\n" + "=" * 80)
    print("🔗  CONSISTENT HASHING DEMO HUB")
    print("=" * 80)
    print("Visualise and measure how keys map to servers on a hash ring!")
    print("=" * 80)


def _launch(script_path: Path) -> None:
    """Run *script_path* with current Python interpreter if it exists."""
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], cwd=str(script_path.parent))
    else:
        rel = script_path.relative_to(BASE_DIR)
        print(f"\n🔧 Demo '{rel}' not found. Create it to enable this option.")


def _explore_structure() -> None:
    print("\n🗂️   PROJECT STRUCTURE (relative to ConsistentHashing):")
    for root, _dirs, files in os.walk(BASE_DIR):
        level = Path(root).relative_to(BASE_DIR).parts
        indent = "  " * len(level)
        print(f"{indent}{Path(root).name}/")
        subindent = "  " * (len(level) + 1)
        for f in files:
            if f.endswith((".py", ".md", ".java")):
                print(f"{subindent}{f}")


def _open_readme() -> None:
    md_file = BASE_DIR / "README.md"
    if not md_file.exists():
        print("❌  README.md not found in this folder.")
        return

    if sys.platform.startswith("win"):
        os.startfile(md_file)  # type: ignore[arg-type]
    elif sys.platform.startswith("darwin"):
        subprocess.run(["open", str(md_file)])
    else:
        subprocess.run(["xdg-open", str(md_file)])


def _help_text() -> None:
    print(
        """
❓ HELP
-----
This launcher gathers interactive scripts that demonstrate consistent hashing.

Add runnable Python scripts under *implementations/* named for example:
  • load_distribution_demo.py
  • replication_demo.py
Each script should be self-contained and print its own instructions.
"""
    )


# ──────────────────────────────────────────────────────────────────────────────
# Demo dispatchers
# ──────────────────────────────────────────────────────────────────────────────

def _load_distribution():
    _launch(IMPL_DIR / "load_distribution_demo.py")


# ──────────────────────────────────────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    _banner()
    while True:
        print(MENU)
        choice = input("🔢  Enter choice (1-5): ").strip()
        if choice == "1":
            _load_distribution()
        elif choice == "2":
            _explore_structure()
        elif choice == "3":
            _open_readme()
        elif choice == "4":
            _help_text()
        elif choice == "5":         
            print("\n👋  Goodbye — happy hashing!")
            break
        else:
            print("❌  Invalid choice. Please select 1–5.")
        input("\n⏎  Press Enter to continue…")


if __name__ == "__main__":
    main() 