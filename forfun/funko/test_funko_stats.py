"""Unit tests for funko_stats.py."""

import os
import tempfile
import unittest
from unittest.mock import patch

from funko_stats import (
    FunkoItem,
    FunkoStats,
    calculate_stats,
    format_stats_report,
    load_funko_csv,
    parse_price,
)


class TestParsePrice(unittest.TestCase):
    def test_valid_numbers(self):
        self.assertEqual(parse_price(15), 15.0)
        self.assertEqual(parse_price(15.75), 15.75)
        self.assertEqual(parse_price("23.94"), 23.94)
        self.assertEqual(parse_price("$19.99"), 19.99)
        self.assertEqual(parse_price(" $ 1,250.50 "), 1250.5)
        self.assertEqual(parse_price("0"), 0.0)

    def test_invalid_or_missing(self):
        self.assertIsNone(parse_price(None))
        self.assertIsNone(parse_price(""))
        self.assertIsNone(parse_price("   "))
        self.assertIsNone(parse_price("--"))
        self.assertIsNone(parse_price("-"))
        self.assertIsNone(parse_price("n/a"))
        self.assertIsNone(parse_price("none"))
        self.assertIsNone(parse_price("invalid"))
        self.assertIsNone(parse_price("-10.50"))


class TestFunkoItem(unittest.TestCase):
    def test_display_name_matching(self):
        item = FunkoItem(
            category="JJK",
            search_name="Satoru Gojo",
            box_name="",
            number="1114",
            key_words="",
            price=11.50,
        )
        self.assertEqual(item.display_name, "Satoru Gojo")
        self.assertEqual(item.label, "Satoru Gojo #1114 (JJK)")

    def test_display_name_override(self):
        item = FunkoItem(
            category="AoT",
            search_name="Levi",
            box_name="Captain Levi",
            number="1315",
            key_words="aaa",
            price=20.00,
        )
        self.assertEqual(item.display_name, "Levi (Box: 'Captain Levi')")
        self.assertEqual(item.label, "Levi (Box: 'Captain Levi') #1315 (AoT, kw: 'aaa')")


class TestCalculateStats(unittest.TestCase):
    def test_calculate_stats_basic(self):
        rows = [
            {
                "category": "JJK",
                "search_name": "Satoru Gojo",
                "name": "",
                "number": "1114",
                "key_words": "",
                "ebay_avg": "10.00",
            },
            {
                "category": "MHA",
                "search_name": "Himiko Toga",
                "name": "",
                "number": "2159",
                "key_words": "",
                "ebay_avg": "20.00",
            },
            {
                "category": "AoT",
                "search_name": "Levi",
                "name": "Captain Levi",
                "number": "1315",
                "key_words": "aaa",
                "ebay_avg": "30.00",
            },
        ]
        stats = calculate_stats(rows)
        self.assertIsNotNone(stats)
        self.assertEqual(stats.total_entries, 3)
        self.assertEqual(stats.priced_entries, 3)
        self.assertEqual(stats.unpriced_entries, 0)
        self.assertAlmostEqual(stats.total_value, 60.00)
        self.assertAlmostEqual(stats.average_value, 20.00)
        self.assertAlmostEqual(stats.highest_value, 30.00)
        self.assertAlmostEqual(stats.lowest_value, 10.00)
        self.assertEqual(len(stats.highest_items), 1)
        self.assertEqual(stats.highest_items[0].search_name, "Levi")
        self.assertEqual(len(stats.lowest_items), 1)
        self.assertEqual(stats.lowest_items[0].search_name, "Satoru Gojo")

    def test_calculate_stats_with_unpriced_and_ties(self):
        rows = [
            {
                "category": "JJK",
                "search_name": "Figure A",
                "number": "1",
                "ebay_avg": "10.00",
            },
            {
                "category": "JJK",
                "search_name": "Figure B",
                "number": "2",
                "ebay_avg": "10.00",  # tied low
            },
            {
                "category": "JJK",
                "search_name": "Figure C",
                "number": "3",
                "ebay_avg": "--",     # unpriced
            },
            {
                "category": "JJK",
                "search_name": "Figure D",
                "number": "4",
                "ebay_avg": "",       # unpriced
            },
            {
                "category": "JJK",
                "search_name": "Figure E",
                "number": "5",
                "ebay_avg": "50.00",  # tied high
            },
            {
                "category": "JJK",
                "search_name": "Figure F",
                "number": "6",
                "ebay_avg": "50.00",  # tied high
            },
        ]
        stats = calculate_stats(rows)
        self.assertIsNotNone(stats)
        self.assertEqual(stats.total_entries, 6)
        self.assertEqual(stats.priced_entries, 4)
        self.assertEqual(stats.unpriced_entries, 2)
        self.assertAlmostEqual(stats.total_value, 120.00)
        self.assertAlmostEqual(stats.average_value, 30.00)
        self.assertEqual(len(stats.highest_items), 2)
        self.assertEqual(len(stats.lowest_items), 2)

    def test_calculate_stats_legacy_name_fallback(self):
        rows = [
            {
                "category": "MHA",
                "name": "Deku",
                "number": "596",
                "ebay_avg": "15.00",
            }
        ]
        stats = calculate_stats(rows)
        self.assertIsNotNone(stats)
        self.assertEqual(stats.highest_items[0].search_name, "Deku")

    def test_calculate_stats_empty(self):
        self.assertIsNone(calculate_stats([]))
        self.assertIsNone(calculate_stats([{"ebay_avg": "--"}, {"ebay_avg": ""}]))


