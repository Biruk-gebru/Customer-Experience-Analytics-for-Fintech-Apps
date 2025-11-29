# Bank Review Analysis

## Task 1: Data Collection and Preprocessing

### Methodology

1.  **Scraping**:
    *   Used `google-play-scraper` library to fetch reviews from the Google Play Store.
    *   Targeted 3 banks: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.
    *   Fetched approximately 600 reviews per bank to ensure >400 valid reviews after cleaning.
    *   Data collected: Review text, rating, date, bank name, and source.

2.  **Preprocessing**:
    *   Script: `preprocess_reviews.py`
    *   Renamed columns to match requirements: `review`, `rating`, `date`.
    *   Removed duplicates based on review text, bank, and date.
    *   Dropped rows with missing review text or ratings.
    *   Normalized dates to `YYYY-MM-DD` format.
    *   Saved final dataset to `data/reviews_cleaned.csv`.

### Usage

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run scraper:
    ```bash
    python scrape_reviews.py
    ```

3.  Run preprocessor:
    ```bash
    python preprocess_reviews.py
    ```
