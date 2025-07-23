import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="nikedb",
    user="nikeuser",
    password="1234"
)

# Fetch the data
query = """
SELECT created_date::date AS date_only, sentiment_label, sentiment_compound, full_text_cleaned
FROM nike_posts
WHERE sentiment_label IS NOT NULL
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Trend Line – Sentiment over time
trend = df.groupby('date_only')['sentiment_compound'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=trend, x='date_only', y='sentiment_compound', marker='o')
plt.title("Average Sentiment Over Time")
plt.xlabel("Date")
plt.ylabel("Avg Sentiment")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("trendline_sentiment.png")
plt.show()

# Bar Chart – Sentiment count
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='sentiment_label', palette='Set2')
plt.title("Sentiment Distribution")
plt.tight_layout()
plt.savefig("sentiment_distribution.png")
plt.show()

# Word Cloud – Positive
positive_text = " ".join(df[df['sentiment_label'] == 'positive']['full_text_cleaned'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Positive Sentiment Word Cloud")
plt.tight_layout()
plt.savefig("positive_wordcloud.png")
plt.show()

# Word Cloud – Negative
negative_text = " ".join(df[df['sentiment_label'] == 'negative']['full_text_cleaned'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='black').generate(negative_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Negative Sentiment Word Cloud")
plt.tight_layout()
plt.savefig("negative_wordcloud.png")
plt.show()
