import pandas as pd
import psycopg2
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.data.path.append('/home/mehlika/nltk_data')

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# PostgreSQL connection
db_params = {
    'host': 'localhost',
    'database': 'nikedb',
    'user': 'nikeuser',
    'password': '1234'
}
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Fetch data
df = pd.read_sql_query("SELECT id, full_text_cleaned FROM nike_posts;", conn)

# Fill NaN with empty string just in case
df['full_text_cleaned'] = df['full_text_cleaned'].fillna("")

# Sentiment scoring
def get_sentiment(row):
    scores = analyzer.polarity_scores(row['full_text_cleaned'])
    compound = scores['compound']
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    return pd.Series([scores['neg'], scores['neu'], scores['pos'], compound, label])

df[['sentiment_neg', 'sentiment_neu', 'sentiment_pos', 'sentiment_compound', 'sentiment_label']] = df.apply(get_sentiment, axis=1)
print("Sentiment scores calculated.")

# Add columns if not exists
try:
    cursor.execute("ALTER TABLE nike_posts ADD COLUMN IF NOT EXISTS sentiment_neg DOUBLE PRECISION;")
    cursor.execute("ALTER TABLE nike_posts ADD COLUMN IF NOT EXISTS sentiment_neu DOUBLE PRECISION;")
    cursor.execute("ALTER TABLE nike_posts ADD COLUMN IF NOT EXISTS sentiment_pos DOUBLE PRECISION;")
    cursor.execute("ALTER TABLE nike_posts ADD COLUMN IF NOT EXISTS sentiment_compound DOUBLE PRECISION;")
    cursor.execute("ALTER TABLE nike_posts ADD COLUMN IF NOT EXISTS sentiment_label TEXT;")
    conn.commit()
    print(" Columns ensured in table.")
except Exception as e:
    print(f" Column creation error: {e}")
    conn.rollback()

# Update rows
success = 0
fail = 0

for i, row in df.iterrows():
    try:
        cursor.execute(
            """
            UPDATE nike_posts
            SET sentiment_neg = %s,
                sentiment_neu = %s,
                sentiment_pos = %s,
                sentiment_compound = %s,
                sentiment_label = %s
            WHERE id = %s;
            """,
            (
                float(row['sentiment_neg']),
                float(row['sentiment_neu']),
                float(row['sentiment_pos']),
                float(row['sentiment_compound']),
                row['sentiment_label'],
                row['id']
            )
        )
        conn.commit()
        success += 1
    except Exception as e:
        conn.rollback()
        print(f" Failed on id {row['id']}: {e}")
        fail += 1

print(f"\n {success} rows updated successfully.")
print(f" {fail} rows failed to update.")

cursor.close()
conn.close()
