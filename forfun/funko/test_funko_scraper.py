"""Unit tests for funko_scraper."""

import os
import tempfile
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from funko_scraper import (
    build_ebay_sold_url,
    calculate_average_price,
    check_and_handle_challenge,
    contains_keyword,
    fetch_ebay_page_html,
    is_challenge_present,
    is_valid_listing,
    load_possible_keywords,
    parse_listings_from_html,
    parse_price,
    update_funkos_csv,
    OUTPUT_FIELDNAMES,
)




class TestFunkoScraper(unittest.TestCase):

    def setUp(self):
        self.possible_keywords = [
            "glow",
            "flocked",
            "chase",
            "chalice",
            "exclusive",
            "aaa",
            "gamestop",
            "amazon",
            "funkon",
            "hot topic",
            "pre-release",
            "bam",
            "px",
            "box lunch",
            "ee",
            "signed",
        ]

    def test_build_ebay_sold_url(self):
        # Base Funko
        url_base = build_ebay_sold_url("Satoru Gojo", "1114")
        self.assertIn("_nkw=funko+pop+Satoru+Gojo+1114", url_base)
        self.assertIn("LH_Sold=1", url_base)
        self.assertIn("LH_Complete=1", url_base)

        # Variant with keywords
        url_var = build_ebay_sold_url("Kento Nanami", "1490", ["glow", "ee", "exclusive"])
        self.assertIn("_nkw=funko+pop+Kento+Nanami+1490+glow+ee+exclusive", url_var)

    def test_parse_price(self):
        self.assertEqual(parse_price("$15.99"), 15.99)
        self.assertEqual(parse_price("$1,250.00"), 1250.00)
        self.assertEqual(parse_price("USD 24.50"), 24.50)
        # Price range: takes midpoint
        self.assertEqual(parse_price("$10.00 to $20.00"), 15.00)
        self.assertEqual(parse_price("$12.00 - $18.00"), 15.00)
        self.assertIsNone(parse_price(""))
        self.assertIsNone(parse_price("Free Shipping"))

    def test_contains_keyword(self):
        # Direct match
        self.assertTrue(contains_keyword("funko pop glow in the dark", "glow"))
        self.assertTrue(contains_keyword("funko pop gitd chase", "glow"))
        self.assertTrue(contains_keyword("funko pop ee exclusive", "ee"))
        self.assertTrue(contains_keyword("funko pop entertainment earth", "ee"))
        self.assertTrue(contains_keyword("funko pop signed jsa auto", "signed"))

        # Non match
        self.assertFalse(contains_keyword("funko pop satoru gojo", "glow"))
        self.assertFalse(contains_keyword("funko pop see through", "ee"))

    def test_is_valid_listing_base_version(self):
        # Target: Satoru Gojo #1114 (base, no keywords)
        target_name = "Satoru Gojo"
        target_num = "1114"
        target_kw = []

        # Exact base match
        self.assertTrue(
            is_valid_listing(
                "Funko Pop! Jujutsu Kaisen - Satoru Gojo #1114 Vinyl Figure",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )

        # Rejection due to unassigned negative keyword (signed)
        self.assertFalse(
            is_valid_listing(
                "Funko Pop! Satoru Gojo #1114 Signed JSA COA",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )

        # Rejection due to unassigned negative keyword (glow)
        self.assertFalse(
            is_valid_listing(
                "Funko Pop! Satoru Gojo #1114 GITD Glow In The Dark",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )

        # Rejection due to wrong number
        self.assertFalse(
            is_valid_listing(
                "Funko Pop! Satoru Gojo #1120 Vinyl Figure",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )

        # Rejection due to number collision (e.g. 11140)
        self.assertFalse(
            is_valid_listing(
                "Funko Pop! Satoru Gojo #11140 Figure",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )

        # Rejection due to junk/box only
        self.assertFalse(
            is_valid_listing(
                "Funko Pop! Satoru Gojo #1114 Empty Box Only",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )



    def test_is_valid_listing_variant_version(self):
        # Target: Kento Nanami #1490 (glow, ee, exclusive)
        target_name = "Kento Nanami"
        target_num = "1490"
        target_kw = ["glow", "ee", "exclusive"]

        # Valid variant match with aliases
        self.assertTrue(
            is_valid_listing(
                "Funko Pop! Animation Jujutsu Kaisen - Kento Nanami #1490 EE Exclusive GITD",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )

        # Rejection when missing a required positive keyword (missing glow)
        self.assertFalse(
            is_valid_listing(
                "Funko Pop! Animation Jujutsu Kaisen - Kento Nanami #1490 EE Exclusive",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )

        # Rejection when contains another unassigned possible keyword (e.g. chase)
        self.assertFalse(
            is_valid_listing(
                "Funko Pop! Animation - Kento Nanami #1490 EE Exclusive Glow Chase",
                target_name,
                target_num,
                target_kw,
                self.possible_keywords,
            )
        )

    def test_calculate_average_price(self):
        self.assertIsNone(calculate_average_price([]))
        self.assertEqual(calculate_average_price([10.0, 20.0, 30.0]), 20.0)
        # Outlier trimming test (5 items: trims min 5.0 and max 100.0)
        self.assertEqual(calculate_average_price([5.0, 20.0, 22.0, 24.0, 100.0]), 22.0)

    def test_parse_listings_from_html(self):
        sample_html = """
        <li class="s-item">
            <div class="s-item__title"><span>Funko Pop Satoru Gojo 1114</span></div>
            <div class="s-item__details">
                <span class="s-item__price">$12.50</span>
            </div>
        </li>
        <li class="s-item">
            <div class="s-item__title"><span>Shop on eBay</span></div>
            <div class="s-item__details"><span class="s-item__price">$99.00</span></div>
        </li>
        <li class="s-item">
            <div class="s-item__title"><span>Funko Pop Satoru Gojo 1114 Glow</span></div>
            <div class="s-item__details">
                <span class="s-item__price">$35.00</span>
            </div>
        </li>
        """
        listings = parse_listings_from_html(sample_html)
        self.assertEqual(len(listings), 2)
        self.assertEqual(listings[0].title, "Funko Pop Satoru Gojo 1114")
        self.assertEqual(listings[0].price, 12.50)
        self.assertEqual(listings[1].title, "Funko Pop Satoru Gojo 1114 Glow")
        self.assertEqual(listings[1].price, 35.00)

    def test_is_challenge_present(self):
        mock_page = MagicMock()
        mock_page.locator.return_value.count.return_value = 0

        mock_page.title.return_value = "Pardon Our Interruption..."
        self.assertTrue(is_challenge_present(mock_page))

        mock_page.title.return_value = "Security Measure | eBay"
        self.assertTrue(is_challenge_present(mock_page))

        mock_page.title.return_value = "Satoru Gojo 1114 for sale | eBay"
        self.assertFalse(is_challenge_present(mock_page))

        # Captcha iframe fallback
        mock_page.locator.return_value.count.return_value = 1
        self.assertTrue(is_challenge_present(mock_page))

    def test_check_and_handle_challenge(self):
        mock_page = MagicMock()
        mock_page.locator.return_value.count.return_value = 0

        # Case 1: Non-challenge page returns False immediately
        mock_page.title.return_value = "funko pop satoru gojo 1114 | eBay"
        result_normal = check_and_handle_challenge(mock_page, headless=False, prompt_input=False, check_interval=0)
        self.assertFalse(result_normal)

        # Case 2: Challenge initially appears, but disappears during checks -> returns False, no prompt
        mock_page.title.side_effect = [
            "Pardon Our Interruption...",  # initial detection
            "Pardon Our Interruption...",  # check 1
            "funko pop satoru gojo 1114 | eBay",  # check 2 (disappeared!)
        ]
        result_auto_resolved = check_and_handle_challenge(mock_page, headless=False, prompt_input=False, check_interval=0)
        self.assertFalse(result_auto_resolved)

        # Case 3: Challenge persists in headless mode -> prints warning and returns False
        mock_page.title.side_effect = None
        mock_page.title.return_value = "Pardon Our Interruption..."
        result_headless = check_and_handle_challenge(mock_page, headless=True, check_interval=0)
        self.assertFalse(result_headless)

        # Case 4: Challenge persists in headed mode -> prompts user and re-outputs status line
        with patch("builtins.print") as mock_print:
            result_headed = check_and_handle_challenge(
                mock_page,
                headless=False,
                prompt_input=False,
                status_line="[1/5] Scraping: Satoru Gojo #1114 (keywords: '')",
                check_interval=0,
            )
            self.assertTrue(result_headed)
            mock_print.assert_any_call("\n[1/5] Scraping: Satoru Gojo #1114 (keywords: '')")


    def test_fetch_ebay_page_html(self):
        mock_page = MagicMock()
        mock_page.title.return_value = "funko pop satoru gojo 1114 | eBay"
        mock_page.content.return_value = "<html><body><li class='s-item'></li></body></html>"

        html = fetch_ebay_page_html(mock_page, "https://example.com/test", timeout=5, headless=True)
        mock_page.goto.assert_called_once_with("https://example.com/test", wait_until="domcontentloaded", timeout=5000)
        self.assertIn("<li class='s-item'>", html)

    def test_update_funkos_csv_in_place(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = os.path.join(tmp_dir, "funkos.csv")
            kw_path = os.path.join(tmp_dir, "possible_key_words.txt")

            with open(kw_path, "w", encoding="utf-8") as f:
                f.write("glow\nsigned\nchase\n")

            # Row 1 already updated, Row 2 needs update
            initial_csv_content = (
                "category,name,number,key_words,ebay_search_link,ebay_match_count,ebay_avg,last_updated\n"
                "JJK,Satoru Gojo,1114,,https://example.com/existing,10,20.00,2026-01-01\n"
                "MHA,Himiko Toga,2159,,,,,\n"
            )
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                f.write(initial_csv_content)

            sample_html = """
            <li class="s-item">
                <div class="s-item__title"><span>Funko Pop Himiko Toga 2159 Vinyl Figure</span></div>
                <div class="s-item__details"><span class="s-item__price">$25.00</span></div>
            </li>
            """

            with patch("funko_scraper.fetch_ebay_html", return_value=sample_html):
                update_funkos_csv(csv_path, kw_path, dry_run=False, delay=0, use_browser=False)

            with open(csv_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                self.assertEqual(lines[0], ",".join(OUTPUT_FIELDNAMES))
                # Row 1 should be untouched
                self.assertEqual(lines[1], "JJK,Satoru Gojo,1114,,https://example.com/existing,10,20.00,2026-01-01")
                # Row 2 should be updated
                self.assertIn("MHA,Himiko Toga,2159,", lines[2])
                self.assertIn(",1,25,", lines[2])
                self.assertTrue(lines[2].endswith(date.today().isoformat()))

    def test_update_funkos_csv_all_already_updated(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = os.path.join(tmp_dir, "funkos.csv")
            kw_path = os.path.join(tmp_dir, "possible_key_words.txt")

            with open(kw_path, "w", encoding="utf-8") as f:
                f.write("glow\nsigned\nchase\n")

            content = (
                "category,name,number,key_words,ebay_search_link,ebay_match_count,ebay_avg,last_updated\n"
                "JJK,Satoru Gojo,1114,,https://example.com,10,20.00,2026-01-01\n"
            )
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                f.write(content)

            with patch("funko_scraper.fetch_ebay_html") as mock_fetch:
                update_funkos_csv(csv_path, kw_path, dry_run=False, delay=0, use_browser=False)
                mock_fetch.assert_not_called()

    def test_update_funkos_csv_no_matches(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = os.path.join(tmp_dir, "funkos.csv")
            kw_path = os.path.join(tmp_dir, "possible_key_words.txt")

            with open(kw_path, "w", encoding="utf-8") as f:
                f.write("glow\nsigned\nchase\n")

            initial_csv_content = "category,name,number,key_words\nJJK,Satoru Gojo,1114,\n"
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                f.write(initial_csv_content)

            # HTML with no matching listings (different number)
            sample_html = """
            <li class="s-item">
                <div class="s-item__title"><span>Funko Pop Satoru Gojo 9999 Vinyl Figure</span></div>
                <div class="s-item__details"><span class="s-item__price">$50.00</span></div>
            </li>
            """

            with patch("funko_scraper.fetch_ebay_html", return_value=sample_html):
                update_funkos_csv(csv_path, kw_path, dry_run=False, delay=0, use_browser=False)

            with open(csv_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                self.assertEqual(lines[0], ",".join(OUTPUT_FIELDNAMES))
                self.assertTrue(lines[1].endswith(f",0,--,{date.today().isoformat()}"))

    def test_update_funkos_csv_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = os.path.join(tmp_dir, "funkos.csv")
            kw_path = os.path.join(tmp_dir, "possible_key_words.txt")

            with open(kw_path, "w", encoding="utf-8") as f:
                f.write("glow\nsigned\nchase\n")

            initial_content = "category,name,number,key_words\nJJK,Satoru Gojo,1114,\n"
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                f.write(initial_content)

            sample_html = """
            <li class="s-item">
                <div class="s-item__title"><span>Funko Pop Satoru Gojo 1114 Vinyl Figure</span></div>
                <div class="s-item__details"><span class="s-item__price">$14.00</span></div>
            </li>
            """

            with patch("funko_scraper.fetch_ebay_html", return_value=sample_html):
                update_funkos_csv(csv_path, kw_path, dry_run=True, delay=0, use_browser=False)

            with open(csv_path, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), initial_content)

    def test_update_funkos_csv_with_html_fetcher(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = os.path.join(tmp_dir, "funkos.csv")
            kw_path = os.path.join(tmp_dir, "possible_key_words.txt")

            with open(kw_path, "w", encoding="utf-8") as f:
                f.write("glow\nsigned\nchase\n")

            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                f.write("category,name,number,key_words\nJJK,Satoru Gojo,1114,\n")

            sample_html = """
            <li class="s-item">
                <div class="s-item__title"><span>Funko Pop Satoru Gojo 1114 Vinyl Figure</span></div>
                <div class="s-item__details"><span class="s-item__price">$25.00</span></div>
            </li>
            """

            update_funkos_csv(csv_path, kw_path, dry_run=False, delay=0, html_fetcher=lambda url: sample_html)

            with open(csv_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("https://www.ebay.com/sch/i.html?", content)
                self.assertIn(",1,25,", content)
                self.assertIn(date.today().isoformat(), content)


if __name__ == "__main__":
    unittest.main()

