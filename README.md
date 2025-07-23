# Nike Reddit Sentiment Analysis

A comprehensive data science project analyzing public sentiment about Nike brand using Reddit discussions through Natural Language Processing (NLP) and sentiment analysis techniques.

## Project Overview

This project extracts and analyzes consumer sentiment from Reddit posts mentioning Nike, providing actionable insights for brand positioning, marketing strategies, and customer experience improvements.

### Key Features
- **Real-time Reddit data collection** via Reddit API
- **Advanced text preprocessing** and cleaning pipeline
- **VADER sentiment analysis** for emotion classification
- **PostgreSQL database** integration for structured storage
- **Interactive visualizations** and word clouds
- **Comprehensive SQL analytics** for business insights

## Business Value

- **Brand Monitoring**: Real-time sentiment tracking across social platforms
- **Consumer Insights**: Understanding customer pain points and preferences
- **Marketing Intelligence**: Identifying optimal engagement timing and messaging
- **Product Feedback**: Direct consumer opinions on specific Nike products
- **Crisis Management**: Early detection of negative sentiment trends

## Key Findings

From our analysis of **603 Reddit posts**:
- **50%+ positive sentiment** indicating strong brand affinity
- **Peak engagement** around product release dates (May 31, June 11)
- **Common praise**: Product quality, comfort, design aesthetics
- **Pain points**: Packaging issues, sizing accuracy, counterfeit concerns
- **High-engagement days**: Fridays and Sundays optimal for marketing

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.8+ |
| **Data Collection** | Reddit API (PRAW) |
| **Database** | PostgreSQL |
| **Sentiment Analysis** | NLTK VADER |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, WordCloud |
| **Environment** | Ubuntu VM |

## Project Structure

```
nike-reddit-sentiment/
│
├── data/
│   ├── nike_reddit_data.csv          # Raw collected data
│   ├── nike_cleaned_data.csv         # Preprocessed data
│   └── sentiment_results.csv         # Sentiment analysis results
│
├── src/
│   ├── nike_reddit_collector.py      # Reddit API data collection
│   ├── nike_data_preprocessor.py     # Text cleaning pipeline
│   ├── sentiment_analysis.py         # VADER sentiment scoring
│   └── visualize_sentiment.py        # Visualization generation
│
├── visualizations/
│   ├── sentiment_distribution.png
│   ├── trendline_sentiment.png
│   ├── positive_wordcloud.png
│   ├── negative_wordcloud.png
│   └── nike_data_overview.png
│
├── sql/
│   └── analysis_queries.sql          # Business intelligence queries
│
├── docs/
│   └── Social_Media_Sentiment_Analysis_Report.pdf
│
└── README.md
```

## Getting Started

### Prerequisites

```bash
# Python 3.8+
python --version

# PostgreSQL
sudo apt-get install postgresql postgresql-contrib
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/mehlikaakbay/nike-reddit-sentiment.git
cd nike-reddit-sentiment
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL database**
```bash
sudo -u postgres createdb nikedb
sudo -u postgres createuser nikeuser
sudo -u postgres psql -c "ALTER USER nikeuser PASSWORD '1234';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE nikedb TO nikeuser;"
```
   - **Note**: The project uses hardcoded database credentials (user: `nikeuser`, password: `1234`)
   - For production use, consider using environment variables for security

4. **Configure Reddit API credentials**
   - The project includes Reddit API credentials in `nike_reddit_collector.py`
   - Update the `REDDIT_CONFIG` dictionary with your own Reddit app credentials:
   ```python
   REDDIT_CONFIG = {
       'client_id': 'your_client_id_here',
       'client_secret': 'your_client_secret_here',
       'user_agent': 'NikeSentimentAnalysis:v1.0 (by /u/YourUsername)'
   }
   ```
   - Create a Reddit app at https://www.reddit.com/prefs/apps if you need new credentials

### Dependencies

Create a `requirements.txt` file with these dependencies:
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
praw>=7.4.0
psycopg2-binary>=2.9.0
nltk>=3.6.0
wordcloud>=1.8.0
emoji>=2.0.0
```

Or install manually:
```bash
pip install pandas numpy matplotlib seaborn
pip install praw psycopg2-binary nltk wordcloud emoji
```

## Usage

### 1. Data Collection
```bash
python src/nike_reddit_collector.py
```
- Collects Nike-related posts from specified subreddits
- Searches using keywords: "Nike", "Air Jordan", "Nike Dunk", etc.
- Saves raw data to `nike_reddit_data.csv`

### 2. Data Preprocessing
```bash  
python src/nike_data_preprocessor.py
```
- Cleans and normalizes text data
- Removes URLs, mentions, deleted content
- Creates derived features (word count, engagement score)
- Outputs `nike_cleaned_data.csv`

### 3. Sentiment Analysis
```bash
python src/sentiment_analysis.py
```
- Applies VADER sentiment scoring
- Classifies posts as positive/neutral/negative
- Updates PostgreSQL database with sentiment scores

### 4. Generate Visualizations
```bash
python src/visualize_sentiment.py
```
- Creates sentiment distribution charts
- Generates trend analysis plots
- Produces positive/negative word clouds

## Sample Visualizations

### Sentiment Distribution
![Sentiment Distribution](visualizations/sentiment_distribution.png)

### Sentiment Trends Over Time
![Sentiment Trends](visualizations/trendline_sentiment.png)

### Word Clouds
| Positive Sentiment | Negative Sentiment |
|:------------------:|:------------------:|
| ![Positive](visualizations/positive_wordcloud.png) | ![Negative](visualizations/negative_wordcloud.png) |

## SQL Analytics

Key business intelligence queries included:

```sql
-- Average engagement metrics
SELECT AVG(score) as avg_score, 
       AVG(num_comments) as avg_comments,
       AVG(score + num_comments * 2) as avg_engagement
FROM nike_posts;

-- Sentiment distribution by day
SELECT DATE(created_date) as post_date,
       sentiment_label,
       COUNT(*) as post_count
FROM nike_posts 
GROUP BY post_date, sentiment_label;

-- Top performing posts
SELECT title, score, num_comments, sentiment_label
FROM nike_posts 
ORDER BY score DESC 
LIMIT 10;
```

## Key Insights & Recommendations

### Strengths to Leverage
- Strong positive sentiment around product quality and comfort
- High engagement on product release days
- Effective branding with "Air Max" and "Jordan" lines

### Areas for Improvement
- Address packaging and shipping concerns
- Improve sizing accuracy communication
- Combat counterfeit product issues
- Enhance return policy transparency

### Strategic Timing
- Plan social campaigns around Fridays/Sundays
- Amplify marketing during product launch periods
- Monitor sentiment dips for proactive response

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request



**University of Europe for Applied Sciences - Big Data & Analytics**
**Supervisor**: Ali VAISIFARD

## Contact

For questions about this project, please reach out via:
mehlika.akbay@ue-germay.de 

## Acknowledgments

- Reddit API and PRAW library developers
- NLTK team for VADER sentiment analysis
- University of Europe for Applied Sciences
- Nike brand for inspiration

---

** Data Ethics Notice**: This project uses publicly available Reddit data in compliance with Reddit's API terms of service and data usage policies. No personal information is stored or analyzed.
