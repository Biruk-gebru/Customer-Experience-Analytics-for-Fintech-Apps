import pandas as pd
from sqlalchemy import create_engine, text
import os

# Database connection parameters
DB_USER = 'db_user'
DB_PASSWORD = 'db_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'bank_reviews'

# Connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_tables(engine):
    """Creates the banks and reviews tables."""
    with engine.connect() as connection:
        # Create banks table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS banks (
                bank_id SERIAL PRIMARY KEY,
                bank_name VARCHAR(255) NOT NULL,
                app_name VARCHAR(255)
            );
        """))
        
        # Create reviews table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id SERIAL PRIMARY KEY,
                bank_id INTEGER REFERENCES banks(bank_id),
                review_text TEXT,
                rating INTEGER,
                review_date TIMESTAMP,
                sentiment_label VARCHAR(50),
                sentiment_score FLOAT,
                source VARCHAR(50)
            );
        """))
        connection.commit()
    print("Tables created successfully.")

def load_data(file_path, engine):
    """Loads data from CSV into the database."""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    df = pd.read_csv(file_path)
    
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Get unique banks and insert them
    unique_banks = df[['bank']].drop_duplicates().reset_index(drop=True)
    
    with engine.connect() as connection:
        for _, row in unique_banks.iterrows():
            # Check if bank exists
            result = connection.execute(text("SELECT bank_id FROM banks WHERE bank_name = :name"), {"name": row['bank']})
            bank_id = result.scalar()
            
            if not bank_id:
                # Insert bank
                connection.execute(text("INSERT INTO banks (bank_name, app_name) VALUES (:name, :app)"), 
                                   {"name": row['bank'], "app": row['bank'] + " App"})
                connection.commit()

    # Create a mapping of bank_name to bank_id
    bank_mapping = {}
    with engine.connect() as connection:
        result = connection.execute(text("SELECT bank_name, bank_id FROM banks"))
        for row in result:
            bank_mapping[row[0]] = row[1]
            
    # Prepare reviews dataframe for insertion
    reviews_df = df.copy()
    reviews_df['bank_id'] = reviews_df['bank'].map(bank_mapping)
    reviews_df = reviews_df.rename(columns={
        'review': 'review_text',
        'date': 'review_date'
    })
    
    # Select only relevant columns
    cols_to_keep = ['bank_id', 'review_text', 'rating', 'review_date', 'sentiment_label', 'sentiment_score', 'source']
    
    # Ensure all columns exist
    for col in cols_to_keep:
        if col not in reviews_df.columns:
            # If source is missing, default to 'Google Play' as per task context usually
            if col == 'source':
                reviews_df[col] = 'Google Play'
            else:
                reviews_df[col] = None
            
    reviews_df = reviews_df[cols_to_keep]
    
    # Insert reviews
    reviews_df.to_sql('reviews', engine, if_exists='append', index=False)
    print(f"Inserted {len(reviews_df)} reviews.")

def verify_data(engine):
    """Verifies data integrity."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM reviews"))
        count = result.scalar()
        print(f"Total reviews in database: {count}")
        
        result = connection.execute(text("SELECT bank_name, COUNT(*) FROM reviews r JOIN banks b ON r.bank_id = b.bank_id GROUP BY bank_name"))
        print("Reviews per bank:")
        for row in result:
            print(f"{row[0]}: {row[1]}")

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    create_tables(engine)
    # Assuming script is run from prod/scripts/ or prod/
    # We will try absolute path or relative
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'reviews_with_themes.csv')
    print(f"Loading data from: {data_path}")
    load_data(data_path, engine)
    verify_data(engine)
