import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import ast

def load_data(filepath):
    df = pd.read_csv(filepath)
    # Parse themes if they are stringified lists
    if 'identified_themes' in df.columns:
         # It seems 'identified_themes' might be a comma separated string or a single string in the CSV based on previous output
         # Let's check the CSV format from previous `head` command
         # "Feature Requests" -> It's a string, not a list.
         # But wait, `themes` column was `['Feature Requests']`.
         # Let's use `identified_themes` which seemed to be the clean string.
         pass
    return df

def analyze_bank(df, bank_name):
    print(f"\n--- Analysis for {bank_name} ---")
    bank_df = df[df['bank'] == bank_name]
    
    avg_rating = bank_df['rating'].mean()
    avg_sentiment = bank_df['sentiment_score'].mean()
    print(f"Average Rating: {avg_rating:.2f}")
    print(f"Average Sentiment Score: {avg_sentiment:.2f}")
    
    # Drivers (Positive Reviews: Rating >= 4)
    pos_df = bank_df[bank_df['rating'] >= 4]
    print(f"\nTop Drivers (Themes in Positive Reviews - {len(pos_df)} reviews):")
    if not pos_df.empty:
        print(pos_df['identified_themes'].value_counts().head(3))
        
    # Pain Points (Negative Reviews: Rating <= 2)
    neg_df = bank_df[bank_df['rating'] <= 2]
    print(f"\nTop Pain Points (Themes in Negative Reviews - {len(neg_df)} reviews):")
    if not neg_df.empty:
        print(neg_df['identified_themes'].value_counts().head(3))
        
    return avg_rating, avg_sentiment

def generate_comparison_plots(df, output_dir):
    # 1. Average Sentiment by Bank
    plt.figure(figsize=(10, 6))
    sns.barplot(x='bank', y='sentiment_score', data=df, estimator='mean', errorbar=None)
    plt.title('Average Sentiment Score by Bank')
    plt.ylabel('Average Sentiment Score')
    plt.savefig(os.path.join(output_dir, 'avg_sentiment_by_bank.png'))
    plt.close()
    
    # 2. Rating Distribution by Bank
    plt.figure(figsize=(10, 6))
    sns.countplot(x='rating', hue='bank', data=df)
    plt.title('Rating Distribution by Bank')
    plt.savefig(os.path.join(output_dir, 'rating_distribution_by_bank.png'))
    plt.close()
    
    # 3. Theme Frequency by Sentiment (Positive vs Negative)
    # We need to melt or restructure data for this
    # Let's just do a simple count of themes for Negative reviews per bank
    neg_df = df[df['rating'] <= 2]
    if not neg_df.empty:
        plt.figure(figsize=(12, 8))
        sns.countplot(y='identified_themes', hue='bank', data=neg_df, order=neg_df['identified_themes'].value_counts().index[:10])
        plt.title('Top Pain Point Themes (Negative Reviews) by Bank')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'pain_points_by_bank.png'))
        plt.close()

def main():
    data_path = 'data/reviews_with_themes.csv'
    output_dir = 'visualizations'
    
    if not os.path.exists(data_path):
        print("Data file not found.")
        return
        
    df = load_data(data_path)
    
    banks = df['bank'].unique()
    stats = []
    
    for bank in banks:
        avg_rating, avg_sentiment = analyze_bank(df, bank)
        stats.append({'bank': bank, 'avg_rating': avg_rating, 'avg_sentiment': avg_sentiment})
        
    generate_comparison_plots(df, output_dir)
    print("\nVisualizations generated in 'visualizations/' directory.")

if __name__ == "__main__":
    main()
