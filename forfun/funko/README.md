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

## Funko Stats Reporter (`funko_stats.py`)

A companion analysis tool that reads any Funko CSV and reports key summary metrics to the console based on the `ebay_avg` column:

- **Total Collection Value**: Sum of all priced Funkos.
- **Average Funko Value**: Mean market value across all priced Funkos.
- **Highest Valued Funko(s)**: Displays name, figure number, category, keywords, and price (handles ties).
- **Lowest Valued Funko(s)**: Displays name, figure number, category, keywords, and price (handles ties).
- **Pricing Status Counts**: Total Funkos, count priced, and count unpriced/pending.

### Usage

```powershell
# Analyze default funkos.csv
python funko_stats.py

# Analyze a specific CSV
python funko_stats.py my_funkos.csv

# Or use the --csv flag
python funko_stats.py --csv my_funkos.csv
```

### Sample Output

```text
=======================================================
           FUNKO POP STATISTICS REPORT
=======================================================
File: my_funkos.csv

Total Funkos:            12
  - Priced:              12
  - Unpriced / Pending:  0

-------------------------------------------------------
Total Collection Value:  $161.40
Average Funko Value:     $13.45
-------------------------------------------------------

Highest Valued Funko ($37.66):
  * Maki Zen'in #1373 (JJK)

Lowest Valued Funko ($5.82):
  * Inasa Yoarashi #1145 (MHA)
=======================================================
```

---

## Agent Skill: `funkos-from-image`

A specialized agent skill located at `.agents/skills/funkos-from-image/SKILL.md` that encapsulates the full image-to-scraping pipeline:

1. **Verify / Initialize Output CSV**: Validates that the target file is either empty or follows standard Funko schema (via `scripts/verify_funko_csv.py`).
2. **Decipher Details from Photos**: Extracts `category`, `search_name`, box `name` (override), `number`, and `key_words` (stickers/exclusives).
3. **Append Entries**: Appends the new rows formatted for scraping.
4. **Scrape & Report**: Invokes `funko_scraper.py` on the target file and calculates statistics with `funko_stats.py`.

---

## Running Tests

Run the test suites for both the scraper and stats reporter:

```powershell
# Run scraper tests
python -m unittest test_funko_scraper.py

# Run stats reporter tests
python -m unittest test_funko_stats.py

# Or run all tests together
python -m unittest discover
```

