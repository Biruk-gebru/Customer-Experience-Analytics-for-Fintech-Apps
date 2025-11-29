from google_play_scraper import reviews, Sort
import pandas as pd
import os

APP_IDS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.bankofabyssinia.boamobile.retail",
    "Dashen": "com.dashen.dashensuperapp"
}

def scrape_reviews():
    all_reviews = []
    
    for bank_name, app_id in APP_IDS.items():
        print(f"Scraping reviews for {bank_name} ({app_id})...")
        
        try:
            # Scrape at least 400 reviews
            # We fetch 600 to ensure we have enough after cleaning
            rvs, _ = reviews(
                app_id,
                lang='en', # defaults to 'en'
                country='us', # defaults to 'us'
                sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
                count=600, 
                filter_score_with=None # None: all scores
            )
            
            print(f"Fetched {len(rvs)} reviews for {bank_name}")
            
            for r in rvs:
                r['bank'] = bank_name
                r['source'] = 'Google Play'
                r['app_id'] = app_id
                all_reviews.append(r)
        except Exception as e:
            print(f"Error scraping {bank_name}: {e}")
            
    return all_reviews

if __name__ == "__main__":
    data = scrape_reviews()
    if data:
        df = pd.DataFrame(data)
        
        # Save raw data
        os.makedirs('data', exist_ok=True)
        output_path = 'data/reviews_raw.csv'
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} raw reviews to {output_path}")
    else:
        print("No data scraped.")
