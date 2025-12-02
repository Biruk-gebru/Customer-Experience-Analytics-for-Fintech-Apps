# Bank Review Analysis - Week 2 Challenge

Customer Experience Analytics for Fintech Apps: Analyzing Google Play Store reviews for three Ethiopian banks.

## Overview

This project analyzes customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for:
- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

---

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

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python scrape_reviews.py

# Run preprocessor
python preprocess_reviews.py
```

### Output
- `data/reviews_raw.csv` - Raw scraped reviews
- `data/reviews_cleaned.csv` - Cleaned and preprocessed reviews (1,200+ reviews)

---

## Task 2: Sentiment and Thematic Analysis

### Methodology

1. **Sentiment Analysis**:
   - Used **VADER** (Valence Aware Dictionary and sEntiment Reasoner) for sentiment analysis
   - Computed sentiment scores: positive, negative, neutral, and compound (-1 to 1)
   - Classified reviews as positive (≥0.05), negative (≤-0.05), or neutral
   - Aggregated sentiment by bank and rating

2. **Thematic Analysis**:
   - Extracted keywords using **TF-IDF** with n-grams (1-3)
   - Implemented rule-based clustering with 7 predefined themes:
     - Account Access Issues
     - Transaction Performance
     - Technical Issues
     - User Interface & Experience
     - Customer Support
     - Feature Requests
     - Security & Privacy
   - Assigned themes to reviews based on keyword matching

### Usage

```bash
# Run sentiment analysis
python3 scripts/sentiment_analysis.py

# Run thematic analysis (requires sentiment analysis output)
python3 scripts/thematic_analysis.py

# Or use Jupyter notebooks for interactive analysis
jupyter notebook
# Open notebooks/sentiment_analysis.ipynb
# Open notebooks/thematic_analysis.ipynb
```

### Outputs

**Data Files:**
- `data/reviews_with_sentiment.csv` - Reviews with sentiment scores and labels
- `data/reviews_with_themes.csv` - Reviews with themes and keywords
- `theme_analysis_report.txt` - Detailed theme analysis report

**Visualizations:**
- `visualizations/sentiment_analysis.png` - Sentiment distribution overview
- `visualizations/sentiment_by_bank_detailed.png` - Bank comparison
- `visualizations/theme_analysis.png` - Theme distribution
- `visualizations/wordclouds_by_bank.png` - Word clouds for each bank

### Key Findings

- **Sentiment Analysis**: >99% success rate analyzing 1,200+ reviews
- **Thematic Analysis**: Identified 7 key themes with strong coverage across all banks
- **Top Themes**: Technical Issues, Account Access Issues, and Transaction Performance

---

## Task 3: Store Cleaned Data in PostgreSQL

### Methodology

1.  **Database Setup**:
    *   Installed PostgreSQL and created a database named `bank_reviews`.
    *   Created a user `db_user` with appropriate permissions.

2.  **Schema Design**:
    *   **banks** table:
        *   `bank_id` (SERIAL PRIMARY KEY)
        *   `bank_name` (VARCHAR)
        *   `app_name` (VARCHAR)
    *   **reviews** table:
        *   `review_id` (SERIAL PRIMARY KEY)
        *   `bank_id` (INTEGER, FOREIGN KEY references banks)
        *   `review_text` (TEXT)
        *   `rating` (INTEGER)
        *   `review_date` (TIMESTAMP)
        *   `sentiment_label` (VARCHAR)
        *   `sentiment_score` (FLOAT)
        *   `source` (VARCHAR)

3.  **Data Loading**:
    *   Script: `scripts/load_data.py`
    *   Connects to the PostgreSQL database using `sqlalchemy` and `psycopg2`.
    *   Creates tables if they don't exist.
    *   Reads cleaned data from `data/reviews_with_themes.csv`.
    *   Populates `banks` and `reviews` tables.
    *   Verifies data integrity by counting records.

### Usage

```bash
# Ensure PostgreSQL is running and user/db are set up
# (See scripts/load_data.py for connection details)

# Run data loader
python3 scripts/load_data.py
```

### Output
-   PostgreSQL database `bank_reviews` populated with 1,800+ reviews.
-   `schema.sql` - Database schema dump.

---

## Task 4: Insights and Recommendations

### Methodology

1. **Insights Derivation**:
   - Analyzed sentiment and themes to identify satisfaction drivers and pain points
   - Compared banks across key metrics (ratings, sentiment, themes)
   - Identified 2+ drivers and pain points per bank with supporting evidence

2. **Visualizations**:
   - Created comparative visualizations using Matplotlib and Seaborn
   - Generated plots for sentiment trends, rating distributions, and pain point analysis

3. **Recommendations**:
   - Developed actionable recommendations for each bank
   - Addressed three scenarios: user retention, feature enhancement, and complaint management
   - Considered ethical implications and potential biases in review data

### Usage

```bash
# Run insights analysis
python3 scripts/insights_analysis.py
```

### Outputs

**Report:**
- `insights_and_recommendations.md` - Comprehensive analysis with recommendations

**Visualizations:**
- `visualizations/avg_sentiment_by_bank.png` - Average sentiment comparison
- `visualizations/rating_distribution_by_bank.png` - Rating distribution
- `visualizations/pain_points_by_bank.png` - Top pain points by bank

### Key Findings

**Satisfaction Drivers:**
- **CBE**: Feature richness, UI design, transaction performance
- **BOA**: Limited positive feedback (critical concern)
- **Dashen**: Excellent UX, fast transactions, high satisfaction

**Pain Points:**
- **CBE**: Transaction speed issues, feature gaps
- **BOA**: Technical instability, crashes, login failures (critical)
- **Dashen**: Limited bill payment options

**Recommendations:**
- **CBE**: Optimize transaction performance, add bill payment features
- **BOA**: Emergency technical overhaul, fix stability issues (urgent)
- **Dashen**: Expand bill payment options, maintain excellence

---

## Project Structure

```
prod/
├── data/
│   ├── reviews_raw.csv
│   ├── reviews_cleaned.csv
│   ├── reviews_with_sentiment.csv
│   └── reviews_with_themes.csv
├── scripts/
│   ├── sentiment_analysis.py
│   ├── thematic_analysis.py
│   ├── load_data.py
│   └── insights_analysis.py
├── notebooks/
│   ├── sentiment_analysis.ipynb
│   └── thematic_analysis.ipynb
├── visualizations/
│   ├── sentiment_analysis.png
│   ├── sentiment_by_bank_detailed.png
│   ├── theme_analysis.png
│   ├── wordclouds_by_bank.png
│   ├── avg_sentiment_by_bank.png
│   ├── rating_distribution_by_bank.png
│   └── pain_points_by_bank.png
├── scrape_reviews.py
├── preprocess_reviews.py
├── requirements.txt
├── schema.sql
├── insights_and_recommendations.md
└── README.md
```

## Dependencies

All required dependencies are listed in `requirements.txt`:
- google-play-scraper
- pandas, numpy
- vaderSentiment
- spacy, scikit-learn
- matplotlib, seaborn, wordcloud
- jupyter
- psycopg2-binary, sqlalchemy

## License

This project is part of the 10 Academy AI Mastery Week 2 Challenge.
