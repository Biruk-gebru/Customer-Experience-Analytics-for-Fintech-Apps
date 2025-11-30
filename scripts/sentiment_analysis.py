"""
Sentiment Analysis for Bank App Reviews
Task 2: Sentiment and Thematic Analysis
Uses VADER sentiment analyzer to compute sentiment scores for reviews
"""

import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyze sentiment of a text using VADER
    Returns: dict with pos, neg, neu, and compound scores
    """
    if pd.isna(text) or text == '':
        return {'pos': 0, 'neg': 0, 'neu': 1, 'compound': 0}
    
    scores = analyzer.polarity_scores(str(text))
    return scores

def classify_sentiment(compound_score):
    """
    Classify sentiment based on compound score
    """
    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def main():
    # Load data
    print("Loading reviews data...")
    df = pd.read_csv('data/reviews_cleaned.csv')
    print(f"Loaded {len(df)} reviews")
    
    # Apply sentiment analysis
    print("\nAnalyzing sentiment...")
    sentiments = df['review'].apply(analyze_sentiment)
    
    # Extract scores into separate columns
    df['sentiment_pos'] = sentiments.apply(lambda x: x['pos'])
    df['sentiment_neg'] = sentiments.apply(lambda x: x['neg'])
    df['sentiment_neu'] = sentiments.apply(lambda x: x['neu'])
    df['sentiment_score'] = sentiments.apply(lambda x: x['compound'])
    
    # Classify sentiment
    df['sentiment_label'] = df['sentiment_score'].apply(classify_sentiment)
    
    # Print summary statistics
    print("\n=== Sentiment Analysis Summary ===")
    print(f"\nTotal reviews analyzed: {len(df)}")
    print(f"Reviews with sentiment scores: {df['sentiment_score'].notna().sum()}")
    print(f"Success rate: {(df['sentiment_score'].notna().sum() / len(df) * 100):.2f}%")
    
    print("\n=== Sentiment Distribution ===")
    print(df['sentiment_label'].value_counts())
    
    print("\n=== Sentiment by Bank ===")
    sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'], normalize='index') * 100
    print(sentiment_by_bank.round(2))
    
    print("\n=== Average Sentiment Score by Bank ===")
    print(df.groupby('bank')['sentiment_score'].mean().round(3))
    
    print("\n=== Sentiment by Rating ===")
    print(df.groupby('rating')['sentiment_score'].mean().round(3))
    
    # Save results
    output_path = 'data/reviews_with_sentiment.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved results to {output_path}")
    
    # Create visualizations
    print("\nCreating visualizations...")
    create_visualizations(df)
    
    return df

def create_visualizations(df):
    """Create and save sentiment visualizations"""
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # Create output directory for plots
    Path('visualizations').mkdir(exist_ok=True)
    
    # 1. Sentiment distribution by bank
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Sentiment counts by bank
    sentiment_counts = pd.crosstab(df['bank'], df['sentiment_label'])
    sentiment_counts.plot(kind='bar', ax=axes[0, 0], color=['#d62728', '#7f7f7f', '#2ca02c'])
    axes[0, 0].set_title('Sentiment Distribution by Bank', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Bank')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].legend(title='Sentiment')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Average sentiment score by bank
    df.groupby('bank')['sentiment_score'].mean().plot(kind='bar', ax=axes[0, 1], color='#1f77b4')
    axes[0, 1].set_title('Average Sentiment Score by Bank', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Bank')
    axes[0, 1].set_ylabel('Average Compound Score')
    axes[0, 1].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Sentiment by rating
    rating_sentiment = df.groupby('rating')['sentiment_score'].mean()
    axes[1, 0].plot(rating_sentiment.index, rating_sentiment.values, marker='o', linewidth=2, markersize=8, color='#ff7f0e')
    axes[1, 0].set_title('Sentiment Score by Rating', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Rating')
    axes[1, 0].set_ylabel('Average Sentiment Score')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_xticks([1, 2, 3, 4, 5])
    
    # Sentiment distribution (overall)
    sentiment_dist = df['sentiment_label'].value_counts()
    colors = {'positive': '#2ca02c', 'neutral': '#7f7f7f', 'negative': '#d62728'}
    sentiment_dist.plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%', 
                        colors=[colors[label] for label in sentiment_dist.index],
                        startangle=90)
    axes[1, 1].set_title('Overall Sentiment Distribution', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('')
    
    plt.tight_layout()
    plt.savefig('visualizations/sentiment_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved sentiment_analysis.png")
    plt.close()
    
    # 2. Detailed bank comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare data for grouped bar chart
    banks = df['bank'].unique()
    x = np.arange(len(banks))
    width = 0.25
    
    positive = [df[(df['bank'] == bank) & (df['sentiment_label'] == 'positive')].shape[0] for bank in banks]
    neutral = [df[(df['bank'] == bank) & (df['sentiment_label'] == 'neutral')].shape[0] for bank in banks]
    negative = [df[(df['bank'] == bank) & (df['sentiment_label'] == 'negative')].shape[0] for bank in banks]
    
    ax.bar(x - width, positive, width, label='Positive', color='#2ca02c')
    ax.bar(x, neutral, width, label='Neutral', color='#7f7f7f')
    ax.bar(x + width, negative, width, label='Negative', color='#d62728')
    
    ax.set_xlabel('Bank', fontweight='bold')
    ax.set_ylabel('Number of Reviews', fontweight='bold')
    ax.set_title('Sentiment Comparison Across Banks', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(banks)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations/sentiment_by_bank_detailed.png', dpi=300, bbox_inches='tight')
    print("✓ Saved sentiment_by_bank_detailed.png")
    plt.close()

if __name__ == "__main__":
    df_with_sentiment = main()
    print("\n✓ Sentiment analysis completed successfully!")