class TestFormatStatsReport(unittest.TestCase):
    def test_format_with_stats(self):
        rows = [
            {
                "category": "JJK",
                "search_name": "Satoru Gojo",
                "number": "1114",
                "ebay_avg": "11.50",
            }
        ]
        stats = calculate_stats(rows)
        report = format_stats_report(stats, csv_path="test_funkos.csv")
        self.assertIn("FUNKO POP STATISTICS REPORT", report)
        self.assertIn("File: test_funkos.csv", report)
        self.assertIn("Total Collection Value:  $11.50", report)
        self.assertIn("Average Funko Value:     $11.50", report)
        self.assertIn("Highest Valued Funko ($11.50):", report)
        self.assertIn("Lowest Valued Funko ($11.50):", report)

    def test_format_tied_plural(self):
        rows = [
            {"search_name": "A", "number": "1", "ebay_avg": "10.00"},
            {"search_name": "B", "number": "2", "ebay_avg": "10.00"},
        ]
        stats = calculate_stats(rows)
        report = format_stats_report(stats)
        self.assertIn("Highest Valued Funkos ($10.00):", report)
        self.assertIn("Lowest Valued Funkos ($10.00):", report)

    def test_format_empty_stats(self):
        report = format_stats_report(None, csv_path="empty.csv")
        self.assertIn("No priced Funkos found in this CSV.", report)


class TestLoadCsvAndMain(unittest.TestCase):
    def test_load_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            load_funko_csv("nonexistent_funko_file.csv")

    def test_load_valid_csv(self):
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv") as tmp:
            tmp.write("category,search_name,number,ebay_avg\n")
            tmp.write("JJK,Gojo,1114,12.00\n")
            tmp_path = tmp.name

        try:
            rows = load_funko_csv(tmp_path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["search_name"], "Gojo")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @patch("sys.stdout")
    def test_main_cli(self, mock_stdout):
        from funko_stats import main

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv") as tmp:
            tmp.write("category,search_name,name,number,key_words,ebay_search_link,ebay_match_count,ebay_avg,last_updated\n")
            tmp.write("JJK,Gojo,,1114,,,1,15.50,2026-09-13\n")
            tmp_path = tmp.name

        try:
            with patch("sys.argv", ["funko_stats.py", tmp_path]):
                main()
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
