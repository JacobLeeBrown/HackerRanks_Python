"""Funko Pop Collection Statistics Reporter.

Reads a Funko Pop CSV file and reports summary metrics based on the ebay_avg column:
- Total collection value (USD)
- Average Funko value (USD)
- Highest valued Funko(s) (name, number, category, value)
- Lowest valued Funko(s) (name, number, category, value)
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from dataclasses import dataclass
from typing import Any


@dataclass
class FunkoItem:
    category: str
    search_name: str
    box_name: str
    number: str
    key_words: str
    price: float

    @property
    def display_name(self) -> str:
        """Return formatted name including box name override if present."""
        if self.box_name and self.box_name != self.search_name:
            return f"{self.search_name} (Box: '{self.box_name}')"
        return self.search_name or self.box_name

    @property
    def label(self) -> str:
        """Return full label including number, category, and keywords."""
        parts = [f"{self.display_name} #{self.number}"]
        details: list[str] = []
        if self.category:
            details.append(self.category)
        if self.key_words:
            details.append(f"kw: '{self.key_words}'")
        if details:
            parts.append(f"({', '.join(details)})")
        return " ".join(parts)


@dataclass
class FunkoStats:
    total_entries: int
    priced_entries: int
    unpriced_entries: int
    total_value: float
    average_value: float
    highest_value: float
    lowest_value: float
    highest_items: list[FunkoItem]
    lowest_items: list[FunkoItem]


def parse_price(val: Any) -> float | None:
    """Safely parse a price string or float. Return None if invalid or missing."""
    if val is None:
        return None
    val_str = str(val).strip().replace("$", "").replace(",", "")
    if not val_str or val_str in ("--", "-", "n/a", "none"):
        return None
    try:
        price = float(val_str)
        return price if price >= 0 else None
    except ValueError:
        return None


def load_funko_csv(csv_path: str) -> list[dict[str, str]]:
    """Read a Funko CSV into a list of row dictionaries."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def calculate_stats(rows: list[dict[str, str]]) -> FunkoStats | None:
    """Calculate summary statistics from a list of Funko CSV row dicts.

    Returns None if there are no priced Funkos in the rows.
    """
    total_entries = len(rows)
    priced_items: list[FunkoItem] = []
    unpriced_count = 0

    for r in rows:
        price = parse_price(r.get("ebay_avg"))
        if price is None:
            unpriced_count += 1
            continue

        search_name = (r.get("search_name") or r.get("name") or "").strip()
        box_name = (r.get("name") or "").strip()
        number = (r.get("number") or "").strip()
        category = (r.get("category") or "").strip()
        key_words = (r.get("key_words") or "").strip()

        priced_items.append(
            FunkoItem(
                category=category,
                search_name=search_name,
                box_name=box_name,
                number=number,
                key_words=key_words,
                price=price,
            )
        )

    if not priced_items:
        return None

    total_value = sum(item.price for item in priced_items)
    average_value = total_value / len(priced_items)

    max_price = max(item.price for item in priced_items)
    min_price = min(item.price for item in priced_items)

    highest_items = [item for item in priced_items if item.price == max_price]
    lowest_items = [item for item in priced_items if item.price == min_price]

    return FunkoStats(
        total_entries=total_entries,
        priced_entries=len(priced_items),
        unpriced_entries=unpriced_count,
        total_value=total_value,
        average_value=average_value,
        highest_value=max_price,
        lowest_value=min_price,
        highest_items=highest_items,
        lowest_items=lowest_items,
    )


def format_stats_report(stats: FunkoStats | None, csv_path: str = "") -> str:
    """Format the calculated statistics into a readable console string."""
    filename = os.path.basename(csv_path) if csv_path else "Collection"
    lines: list[str] = [
        "=" * 55,
        f"           FUNKO POP STATISTICS REPORT",
        "=" * 55,
        f"File: {filename}",
    ]

    if stats is None:
        lines.extend([
            "",
            "No priced Funkos found in this CSV.",
            "Make sure the 'ebay_avg' column is populated with numeric values.",
            "=" * 55,
        ])
        return "\n".join(lines)

    lines.extend([
        "",
        f"Total Funkos:            {stats.total_entries}",
        f"  - Priced:              {stats.priced_entries}",
        f"  - Unpriced / Pending:  {stats.unpriced_entries}",
        "",
        "-" * 55,
        f"Total Collection Value:  ${stats.total_value:,.2f}",
        f"Average Funko Value:     ${stats.average_value:,.2f}",
        "-" * 55,
        "",
    ])

    # Highest valued
    high_plural = "s" if len(stats.highest_items) > 1 else ""
    lines.append(f"Highest Valued Funko{high_plural} (${stats.highest_value:,.2f}):")
    for item in stats.highest_items:
        lines.append(f"  * {item.label}")

    lines.append("")

    # Lowest valued
    low_plural = "s" if len(stats.lowest_items) > 1 else ""
    lines.append(f"Lowest Valued Funko{low_plural} (${stats.lowest_value:,.2f}):")
    for item in stats.lowest_items:
        lines.append(f"  * {item.label}")

    lines.append("=" * 55)
    return "\n".join(lines)


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_csv = os.path.join(base_dir, "funkos.csv")

    parser = argparse.ArgumentParser(
        description="Report common statistics (average, total, highest, lowest) for Funko Pop CSV files."
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default=None,
        help="Path to the Funko CSV file (default: funkos.csv).",
    )
    parser.add_argument(
        "--csv",
        dest="csv_opt",
        default=None,
        help="Alternative flag to specify path to the Funko CSV file.",
    )

    args = parser.parse_args()
    target_csv = args.csv_opt or args.csv_file or default_csv

    try:
        rows = load_funko_csv(target_csv)
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"Error reading CSV file '{target_csv}': {err}", file=sys.stderr)
        sys.exit(1)

    stats = calculate_stats(rows)
    report = format_stats_report(stats, csv_path=target_csv)
    print(report)


if __name__ == "__main__":
    main()
