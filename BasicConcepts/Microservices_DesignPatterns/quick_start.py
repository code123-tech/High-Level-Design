#!/usr/bin/env python3
"""
Microservices Design Patterns – Quick Start Guide
------------------------------------------------
This menu-driven script is the central launcher for all hands-on
microservices design-pattern demos contained within this folder.
It mirrors the UX of other *quick_start.py* scripts in the repository
(e.g. CAP_Theorem, ClientServer_P2P).

Run it from the command line:
    python quick_start.py

Menu options will open theory docs or delegate to demo scripts located in
*implementations/* or *demos/* sub-directories.  Most demo scripts are
initially placeholders – feel free to flesh them out over time.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────
MENU: str = """
🚀  MICROSERVICES DESIGN PATTERNS – MAIN MENU

1. Strangler Pattern Demo
2. SAGA Pattern Demo (Orchestration)
3. CQRS Pattern Demo
4. Pattern-Comparison Tool (visual)
5. View Theory (README.md)
6. Explore File Structure
7. Help
8. Exit
"""

BASE_DIR: Path = Path(__file__).parent.resolve()
IMPL_DIR: Path = BASE_DIR / "implementations"
DEMOS_DIR: Path = BASE_DIR / "demos"


# ──────────────────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────────────────

def banner() -> None:
    """Pretty banner shown once at start-up."""
    print("\n" + "=" * 80)
    print("🏗️   MICROSERVICES DESIGN PATTERNS DEMO HUB")
    print("=" * 80)
    print("Experience Strangler, SAGA, CQRS and more through tiny runnable demos!")
    print("=" * 80)


def _launch(script_path: Path) -> None:
    """Run *script_path* via current Python interpreter if it exists."""
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], cwd=str(script_path.parent))
    else:
        rel = script_path.relative_to(BASE_DIR)
        print(f"\n🔧 {rel} not found. Create it to enable this demo.")


def strangler_demo() -> None:
    _launch(IMPL_DIR / "strangler_demo.py")


def saga_demo() -> None:
    _launch(IMPL_DIR / "saga_demo.py")


def cqrs_demo() -> None:
    _launch(IMPL_DIR / "cqrs_demo.py")


def comparison_tool() -> None:
    """Launch a visual comparison / pattern-exploration demo from demos/."""
    _launch(DEMOS_DIR / "pattern_comparison.py")


def view_readme() -> None:
    readme = BASE_DIR / "README.md"
    if sys.platform.startswith("win"):
        os.startfile(readme)  # type: ignore[arg-type]
    elif sys.platform.startswith("darwin"):
        subprocess.run(["open", str(readme)])
    else:
        subprocess.run(["xdg-open", str(readme)])


def explore_structure() -> None:
    print("\n🗂️   PROJECT STRUCTURE (relative to Microservices_DesignPatterns):")
    for root, _dirs, files in os.walk(BASE_DIR):
        level = Path(root).relative_to(BASE_DIR).parts
        indent = "  " * len(level)
        print(f"{indent}{Path(root).name}/")
        subindent = "  " * (len(level) + 1)
        for f in files:
            if f.endswith((".py", ".md")):
                print(f"{subindent}{f}")


def help_text() -> None:
    print(
        """
❓ HELP
-----
This hub lets you:
  • Launch micro-demo simulations for key patterns.
  • Open the theory guide (README.md).
  • Inspect file-tree to understand where to add your own code.

Add your demos under *implementations/* and comparison visualisations under
*demos/*.  Modify this launcher as the project evolves.
"""
    )


# ──────────────────────────────────────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    banner()
    while True:
        print(MENU)
        choice = input("🔢  Enter choice (1-8): ").strip()
        if choice == "1":
            strangler_demo()
        elif choice == "2":
            saga_demo()
        elif choice == "3":
            cqrs_demo()
        elif choice == "4":
            comparison_tool()
        elif choice == "5":
            view_readme()
        elif choice == "6":
            explore_structure()
        elif choice == "7":
            help_text()
        elif choice == "8":
            print("\n👋  Goodbye—happy micro-servicing!")
            break
        else:
            print("❌  Invalid choice. Please select 1–8.")
        input("\n⏎  Press Enter to continue…")


if __name__ == "__main__":
    main() 