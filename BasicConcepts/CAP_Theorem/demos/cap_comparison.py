#!/usr/bin/env python3
"""
cap_comparison.py
=================
Compare CP vs AP demo runs side-by-side in one terminal session.

We import the two demo modules, capture their console output, and then
print them in two columns to highlight the difference:
  • CP rejects writes on minority side (maintains consistency, downtime)
  • AP accepts writes everywhere (stays available, diverges then converges)

Run directly or via quick_start.py menu option 3.
"""

import io
import textwrap
from contextlib import redirect_stdout
from pathlib import Path

# Dynamic import so this file works even if demos move
import importlib.util

BASE_DIR = Path(__file__).resolve().parent.parent / "implementations"


def run_demo(module_name: str):
    """Import module dynamically and capture its main() output as list of lines."""
    spec = importlib.util.spec_from_file_location(module_name, BASE_DIR / f"{module_name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore

    buf = io.StringIO()
    with redirect_stdout(buf):
        if hasattr(mod, "main"):
            mod.main()
        else:
            print(f"Module {module_name} has no main() – nothing to run")
    output = buf.getvalue().splitlines()
    return output


def pad(lines, width):
    return [line.ljust(width) for line in lines]


def side_by_side(left_lines, right_lines, col_width=60):
    max_len = max(len(left_lines), len(right_lines))
    left_lines += [""] * (max_len - len(left_lines))
    right_lines += [""] * (max_len - len(right_lines))

    left_pad = pad(left_lines, col_width)
    result = [f"{l} | {r}" for l, r in zip(left_pad, right_lines)]
    return "\n".join(result)


def main():
    print("\n🔄 CAP COMPARISON TOOL – CP vs AP\n")
    print("Running CP demo …\n")
    cp_output = run_demo("cp_demo")

    print("Running AP demo …\n")
    ap_output = run_demo("ap_demo")

    print("\n📊 Side-by-Side Output (left = CP, right = AP)\n")
    print(side_by_side(cp_output, ap_output))

    print("\nLegend:\n  ✅ WRITE accepted    ❌ WRITE rejected\n  🔄 SYNC/Reconcile    ⚠️  Final note\n")


if __name__ == "__main__":
    main() 