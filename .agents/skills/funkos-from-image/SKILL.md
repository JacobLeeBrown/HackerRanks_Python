---
name: funkos-from-image
description: Extracts Funko Pop details (category, search_name, box name, number, keywords) from user-provided images, validates or initializes the output CSV file, appends the new entries, and runs the market value scraper to calculate sold prices. Use whenever the user provides one or more photos of Funko Pops and requests to catalog them into a CSV or scrape their market values.
---

# Funko Pop Image-to-Scraper Workflow (`funkos-from-image`)

This skill defines the complete end-to-end workflow for taking an image of Funko Pops and a target CSV path, extracting figurine metadata, formatting and appending the rows, and scraping market value data from eBay.

---

## Workflow Steps

```
[1. Verify / Init CSV] ---> [2. Decipher Image] ---> [3. Append Rows] ---> [4. Run Scraper & Stats]
```

---

### Step 1: Verify or Initialize the Output File

Before analyzing the image, check the target output file path:

1. **New or Empty File**:
   If the output file does not exist or has a file size of 0 bytes, initialize it with the standard 9-column Funko header:
   ```csv
   category,search_name,name,number,key_words,ebay_avg,ebay_match_count,last_updated,ebay_search_link
   ```
2. **Existing File**:
   If the output file already exists, verify that it has an acceptable Funko schema. It must contain at minimum:
   - Category column: `category`
   - Identifier column: `search_name` (or legacy `name`)
   - Figure number: `number`
   - Keywords: `key_words`
3. **Automated Verification**:
   You can run the included verification helper script:
   ```powershell
   python .agents/skills/funkos-from-image/scripts/verify_funko_csv.py <path_to_output_csv>
   ```
   If the file has an incompatible schema, halt and explain the missing columns to the user before touching the file.

---

### Step 2: Decipher Funko Details from the Image

Visually inspect each Funko Pop box visible in the provided image(s). For each figurine, determine the following 5 fields:

#### 1. `category`
- The anime series, movie, or franchise grouping (e.g., `JJK`, `MHA`, `Demon Slayer`, `AoT`, `Marvel`, `One Punch Man`).
- If the user explicitly requested a category name or abbreviation in their prompt (e.g., *"all from My Hero Academia -> MHA"*), prioritize their requested convention.
- Otherwise, extract the franchise title from the top-center logo on the box.

#### 2. `search_name`
- The primary, clean character search string used for eBay sold queries and listing validation.
- Strip subtitles, promotional descriptors, or variant parentheticals (e.g., use `Levi`, `Eijiro Kirishima`, `All Might`, `Shota Aizawa`, `Yuji Itadori`).

#### 3. `name` (Box Name Override)
- **Only populate when the literal printed text on the box differs from `search_name`**.
- Leave **blank** (`""`) if the box name is identical to `search_name`.
- *Examples where `name` is populated:*
  - `search_name`: `Levi` $\rightarrow$ `name`: `Captain Levi`
  - `search_name`: `Eijiro Kirishima` $\rightarrow$ `name`: `Eijiro Unbreakable`
  - `search_name`: `All Might` $\rightarrow$ `name`: `All Might (Teacher)`
  - `search_name`: `Shota Aizawa` $\rightarrow$ `name`: `Shota Aizawa (Hero Costume)`
  - `search_name`: `Yuji Itadori` $\rightarrow$ `name`: `Yuji Itadori with Sukuna Mouth`

#### 4. `number`
- The figurine number printed on the box (typically in the top-right corner or above the character name).
- Must be numeric digits (e.g., `1114`, `1886`, `2125`).

#### 5. `key_words`
- Tertiary identifiers used to isolate specific variants, finishes, or store exclusives.
- Check the stickers on the plastic window:
  - **Retailer Exclusives**: `hot topic`, `gamestop`, `chalice`, `bam`, `box lunch`, `amazon`, `galactic`, `fye`, `ee`, `aaa`, `funkon`, `PX`.
  - **Variant Types**: `glow`, `flocked`, `chase`, `signed`.
- **Special Edition Sticker Note**:
  - The round silver/blue "Special Edition Funko" sticker is used for international distribution of US retailer exclusives.
  - Cross-reference the figure number to identify the underlying US retailer (e.g., #1152 is Hot Topic, #2129 is GameStop) so that negative keyword filtering does not reject valid sold listings.
- **Multiple Keywords**: Comma-separate within quotes (e.g., `"flocked,chase,chalice"`, `"aaa,glow"`, `"gamestop,glow"`).
- **Common / Non-exclusive**: Leave empty (`""`).
- Refer to `forfun/funko/possible_key_words.txt` for the full list of recognized positive/negative filter keywords.

#### 6. Multi-Image Deduplication
- When multiple photos are provided, cross-reference figurines across images to avoid duplicate rows.

---

### Step 3: Append Entries to the Output File

1. Format the deciphered entries with empty scraper output columns:
   ```csv
   category,search_name,name,number,key_words,,,,
   ```
2. Append the rows to the output CSV file, preserving existing rows and properly quoting fields that contain commas.
3. Verify that the row count matches the number of figurines identified.

---

### Step 4: Run the Scraper and Review Stats

1. **Execute Scraper**:
   Run `funko_scraper.py` targeting the output file:
   ```powershell
   python forfun/funko/funko_scraper.py --csv <path_to_output_csv>
   ```
   - The scraper runs in headed mode by default with persistent browser cookies (`.ebay_browser_profile/`).
   - If eBay displays a bot challenge ("Pardon Our Interruption..."), complete it in the open browser window and press `[Enter]` in the terminal to resume.

2. **Verify Results & Display Statistics**:
   Run `funko_stats.py` on the output CSV to calculate collection summary metrics:
   ```powershell
   python forfun/funko/funko_stats.py <path_to_output_csv>
   ```
   Report the newly scraped Funko details, average prices, and updated collection stats to the user.
