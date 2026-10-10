"""Helper script to verify or initialize a Funko Pop CSV file."""

from __future__ import annotations

import argparse
import csv
import os
import sys

STANDARD_FIELDNAMES = [
    "category",
    "search_name",
    "name",
    "number",
    "key_words",
    "ebay_avg",
    "ebay_match_count",
    "last_updated",
    "ebay_search_link",
]

REQUIRED_COLUMNS = ["category", "number", "key_words"]


def verify_or_init_csv(csv_path: str, auto_init: bool = True) -> bool:
    """Verify that a CSV file exists and has an acceptable Funko schema, or initialize it."""
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        if auto_init:
            os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(STANDARD_FIELDNAMES)
            print(f"[OK] Initialized new Funko CSV with standard header: {csv_path}")
            return True
        else:
            print(f"[ERROR] File does not exist or is empty: {csv_path}", file=sys.stderr)
            return False

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            header = []

    header_clean = [col.strip().lower() for col in header]

    # Check for name/search_name
    has_name = "search_name" in header_clean or "name" in header_clean
    missing_required = [col for col in REQUIRED_COLUMNS if col not in header_clean]

    if not has_name or missing_required:
        print(f"[ERROR] Invalid Funko CSV header in {csv_path}:", file=sys.stderr)
        if not has_name:
            print("  - Missing name column ('search_name' or 'name')", file=sys.stderr)
        for col in missing_required:
            print(f"  - Missing required column: '{col}'", file=sys.stderr)
        print(f"  Existing columns: {header}", file=sys.stderr)
        return False

    print(f"[OK] Verified valid Funko CSV format: {csv_path} ({len(header)} columns)")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify or initialize Funko CSV file format.")
    parser.add_argument("csv_path", help="Path to Funko CSV file.")
    parser.add_argument(
        "--no-init",
        action="store_true",
        help="Do not automatically initialize empty or missing files.",
    )
    args = parser.parse_args()

    success = verify_or_init_csv(args.csv_path, auto_init=not args.no_init)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
