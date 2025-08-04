import pandas as pd
import numpy as np
import re
import unicodedata
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class NikeDataPreprocessor:
    def __init__(self, csv_file='nike_reddit_data.csv'):
        """Load and initialize the Nike Reddit data from CSV"""
        self.raw_data = None
        self.cleaned_data = None
        self.load_data(csv_file)

    def load_data(self, csv_file):
        """Load and clean data from CSV before processing"""
        try:
            self.df = pd.read_csv(csv_file, encoding='utf-8')
            print(f" Loaded {len(self.df)} posts from {csv_file}")

            # Clean text fields before processing
            for field in ['title', 'selftext', 'full_text']:
                if field in self.df.columns:
                    self.df[field] = self.df[field].astype(str).apply(self.clean_raw_text)

        except Exception as e:
            print(f" Error loading data: {e}")
            self.df = None

    def clean_raw_text(self, text):
        """Remove corrupted Unicode characters and normalize"""
        try:
            text = str(text)
            text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
            return text
        except Exception:
            return ''

    def clean_text(self, text):
        """Clean individual text entries after raw Unicode normalization"""
        if pd.isna(text) or text == '':
            return ''

        text = re.sub(r'http[s]?://\S+', '', text)
        text = re.sub(r'/u/\w+', '', text)
        text = re.sub(r'/r/\w+', '', text)
        text = re.sub(r'\[deleted\]|\[removed\]', '', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', text)

        return text.strip()

    def preprocess_data(self):
        """Main preprocessing pipeline"""
        if self.df is None:
            print(" No data loaded. Cannot preprocess.")
            return None

        print(" Starting data preprocessing...")
        df = self.df.copy()

        print("   Cleaning text fields...")
        df = df[(df['title'].notna()) & (df['title'] != '')]
        df['title_cleaned'] = df['title'].apply(self.clean_text)
        df['selftext_cleaned'] = df['selftext'].apply(self.clean_text)

        df['full_text_cleaned'] = df.apply(
            lambda row: f"{row['title_cleaned']} {row['selftext_cleaned']}".strip(), axis=1
        )
        df = df[df['full_text_cleaned'].str.len() > 10]

        print("\tHandling missing values...")
        df['author'] = df['author'].fillna('[unknown]')
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
        df['num_comments'] = pd.to_numeric(df['num_comments'], errors='coerce').fillna(0)

        print("\tConverting data types...")
        df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')

        print("\tRemoving duplicates...")
        initial = len(df)
        df = df.drop_duplicates(subset=['id'])
        df = df.drop_duplicates(subset=['full_text_cleaned'])
        print(f"    Removed {initial - len(df)} duplicate posts")

        print("\tAdding derived features...")
        df['text_length'] = df['full_text_cleaned'].str.len()
        df['word_count'] = df['full_text_cleaned'].str.split().str.len()
        df['engagement_score'] = df['score'] + (df['num_comments'] * 2)
        df['date_only'] = df['created_date'].dt.date
        df['hour'] = df['created_date'].dt.hour
        df['day_of_week'] = df['created_date'].dt.day_name()

        print("\tFiltering quality content...")
        df = df[df['word_count'] >= 3]
        df = df[df['score'] >= -50]

        self.cleaned_data = df.reset_index(drop=True)
        print(f" Preprocessing completed: {len(self.cleaned_data)} clean posts")
        return self.cleaned_data

    def save_cleaned_data(self, filename='nike_cleaned_data.csv'):
        """Save cleaned data to CSV"""
        if self.cleaned_data is None:
            print("No cleaned data available. Run preprocess_data() first.")
            return
        try:
            self.cleaned_data.to_csv(filename, index=False, encoding='utf-8')
            print(f"Cleaned data saved to {filename}")

            summary_file = filename.replace('.csv', '_summary.txt')
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("Nike Reddit Data Cleaning Summary\n")
                f.write("="*40 + "\n")
                f.write(f"Original posts: {len(self.df)}\n")
                f.write(f"Cleaned posts: {len(self.cleaned_data)}\n")
                f.write(f"Retained: {len(self.cleaned_data)/len(self.df)*100:.1f}%\n\n")
                f.write("Columns:\n")
                for col in self.cleaned_data.columns:
                    f.write(f" - {col}\n")
            print(f" Summary saved to {summary_file}")
        except Exception as e:
            print(f" Error saving data: {e}")

def main():
    print(" Nike Data Preprocessing Pipeline")
    print("=" * 50)

    preprocessor = NikeDataPreprocessor('nike_reddit_data.csv')
    cleaned = preprocessor.preprocess_data()

    if cleaned is not None:
        preprocessor.save_cleaned_data()
        print("\n Preprocessing complete. Cleaned CSV ready.")
    else:
        print(" Preprocessing failed.")

main()
