"""
Thematic Analysis for Bank App Reviews
Task 2: Sentiment and Thematic Analysis
Uses TF-IDF and keyword extraction to identify themes in reviews
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from pathlib import Path
import re

# Define theme keywords (manual/rule-based clustering)
THEME_KEYWORDS = {
    'Account Access Issues': [
        'login', 'password', 'account', 'locked', 'access', 'sign in', 
        'authentication', 'verify', 'otp', 'code', 'unlock', 'reset'
    ],
    'Transaction Performance': [
        'transfer', 'transaction', 'slow', 'loading', 'payment', 'send money',
        'receive', 'delay', 'pending', 'processing', 'speed', 'fast', 'quick'
    ],
    'Technical Issues': [
        'crash', 'bug', 'error', 'freeze', 'not working', 'broken', 'issue',
        'problem', 'fail', 'glitch', 'stuck', 'down', 'offline'
    ],
    'User Interface & Experience': [
        'ui', 'interface', 'design', 'easy', 'simple', 'user friendly',
        'navigation', 'layout', 'look', 'beautiful', 'modern', 'clean'
    ],
    'Customer Support': [
        'support', 'help', 'customer service', 'call center', 'contact',
        'response', 'complaint', 'feedback', 'assist', 'service'
    ],
    'Feature Requests': [
        'need', 'want', 'add', 'feature', 'should', 'wish', 'request',
        'update', 'improve', 'enhancement', 'suggest', 'would be nice'
    ],
    'Security & Privacy': [
        'security', 'safe', 'secure', 'privacy', 'protect', 'fingerprint',
        'biometric', 'fraud', 'scam', 'trust', 'encryption'
    ]
}

def clean_text(text):
    """Clean and normalize text for analysis"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def extract_keywords_tfidf(reviews, n_keywords=20):
    """Extract top keywords using TF-IDF"""
    
    # Clean reviews
    cleaned_reviews = [clean_text(r) for r in reviews]
    
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 3),  # unigrams, bigrams, trigrams
        min_df=2,  # must appear in at least 2 documents
        max_df=0.8,  # ignore terms that appear in >80% of documents
        stop_words='english'
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(cleaned_reviews)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get average TF-IDF scores
        avg_scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
        
        # Get top keywords
        top_indices = avg_scores.argsort()[-n_keywords:][::-1]
        top_keywords = [(feature_names[i], avg_scores[i]) for i in top_indices]
        
        return top_keywords
    except:
        return []

def assign_themes(text):
    """Assign themes to a review based on keyword matching"""
    if pd.isna(text) or text == '':
        return []
    
    text_lower = str(text).lower()
    matched_themes = []
    
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                matched_themes.append(theme)
                break  # Only count theme once per review
    
    return matched_themes

