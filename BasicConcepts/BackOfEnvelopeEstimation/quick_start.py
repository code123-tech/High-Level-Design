#!/usr/bin/env python3
"""
Back-of-the-Envelope Estimation – Quick Start Launcher
====================================================
Interactive hub to run bite-sized demos that practise common BoE
calculations (traffic, storage, RAM/cache, server count).

Usage:
    python quick_start.py

Each menu entry maps to a script under *implementations/*.
If the script is missing you will see a friendly reminder so you can add it
later.
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
📝  BACK-OF-THE-ENVELOPE – MAIN MENU

1. Traffic/QPS Estimation
2. Storage Estimation
3. RAM/Cache Estimation
4. Server Count Estimation
5. View README (Markdown)
6. Architecture Visual Demo
7. Explore File Structure
8. Help
9. Exit
"""

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _banner() -> None:
    print("\n" + "=" * 80)
    print("📝  BACK-OF-THE-ENVELOPE ESTIMATION DEMO HUB")
    print("=" * 80)
    print("Run quick demos that turn high-level assumptions into rough numbers!")
    print("=" * 80)


def _launch(script_path: Path) -> None:
    """Run *script_path* with current Python interpreter if it exists."""
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], cwd=str(script_path.parent))
    else:
        rel = script_path.relative_to(BASE_DIR)
        print(f"\n🔧 Demo '{rel}' not found. Create it to enable this option.")


def _explore_structure() -> None:
    print("\n🗂️   PROJECT STRUCTURE (relative to BackOfEnvelopeEstimation):")
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
This launcher gathers small calculators that practise back-of-the-envelope
estimation techniques.

Add runnable Python scripts under *implementations/* named:
  • traffic_qps_demo.py
  • storage_estimation_demo.py
  • ram_cache_estimation_demo.py
  • server_estimation_demo.py

Each script should be self-contained and print its own instructions.
"""
    )


def _open_readme() -> None:
    """Open the local README.md in the default viewer."""
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


# ──────────────────────────────────────────────────────────────────────────────
# Demo dispatchers
# ──────────────────────────────────────────────────────────────────────────────

def _traffic_demo():
    _launch(IMPL_DIR / "traffic_qps_demo.py")


def _storage_demo():
    _launch(IMPL_DIR / "storage_estimation_demo.py")


def _ram_demo():
    _launch(IMPL_DIR / "ram_cache_estimation_demo.py")


def _server_demo():
    _launch(IMPL_DIR / "server_estimation_demo.py")


def _visual_demo():
    """Launch the optional architecture visualisation demo."""
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
            _traffic_demo()
        elif choice == "2":
            _storage_demo()
        elif choice == "3":
            _ram_demo()
        elif choice == "4":
            _server_demo()
        elif choice == "5":
            _open_readme()
        elif choice == "6":
            _visual_demo()
        elif choice == "7":
            _explore_structure()
        elif choice == "8":
            _help_text()
        elif choice == "9":
            print("\n👋  Goodbye — happy estimating!")
            break
        else:
            print("❌  Invalid choice. Please select 1–9.")
        input("\n⏎  Press Enter to continue…")


if __name__ == "__main__":
    main() 