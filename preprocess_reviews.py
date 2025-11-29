import pandas as pd
import os

def preprocess():
    input_file = 'data/reviews_raw.csv'
    output_file = 'data/reviews_cleaned.csv'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run scrape_reviews.py first.")
        return

    try:
        df = pd.read_csv(input_file)
        
        print(f"Initial shape: {df.shape}")
        
        # Check if required columns exist in raw data
        # 'content' -> 'review', 'score' -> 'rating', 'at' -> 'date'
        
        if 'content' in df.columns:
            df = df.rename(columns={
                'content': 'review',
                'score': 'rating',
                'at': 'date'
            })
        
        required_cols = ['review', 'rating', 'date', 'bank', 'source']
        
        # Ensure all required columns exist
        for col in required_cols:
            if col not in df.columns:
                print(f"Error: Missing column '{col}' in data.")
                return

        # Select columns
        df = df[required_cols]
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['review', 'bank', 'date'])
        
        # Handle missing data
        # Drop rows with missing review or rating
        df = df.dropna(subset=['review', 'rating'])
        
        # Normalize dates (YYYY-MM-DD)
        # 'date' might be string or datetime. pd.to_datetime handles both.
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        print(f"Final shape: {df.shape}")
        
        df.to_csv(output_file, index=False)
        print(f"Saved cleaned data to {output_file}")
        
    except Exception as e:
        print(f"Error during preprocessing: {e}")

if __name__ == "__main__":
    preprocess()