def main():
    # Load data with sentiment
    print("Loading reviews with sentiment data...")
    df = pd.read_csv('data/reviews_with_sentiment.csv')
    print(f"Loaded {len(df)} reviews")
    
    # Extract keywords per bank
    print("\n=== Extracting Keywords by Bank ===")
    bank_keywords = {}
    
    for bank in df['bank'].unique():
        print(f"\n{bank}:")
        bank_reviews = df[df['bank'] == bank]['review'].tolist()
        keywords = extract_keywords_tfidf(bank_reviews, n_keywords=15)
        bank_keywords[bank] = keywords
        
        print("Top keywords:")
        for keyword, score in keywords[:10]:
            print(f"  - {keyword}: {score:.4f}")
    
    # Assign themes to each review
    print("\n\nAssigning themes to reviews...")
    df['themes'] = df['review'].apply(assign_themes)
    df['num_themes'] = df['themes'].apply(len)
    df['theme_names'] = df['themes'].apply(lambda x: ', '.join(x) if x else 'No Theme')
    
    # Theme analysis
    print("\n=== Theme Analysis Summary ===")
    print(f"\nReviews with at least one theme: {(df['num_themes'] > 0).sum()} ({(df['num_themes'] > 0).sum() / len(df) * 100:.1f}%)")
    print(f"Average themes per review: {df['num_themes'].mean():.2f}")
    
    # Count themes by bank
    print("\n=== Theme Distribution by Bank ===")
    for bank in df['bank'].unique():
        print(f"\n{bank}:")
        bank_df = df[df['bank'] == bank]
        all_themes = []
        for themes in bank_df['themes']:
            all_themes.extend(themes)
        
        theme_counts = Counter(all_themes)
        for theme, count in theme_counts.most_common():
            percentage = (count / len(bank_df)) * 100
            print(f"  {theme}: {count} ({percentage:.1f}%)")
    
    # Overall theme distribution
    print("\n=== Overall Theme Distribution ===")
    all_themes = []
    for themes in df['themes']:
        all_themes.extend(themes)
    
    theme_counts = Counter(all_themes)
    for theme, count in theme_counts.most_common():
        percentage = (count / len(df)) * 100
        print(f"  {theme}: {count} ({percentage:.1f}%)")
    
    # Save results
    output_path = 'data/reviews_with_themes.csv'
    
    # Prepare output columns
    output_df = df.copy()
    output_df['identified_themes'] = output_df['theme_names']
    
    # Extract top keywords for each review
    print("\nExtracting top keywords for each review...")
    output_df['top_keywords'] = output_df['review'].apply(extract_review_keywords)
    
    # Save
    output_df.to_csv(output_path, index=False)
    print(f"\n✓ Saved results to {output_path}")
    
    # Create visualizations
    print("\nCreating visualizations...")
    create_visualizations(df, bank_keywords)
    
    # Generate theme summary report
    generate_theme_report(df, bank_keywords)
    
    return output_df

def extract_review_keywords(review, n=5):
    """Extract top keywords from a single review"""
    if pd.isna(review) or review == '':
        return ''
    
    cleaned = clean_text(review)
    words = cleaned.split()
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
                  'this', 'that', 'it', 'its', 'i', 'you', 'he', 'she', 'we', 'they'}
    
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Get most common
    word_counts = Counter(keywords)
    top = [word for word, count in word_counts.most_common(n)]
    
    return ', '.join(top)

