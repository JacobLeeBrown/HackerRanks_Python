# Funko Pop Market Value Scraper

An automated scraper that queries eBay's completed and sold listings to calculate real-world market values (USD) for target Funko Pop figurines, writing results back to a CSV file in-place.

---

## Features

- **Automated Sold Listings Querying**: Constructs targeted eBay sold searches using character identifiers, figure numbers, and variant keywords.
- **Accurate Title & Keyword Matching**: Enforces strict positive keyword matching and negative keyword exclusion using [possible_key_words.txt](file:///c:/dev/github/HackerRanks_Python/forfun/funko/possible_key_words.txt) to prevent standard versions from being conflated with rare variants, retailer exclusives, or signed boxes.
- **Smart 30-Day Freshness Filter**: Automatically skips entries that have been updated within the last 30 days (configurable), only scraping new or stale rows.
- **Persistent Browser Session**: Launches a real Google Chrome instance with Playwright and a persistent profile directory (`.ebay_browser_profile/`), allowing manual completion of eBay verification challenges if prompted.
- **Safe In-Place CSV Updates**: Atomically updates CSV files so no data is corrupted or lost during interrupted runs.

---

## Installation & Setup

1. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Ensure Google Chrome is Installed**:
   The scraper uses Playwright configured to use your system's installed Google Chrome (`channel="chrome"`). If Playwright browsers are needed separately:
   ```powershell
   playwright install chromium
   ```

---

## Input CSV Setup

The scraper operates on CSV files following this 9-column schema:

```csv
category,search_name,name,number,key_words,ebay_search_link,ebay_match_count,ebay_avg,last_updated
```

### Manual Input Columns

When adding new Funko Pops to your CSV, populate the first 5 columns and leave the remaining 4 empty:

| Column | Description | Example |
| :--- | :--- | :--- |
| `category` | Arbitrary grouping (e.g., anime series, franchise) for human organization. | `JJK`, `MHA`, `Demon Slayer` |
| `search_name` | The primary search query used on eBay and for listing title validation. | `Levi`, `Satoru Gojo`, `Eijiro Kirishima` |
| `name` | *(Optional)* The literal physical name printed on the Funko box. Leave blank if identical to `search_name`. Only populate when the box name differs. | `Captain Levi`, `Eijiro Unbreakable`, `All Might (Teacher)` |
| `number` | The Funko Pop figure number as printed on the box. | `1315`, `1114`, `1009` |
| `key_words` | Comma-separated list of variant/retailer keywords (quoted if containing multiple keywords). | `"flocked,chase,chalice"`, `hot topic`, `bam` |

> [!TIP]
> **Negative Keyword Filtering**: The scraper checks listings against [possible_key_words.txt](file:///c:/dev/github/HackerRanks_Python/forfun/funko/possible_key_words.txt). If a listing contains any keyword from that list that is **not** specified in your row's `key_words`, that listing will be rejected. This ensures non-chase figures are not polluted by chase pricing, unsigned figures are not priced as signed, etc.

### Scraper Output Columns

Leave these blank when adding new rows. The scraper populates them automatically:

| Column | Description |
| :--- | :--- |
| `ebay_search_link` | The exact URL used to fetch eBay sold listings. |
| `ebay_match_count` | The number of valid sold listings matched after filtering. |
| `ebay_avg` | The average USD sold price, or `--` if no valid listings were found. |
| `last_updated` | The date (`YYYY-MM-DD`) when the entry was scraped. |

---

## Running the Scraper

### 1. Default Run (`funkos.csv`)
Scrapes all pending or stale entries in the default `funkos.csv`:
```powershell
python funko_scraper.py
```

### 2. Targeting a Custom CSV
To scrape a different file, such as `my_funkos.csv`:
```powershell
python funko_scraper.py --csv my_funkos.csv
```

### 3. Dry Run (No File Changes)
Fetch listings, print match counts, and display calculated averages without modifying the CSV:
```powershell
python funko_scraper.py --csv my_funkos.csv --dry-run
```

### 4. Customizing Request Delay & Age Threshold
To increase the polite delay between requests (default: 2.0s) or re-scrape entries older than 14 days (default: 30 days):
```powershell
python funko_scraper.py --delay 3.0 --max-age 14
```

### 5. Headless Mode
Run the browser in headless mode (background):
```powershell
python funko_scraper.py --headless
```
> [!WARNING]
> eBay frequently serves bot verification challenges ("Pardon Our Interruption...") in headless mode. Headed mode (`headless=False`, the default) is strongly recommended so you can solve any interactive CAPTCHA challenges when prompted.

---

## CLI Options Reference

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--csv` | `str` | `funkos.csv` | Path to the target CSV file. |
| `--dry-run` | flag | `False` | Scrape and calculate prices without saving to CSV. |
| `--headless` | flag | `False` | Run browser in headless mode. |
| `--delay` | `float` | `2.0` | Delay in seconds between requests to prevent rate limiting. |
| `--max-age` | `int` | `30` | Maximum age in days before an existing row is re-scraped. |
| `--profile-dir` | `str` | `.ebay_browser_profile` | Custom persistent Chrome profile directory. |

---

## Handling eBay Bot Verification

If eBay detects automated traffic, the terminal will notify you:

```text
=================================================================
[!] ACTION REQUIRED: eBay challenge detected ('Pardon Our Interruption')
    Please complete the verification challenge in the browser window.
=================================================================
    Press [Enter] after completing the challenge...
```

1. Switch to the open Chrome browser window.
2. Complete the CAPTCHA / slide challenge.
3. Return to the terminal and press `[Enter]`.
4. The scraper will reload the page and continue automatically. Verification cookies are preserved in `.ebay_browser_profile/` so subsequent queries remain authenticated.

---

## Running Tests

Unit tests mock network requests and verify URL formatting, keyword matching, price calculations, and CSV parsing:

```powershell
python -m unittest test_funko_scraper.py
```
