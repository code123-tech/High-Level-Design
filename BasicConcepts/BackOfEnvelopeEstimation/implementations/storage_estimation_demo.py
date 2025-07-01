#!/usr/bin/env python3
"""
storage_estimation_demo.py
--------------------------
Back-of-the-envelope calculator estimating **daily** storage usage given:
  • Daily Active Users (DAU)
  • Posts per user per day
  • Characters per post (assumes 2 bytes per char)
  • Percentage of users uploading an image & its average size

Run:
    python storage_estimation_demo.py
"""
from __future__ import annotations

CHAR_BYTES = 2  # assume UTF-16 for simple maths
DEFAULT_IMAGE_KB = 300

BYTES_IN_MB = 1024 ** 2
BYTES_IN_GB = 1024 ** 3
BYTES_IN_TB = 1024 ** 4


def _prompt_int(prompt: str, default: int) -> int:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip() or str(default)
        try:
            return int(raw.replace("_", ""))
        except ValueError:
            print("❌  Please enter an integer.")


def _prompt_float(prompt: str, default: float) -> float:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip() or str(default)
        try:
            return float(raw)
        except ValueError:
            print("❌  Please enter a number.")


def _fmt(bytes_: float) -> str:
    if bytes_ >= BYTES_IN_TB:
        return f"{bytes_ / BYTES_IN_TB:.2f} TB"
    if bytes_ >= BYTES_IN_GB:
        return f"{bytes_ / BYTES_IN_GB:.2f} GB"
    return f"{bytes_ / BYTES_IN_MB:.2f} MB"


def main() -> None:  # noqa: D401
    print("\n=== STORAGE ESTIMATOR (DAILY) ===\n")
    dau = _prompt_int("Daily Active Users", 250_000_000)
    posts_per_user = _prompt_int("Posts per user per day", 2)
    chars_per_post = _prompt_int("Characters per post", 250)
    pct_image_uploaders = _prompt_float("% of DAU uploading an image", 10.0)
    image_kb = _prompt_int("Average image size (KB)", DEFAULT_IMAGE_KB)

    # Text storage ----------------------------------------------
    bytes_per_post = chars_per_post * CHAR_BYTES
    text_bytes_daily = dau * posts_per_user * bytes_per_post

    # Image storage ---------------------------------------------
    image_uploaders = dau * (pct_image_uploaders / 100)
    image_bytes_daily = image_uploaders * posts_per_user * image_kb * 1024

    total_bytes_daily = text_bytes_daily + image_bytes_daily

    print("\n--- RESULT (per day) ---")
    print(f"Text data   : {_fmt(text_bytes_daily)}")
    print(f"Image data  : {_fmt(image_bytes_daily)}")
    print("----------------------------")
    print(f"Total       : {_fmt(total_bytes_daily)}")

    years = _prompt_int("\nYears to project storage for", 5)
    total_bytes = total_bytes_daily * 365 * years
    print(f"Projected over {years} year(s): {_fmt(total_bytes)}\n")


if __name__ == "__main__":
    main() 