def create_visualizations(df, bank_keywords):
    """Create theme visualizations"""
    
    sns.set_style("whitegrid")
    Path('visualizations').mkdir(exist_ok=True)
    
    # 1. Theme distribution across banks
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Collect all themes by bank
    theme_data = []
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        all_themes = []
        for themes in bank_df['themes']:
            all_themes.extend(themes)
        theme_counts = Counter(all_themes)
        
        for theme, count in theme_counts.items():
            theme_data.append({'Bank': bank, 'Theme': theme, 'Count': count})
    
    theme_df = pd.DataFrame(theme_data)
    
    if not theme_df.empty:
        # Top themes overall
        theme_totals = theme_df.groupby('Theme')['Count'].sum().sort_values(ascending=False)
        theme_totals.head(7).plot(kind='barh', ax=axes[0, 0], color='#1f77b4')
        axes[0, 0].set_title('Top Themes Across All Banks', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Number of Reviews')
        axes[0, 0].set_ylabel('Theme')
        
        # Themes by bank (stacked bar)
        theme_pivot = theme_df.pivot_table(index='Bank', columns='Theme', values='Count', fill_value=0)
        theme_pivot.plot(kind='bar', stacked=True, ax=axes[0, 1])
        axes[0, 1].set_title('Theme Distribution by Bank', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Bank')
        axes[0, 1].set_ylabel('Number of Reviews')
        axes[0, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Number of themes per review
    df['num_themes'].value_counts().sort_index().plot(kind='bar', ax=axes[1, 0], color='#2ca02c')
    axes[1, 0].set_title('Distribution of Theme Count per Review', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Number of Themes')
    axes[1, 0].set_ylabel('Number of Reviews')
    
    # Theme coverage by bank
    theme_coverage = df.groupby('bank').apply(lambda x: (x['num_themes'] > 0).sum() / len(x) * 100)
    theme_coverage.plot(kind='bar', ax=axes[1, 1], color='#ff7f0e')
    axes[1, 1].set_title('Theme Coverage by Bank (%)', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Bank')
    axes[1, 1].set_ylabel('Percentage of Reviews with Themes')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('visualizations/theme_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved theme_analysis.png")
    plt.close()
    
    # 2. Word clouds for each bank
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for idx, bank in enumerate(df['bank'].unique()):
        bank_reviews = ' '.join(df[df['bank'] == bank]['review'].dropna().astype(str))
        
        if bank_reviews:
            wordcloud = WordCloud(
                width=800, height=400,
                background_color='white',
                colormap='viridis',
                max_words=100
            ).generate(bank_reviews)
            
            axes[idx].imshow(wordcloud, interpolation='bilinear')
            axes[idx].set_title(f'{bank}', fontsize=14, fontweight='bold')
            axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('visualizations/wordclouds_by_bank.png', dpi=300, bbox_inches='tight')
    print("✓ Saved wordclouds_by_bank.png")
    plt.close()

def generate_theme_report(df, bank_keywords):
    """Generate a text report summarizing themes"""
    
    report_path = 'theme_analysis_report.txt'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("THEMATIC ANALYSIS REPORT\n")
        f.write("Task 2: Sentiment and Thematic Analysis\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Total Reviews Analyzed: {len(df)}\n")
        f.write(f"Reviews with Themes: {(df['num_themes'] > 0).sum()} ({(df['num_themes'] > 0).sum() / len(df) * 100:.1f}%)\n")
        f.write(f"Average Themes per Review: {df['num_themes'].mean():.2f}\n\n")
        
        # Overall theme summary
        f.write("-" * 80 + "\n")
        f.write("OVERALL THEME DISTRIBUTION\n")
        f.write("-" * 80 + "\n")
        
        all_themes = []
        for themes in df['themes']:
            all_themes.extend(themes)
        
        theme_counts = Counter(all_themes)
        for theme, count in theme_counts.most_common():
            percentage = (count / len(df)) * 100
            f.write(f"{theme:.<50} {count:>5} ({percentage:>5.1f}%)\n")
        
        # Bank-specific analysis
        for bank in df['bank'].unique():
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"{bank}\n")
            f.write("=" * 80 + "\n\n")
            
            bank_df = df[df['bank'] == bank]
            
            # Top keywords
            f.write("Top Keywords (TF-IDF):\n")
            if bank in bank_keywords:
                for keyword, score in bank_keywords[bank][:10]:
                    f.write(f"  • {keyword}: {score:.4f}\n")
            
            # Themes
            f.write("\nTheme Distribution:\n")
            bank_themes = []
            for themes in bank_df['themes']:
                bank_themes.extend(themes)
            
            bank_theme_counts = Counter(bank_themes)
            for theme, count in bank_theme_counts.most_common():
                percentage = (count / len(bank_df)) * 100
                f.write(f"  • {theme}: {count} ({percentage:.1f}%)\n")
            
            # Example reviews for top theme
            if bank_theme_counts:
                top_theme = bank_theme_counts.most_common(1)[0][0]
                f.write(f"\nExample reviews for '{top_theme}':\n")
                
                theme_reviews = bank_df[bank_df['themes'].apply(lambda x: top_theme in x)]
                for idx, row in theme_reviews.head(3).iterrows():
                    f.write(f"  {idx+1}. \"{row['review'][:100]}...\"\n")
                    f.write(f"     Rating: {row['rating']}, Sentiment: {row['sentiment_label']}\n\n")
    
    print(f"✓ Saved theme analysis report to {report_path}")

if __name__ == "__main__":
    df_with_themes = main()
    print("\n✓ Thematic analysis completed successfully!")
