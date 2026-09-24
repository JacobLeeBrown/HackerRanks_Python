## Funko Tool Context

"Funkos" are collectible figurines of almost every character, fictional or non-
fictional. The tool in this directory is for web-scraping the USD value of
target Funkos from common marketplaces like Ebay or the official Funko site.

Each individual Funko has identifiers like a name and a number. While these are
the key details to classifying a specific figurine, popular characters can have
multiple versions commonly differentiated by the associated number. The 
difficulty of this task comes from the reality that there can be variants of the
same character *and* number, like a base version and another that glows in the
dark.

The input to this tool is a CSV in the same directory, titled "funkos.csv".
Columns set manually will be:
- category = Arbitrary grouping for human search
- name = The primary identifier for the Funko, as it appears on its box.
- number = The secondary identifier, also as it appears on its box.
- key_words = A double-quoted, comma-delimited list of tertiary identifiers to
    differentiate special versions.

Given these values, the tool modifies `funkos.csv` in-place, filling in:
- `ebay_search_link`: The search URL used for the Funko on eBay.
- `ebay_match_count`: The number of sold listings matching the exact Funko.
- `ebay_avg`: The average USD value of matching sold listings, or `--` if no matches are found.
- `last_updated`: The date (YYYY-MM-DD) when the row was populated.

The tool only scrapes rows that do not already have a `last_updated` value,
skipping any rows that have already been populated.
Concerning `key_words`, it's just as important to understanding what key-words
are *not* provided. To support this, I've included `possible_key_words.txt` in
this directory (Note: the list is not exhaustive, but covers the most common
variants).

### Edge Cases

1. Ebay's search is not perfect. Even if we gave an exact product code for the
        Funko we wanted, it could still return listings for similar, but not 
        exact, Funkos. Those listings should be ignored.
2. A common, *non-factory* variant is signed Funkos, meaning the person the
        Funko depicts, or the character's actor/voice-actor signed the Funko's
        box, making it a more valuable collectible. "signed" is included as a
        possible key-word to properly identify/ignore such cases.