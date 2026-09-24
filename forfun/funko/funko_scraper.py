"""Funko Pop Market Value Scraper.

Scrapes sold listings on eBay for target Funko Pops defined in funkos.csv,
filters listings using positive and negative keyword matching, calculates
the average USD market value, and updates the CSV file in-place for rows
missing a last_updated date.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable, Sequence

try:
    from playwright.sync_api import Page, sync_playwright, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = None  # type: ignore


OUTPUT_FIELDNAMES = [
    "category",
    "name",
    "number",
    "key_words",
    "ebay_search_link",
    "ebay_match_count",
    "ebay_avg",
    "last_updated",
]


# Common alias dictionary for keywords in possible_key_words.txt
KEYWORD_ALIASES: dict[str, list[str]] = {
    "glow": ["glow", "gitd", "glow in the dark", "glow-in-the-dark"],
    "flocked": ["flocked", "flock"],
    "chase": ["chase"],
    "chalice": ["chalice", "chalice collectibles"],
    "aaa": ["aaa", "aaa anime"],
    "gamestop": ["gamestop", "game stop"],
    "amazon": ["amazon"],
    "funkon": ["funkon"],
    "hot topic": ["hot topic", "hottopic", "ht"],
    "pre-release": ["pre-release", "prerelease", "pre release"],
    "bam": ["bam"],
    "box lunch": ["box lunch", "boxlunch"],
    "ee": ["ee", "entertainment earth"],
    "psa": ["psa", "beckett"],
    "signed": ["signed", "autograph", "autographed"],
}



JUNK_TITLE_PATTERNS = [
    r"\bbox only\b",
    r"\bempty box\b",
    r"\bprotector only\b",
    r"\bdisplay only\b",
    r"\bdisplay case\b",
    r"\bcustom\b",
    r"\blot of\b",
    r"\bmystery box\b",
    r"\bcase only\b",
    r"\breplacement box\b",
    r"\bpop protector\b",
    r"\bmini\b",
    r"\bkeychain\b",
    r"\bpin\b",
    r"\bshirt\b",
    r"\btee\b",
    r"\bsoda\b",
]


@dataclass
class ListingItem:
    title: str
    price: float
    raw_price: str = ""


def load_possible_keywords(file_path: str) -> list[str]:
    """Load reference keywords from possible_key_words.txt."""
    if not os.path.exists(file_path):
        return []
    keywords = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                keywords.append(line.lower())
    return keywords


def build_ebay_sold_url(name: str, number: str, key_words: Sequence[str] = ()) -> str:
    """Construct an eBay sold & completed search URL for a given Funko."""
    query_parts = ["funko", "pop", name.strip(), str(number).strip()]
    for kw in key_words:
        kw_clean = kw.strip()
        if kw_clean:
            query_parts.append(kw_clean)

    query_str = " ".join(query_parts)
    params = {
        "_nkw": query_str,
        "_sacat": "0",
        "_from": "R40",
        "rt": "nc",
        "LH_Sold": "1",
        "LH_Complete": "1",
    }
    return f"https://www.ebay.com/sch/i.html?{urllib.parse.urlencode(params)}"


def parse_price(price_str: str) -> float | None:
    """Parse raw price string into a float value in USD.
    
    Handles formats like '$14.99', '$12.00 to $18.00', 'USD 25.00'.
    """
    if not price_str:
        return None

    cleaned = price_str.replace(",", "")
    # Check for range: '$10.00 to $20.00'
    range_match = re.search(r"\$?\s*(\d+(?:\.\d+)?)\s*(?:to|-)\s*\$?\s*(\d+(?:\.\d+)?)", cleaned, re.IGNORECASE)
    if range_match:
        p1 = float(range_match.group(1))
        p2 = float(range_match.group(2))
        return round((p1 + p2) / 2.0, 2)

    single_match = re.search(r"\$?\s*(\d+(?:\.\d+)?)", cleaned)
    if single_match:
        val = float(single_match.group(1))
        if val > 0:
            return val
    return None


def contains_keyword(text: str, keyword: str) -> bool:
    """Check if a normalized text contains the keyword or any of its aliases."""
    kw_norm = keyword.strip().lower()
    aliases = KEYWORD_ALIASES.get(kw_norm, [kw_norm])
    
    for alias in aliases:
        # Check boundary match
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def is_valid_listing(
    title: str,
    name: str,
    number: str,
    target_keywords: Sequence[str],
    all_possible_keywords: Sequence[str],
) -> bool:
    """Evaluate whether an eBay listing title matches the exact target Funko."""
    title_lower = title.lower()

    # 1. Filter junk / non-figurine listings
    for junk_pattern in JUNK_TITLE_PATTERNS:
        if re.search(junk_pattern, title_lower):
            return False

    # 2. Check number match (e.g. #1114 or 1114 as word)
    number_str = str(number).strip()
    num_pattern = r"(?:^|\D)" + re.escape(number_str) + r"(?:\D|$)"
    if not re.search(num_pattern, title_lower):
        return False

    # 3. Check name tokens match (all significant words of the name should match)
    # Split name words (ignore punctuation)
    name_words = [w.lower() for w in re.findall(r"[a-zA-Z0-9]+", name) if len(w) > 1]
    for w in name_words:
        if w not in title_lower:
            return False

    # 4. Check positive keywords: all target keywords must be present
    target_kw_set = {kw.strip().lower() for kw in target_keywords if kw.strip()}
    for kw in target_kw_set:
        if not contains_keyword(title_lower, kw):
            return False

    # 5. Check negative keywords: any possible keyword NOT in target_kw_set must NOT be present
    for kw in all_possible_keywords:
        kw_norm = kw.strip().lower()
        if kw_norm not in target_kw_set:
            if contains_keyword(title_lower, kw_norm):
                return False

    return True




def get_http_session():
    """Create or return a requests Session with browser-like headers if available."""
    try:
        import requests
        session = requests.Session()
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.ebay.com/",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        })
        return session
    except ImportError:
        return None


GLOBAL_SESSION = None


def fetch_ebay_html(url: str, timeout: int = 15) -> str:
    """Fetch raw HTML for an eBay URL with standard browser headers."""
    global GLOBAL_SESSION
    if GLOBAL_SESSION is None:
        GLOBAL_SESSION = get_http_session()

    if GLOBAL_SESSION is not None:
        resp = GLOBAL_SESSION.get(url, timeout=timeout)
        if resp.status_code == 200:
            return resp.text

    # Fallback to urllib if requests is unavailable or fails
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")


def parse_listings_from_html(html: str) -> list[ListingItem]:
    """Extract listing items with titles and prices from eBay HTML."""
    listings: list[ListingItem] = []

    # Attempt BeautifulSoup parsing if available
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".s-item, .s-card")
        for item in items:
            title_el = item.select_one(".s-item__title, .s-card__title, span[role='heading']")
            price_el = item.select_one(".s-item__price, .s-card__price")
            if title_el and price_el:
                title = title_el.get_text(strip=True)
                raw_price = price_el.get_text(strip=True)
                if not title or "Shop on eBay" in title:
                    continue
                price = parse_price(raw_price)
                if price is not None:
                    listings.append(ListingItem(title=title, price=price, raw_price=raw_price))
        if listings:
            return listings
    except ImportError:
        pass

    # Fallback to regex pattern matching on eBay DOM structure
    item_blocks = re.findall(r'<li class="s-item[^"]*"[^>]*>(.*?)</li>', html, re.DOTALL)
    if not item_blocks:
        item_blocks = re.findall(r'<div class="s-item__info[^"]*"[^>]*>(.*?)</div>\s*</div>', html, re.DOTALL)

    for block in item_blocks:
        title_m = re.search(r'class="s-item__title"[^>]*>(?:<span[^>]*>)?(.*?)(?:</span>)?</div>', block, re.DOTALL)
        if not title_m:
            title_m = re.search(r'<span role="heading"[^>]*>(.*?)</span>', block, re.DOTALL)
            
        price_m = re.search(r'class="s-item__price"[^>]*>(?:<span[^>]*>)?(.*?)(?:</span>)?</span>', block, re.DOTALL)

        if title_m and price_m:
            title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip()
            raw_price = re.sub(r"<[^>]+>", "", price_m.group(1)).strip()
            if not title or "Shop on eBay" in title:
                continue
            price = parse_price(raw_price)
            if price is not None:
                listings.append(ListingItem(title=title, price=price, raw_price=raw_price))

    return listings


def calculate_average_price(prices: Sequence[float]) -> float | None:
    """Calculate the average price from a list of valid prices.
    
    If at least 5 prices exist, trims top/bottom extremes (10% trimmed mean)
    to protect against outliers.
    """
    if not prices:
        return None

    cleaned_prices = sorted(prices)
    if len(cleaned_prices) >= 5:
        # Trim 1 lowest and 1 highest for small sets, or 10%
        trim_count = max(1, int(len(cleaned_prices) * 0.1))
        trimmed = cleaned_prices[trim_count:-trim_count]
        if trimmed:
            cleaned_prices = trimmed

    avg = sum(cleaned_prices) / len(cleaned_prices)
    return round(avg, 2)


def is_challenge_present(page: Any) -> bool:
    """Check if the page currently shows a challenge or interruption indicator."""
    try:
        title = page.title()
    except Exception:
        return False
    challenge_indicators = [
        "pardon our interruption",
        "security measure",
        "captcha",
        "robot",
        "verify you are a human",
    ]
    if any(ind in title.lower() for ind in challenge_indicators):
        return True
    try:
        if page.locator("iframe[src*='captcha'], div#captcha_container, div.captcha").count() > 0:
            return True
    except Exception:
        pass
    return False


def check_and_handle_challenge(
    page: Any,
    headless: bool = False,
    prompt_input: bool = True,
    status_line: str | None = None,
    max_checks: int = 3,
    check_interval: float = 1.0,
) -> bool:
    """Detect eBay anti-bot verification challenge and prompt user to resolve if headed.

    If the page initially shows an interruption screen, performs up to max_checks
    in check_interval intervals to see if the page automatically transitions away.
    Only prompts the user if the challenge remains after those checks.
    """
    if is_challenge_present(page):
        # Do 3 checks in 1 second intervals for the page to disappear
        for _ in range(max_checks):
            if check_interval > 0:
                time.sleep(check_interval)
            if not is_challenge_present(page):
                return False

        title = page.title()
        if headless:
            print(f"\n[WARNING] eBay displayed a bot verification challenge in headless mode ('{title.strip()}').")
            print("          Run without --headless to solve it in a visible browser.")
            return False

        print(f"\n{'=' * 65}")
        print(f"[!] ACTION REQUIRED: eBay challenge detected ('{title.strip()}')")
        print("    Please complete the verification challenge in the browser window.")
        print(f"{'=' * 65}")
        if prompt_input:
            input("    Press [Enter] after completing the challenge...")
            try:
                page.wait_for_load_state("domcontentloaded", timeout=15000)
            except Exception:
                pass
            if "pardon our interruption" in page.title().lower() or "security measure" in page.title().lower():
                try:
                    page.reload(wait_until="domcontentloaded", timeout=15000)
                except Exception:
                    pass
        if status_line:
            print(f"\n{status_line}")
        return True
    return False


def fetch_ebay_page_html(
    page: Any,
    url: str,
    timeout: int = 30,
    headless: bool = False,
    status_line: str | None = None,
) -> str:
    """Navigate to an eBay URL using a Playwright Page and return rendered HTML."""
    page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
    check_and_handle_challenge(page, headless=headless, status_line=status_line)

    # Wait briefly for listings or no-results banner to appear
    try:
        page.wait_for_selector(
            ".s-item, .s-card, .srp-save-null-search, .srp-river-answer--NO_EXACT_MATCH",
            timeout=8000,
        )
    except Exception:
        pass

    return page.content()


def scrape_funko_average(
    name: str,
    number: str,
    key_words_str: str,
    all_possible_keywords: Sequence[str],
    page: Any | None = None,
    html_fetcher: Callable[[str], str] | None = None,
    timeout: int = 30,
    headless: bool = False,
    status_line: str | None = None,
) -> tuple[str, float | None, list[ListingItem]]:
    """Scrape sold listings for a single Funko and return (search_url, avg_price, matched_listings)."""
    target_keywords = [k.strip() for k in key_words_str.split(",") if k.strip()]
    url = build_ebay_sold_url(name, number, target_keywords)

    if html_fetcher is not None:
        html = html_fetcher(url)
    elif page is not None:
        html = fetch_ebay_page_html(
            page,
            url,
            timeout=timeout,
            headless=headless,
            status_line=status_line,
        )
    else:
        html = fetch_ebay_html(url, timeout=timeout)

    raw_listings = parse_listings_from_html(html)

    matched = [
        item for item in raw_listings
        if is_valid_listing(item.title, name, number, target_keywords, all_possible_keywords)
    ]

    prices = [item.price for item in matched]
    avg_price = calculate_average_price(prices)
    return url, avg_price, matched



def update_funkos_csv(
    csv_path: str,
    keywords_path: str,
    dry_run: bool = False,
    headless: bool = False,
    delay: float = 2.0,
    user_data_dir: str | None = None,
    use_browser: bool = True,
    html_fetcher: Callable[[str], str] | None = None,
) -> None:
    """Process funkos.csv, fetch sold data for un-updated rows, and update in-place."""
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    all_possible_keywords = load_possible_keywords(keywords_path)

    rows: list[dict[str, str]] = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        for col in OUTPUT_FIELDNAMES:
            if col not in fieldnames:
                fieldnames.append(col)
        for r in reader:
            rows.append(r)

    rows_to_scrape = [
        r for r in rows
        if r.get("name", "").strip()
        and r.get("number", "").strip()
        and not r.get("last_updated", "").strip()
    ]

    print(f"Loaded {len(rows)} Funko entries from {csv_path} ({len(rows_to_scrape)} pending update)...")

    if not rows_to_scrape:
        print("All entries already have 'last_updated' values. Nothing to scrape.")
        return

    def _process_all(page_obj: Any | None = None, fetcher_fn: Callable[[str], str] | None = None) -> None:
        today_str = date.today().isoformat()
        scraped_count = 0
        for row in rows:
            name = row.get("name", "").strip()
            number = row.get("number", "").strip()
            kw_str = row.get("key_words", "").strip()
            last_updated = row.get("last_updated", "").strip()

            if not name or not number or last_updated:
                continue

            scraped_count += 1
            status_line = f"[{scraped_count}/{len(rows_to_scrape)}] Scraping: {name} #{number} (keywords: '{kw_str}')"
            print(f"\n{status_line}")

            search_url = build_ebay_sold_url(
                name, number, [k.strip() for k in kw_str.split(",") if k.strip()]
            )
            match_count = 0
            avg_formatted = "--"

            try:
                url, avg_price, matched = scrape_funko_average(
                    name=name,
                    number=number,
                    key_words_str=kw_str,
                    all_possible_keywords=all_possible_keywords,
                    page=page_obj,
                    html_fetcher=fetcher_fn,
                    headless=headless,
                    status_line=status_line,
                )
                search_url = url
                match_count = len(matched)
                if avg_price is not None and match_count > 0:
                    avg_formatted = str(int(avg_price)) if avg_price.is_integer() else f"{avg_price:.2f}"
                    print(f"  Matched {match_count} sold listings. Calculated average: ${avg_formatted}")
                else:
                    avg_formatted = "--"
                    print("  No valid matching listings found. Setting average to '--'")

            except Exception as e:
                print(f"  Error fetching listings: {e}")

            row["ebay_search_link"] = search_url
            row["ebay_match_count"] = str(match_count)
            row["ebay_avg"] = avg_formatted
            row["last_updated"] = today_str

            if scraped_count < len(rows_to_scrape) and delay > 0:
                time.sleep(delay)

    if html_fetcher is not None or not use_browser:
        _process_all(fetcher_fn=html_fetcher)
    else:
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError(
                "Playwright is not installed. Run 'pip install playwright && playwright install chromium' "
                "or pass use_browser=False to use fallback HTTP fetching."
            )

        profile_dir = user_data_dir or os.path.join(
            os.path.dirname(os.path.abspath(csv_path)), ".ebay_browser_profile"
        )
        print(f"Launching persistent browser (headless={headless})...")
        print(f"Using profile directory: {profile_dir}")
        print("Using browser channel: 'chrome'")

        launch_kwargs: dict[str, Any] = {
            "user_data_dir": profile_dir,
            "channel": "chrome",
            "headless": headless,
            "no_viewport": True,
            "ignore_default_args": ["--enable-automation"],
            "args": ["--disable-blink-features=AutomationControlled"],
        }

        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(**launch_kwargs)
            try:
                page = context.pages[0] if context.pages else context.new_page()
                _process_all(page_obj=page)
            finally:
                context.close()

    if dry_run:
        print("\n[DRY RUN] Completed without modifying CSV.")
        return

    # Write back updated rows atomically
    temp_path = csv_path + ".tmp"
    with open(temp_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    os.replace(temp_path, csv_path)
    print(f"\nSuccessfully updated {csv_path}")


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "funkos.csv")
    keywords_file = os.path.join(base_dir, "possible_key_words.txt")

    parser = argparse.ArgumentParser(description="Funko Pop eBay sold listings scraper.")
    parser.add_argument("--csv", type=str, default=None, help="Path to CSV file (default: funkos.csv)")
    parser.add_argument("--dry-run", action="store_true", help="Scrape without saving changes to funkos.csv")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode (default: headed)")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between requests in seconds (default: 2.0)")
    parser.add_argument("--profile-dir", type=str, default=None, help="Custom browser profile directory")
    args = parser.parse_args()

    input_path = args.csv or csv_file

    update_funkos_csv(
        input_path,
        keywords_file,
        dry_run=args.dry_run,
        headless=args.headless,
        delay=args.delay,
        user_data_dir=args.profile_dir,
    )





if __name__ == "__main__":
    main()


