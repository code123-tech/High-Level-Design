#!/usr/bin/env python3
"""
CAP Theorem Quick Start Guide
----------------------------
Light-weight interactive menu to explore Consistency-Availability-Partition
trade-offs.  Mirrors the UX of other quick_start scripts in this repo but
calls placeholder demos for now.
"""

import os
import sys
import subprocess
from pathlib import Path

MENU = """
🚀 CAP THEOREM LEARNING MENU

1. CP Demo  (Consistency + Partition-tolerance)
2. AP Demo  (Availability + Partition-tolerance)
3. CAP Comparison Tool
4. View Theory (README)
5. Explore File Structure
6. Help
7. Exit
"""

BASE_DIR = Path(__file__).parent.resolve()
IMPL_DIR = BASE_DIR / "implementations"
DEMOS_DIR = BASE_DIR / "demos"


def banner():
    print("\n" + "=" * 80)
    print("⚖️  CAP THEOREM DEMO")
    print("=" * 80)
    print("Understand the trade-offs between Consistency, Availability, and Partition-tolerance!")
    print("=" * 80)


def cp_demo():
    """Launch CP demo stub or real script if present."""
    script = IMPL_DIR / "cp_demo.py"
    if script.exists():
        subprocess.run([sys.executable, str(script)], cwd=str(IMPL_DIR))
    else:
        print("\n🔧 CP demo not implemented yet. Create 'implementations/cp_demo.py' to add it.")


def ap_demo():
    """Launch AP demo stub or real script if present."""
    script = IMPL_DIR / "ap_demo.py"
    if script.exists():
        subprocess.run([sys.executable, str(script)], cwd=str(IMPL_DIR))
    else:
        print("\n🔧 AP demo not implemented yet. Create 'implementations/ap_demo.py' to add it.")


def comparison_tool():
    """Launch visual comparison tool stub or real script if present."""
    script = DEMOS_DIR / "cap_comparison.py"
    if script.exists():
        subprocess.run([sys.executable, str(script)], cwd=str(DEMOS_DIR))
    else:
        print("\n🔧 Comparison tool not implemented yet. Create 'demos/cap_comparison.py' to add it.")


def view_readme():
    readme = BASE_DIR / "README.md"
    if sys.platform.startswith("win"):
        os.startfile(readme)
    elif sys.platform.startswith("darwin"):
        subprocess.run(["open", str(readme)])
    else:
        subprocess.run(["xdg-open", str(readme)])


def explore_structure():
    print("\n🗂️  PROJECT STRUCTURE (relative to CAP_Theorem):")
    for root, dirs, files in os.walk(BASE_DIR):
        level = root.replace(str(BASE_DIR), "").count(os.sep)
        indent = "  " * level
        print(f"{indent}{Path(root).name}/")
        subindent = "  " * (level + 1)
        for f in files:
            if f.endswith((".py", ".md")):
                print(f"{subindent}{f}")


def help_text():
    print("""
❓ HELP
-----
This menu lets you:
  • Launch CP or AP simulation demos (once implemented)
  • Compare outputs side-by-side via the comparison tool
  • Open the theory guide (README.md)
Feel free to add your own code inside the implementations/ & demos/ folders!
""")


def main():
    banner()
    while True:
        print(MENU)
        choice = input("🔢 Enter choice (1-7): ").strip()
        if choice == "1":
            cp_demo()
        elif choice == "2":
            ap_demo()
        elif choice == "3":
            comparison_tool()
        elif choice == "4":
            view_readme()
        elif choice == "5":
            explore_structure()
        elif choice == "6":
            help_text()
        elif choice == "7":
            print("\n👋 Goodbye—explore CAP responsibly!")
            break
        else:
            print("❌ Invalid choice. Please pick 1–7.")
        input("\n⏎  Press Enter to continue...")


if __name__ == "__main__":
    main() 