import praw
import pandas as pd
from datetime import datetime, timezone
import time

REDDIT_CONFIG = {
    'client_id': 'Ioe8HE1SpLStziNsmvai2Q',
    'client_secret': 'InSUZ67fpbIW1snh2SxC2AJvgwX8LQ',
    'user_agent': 'NikeSentimentAnalysis:v1.0 (by /u/MehlikaAnalyze)'
}

class NikeRedditCollector:
    def __init__(self, config):
        self.reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent']
        )
        print(f"Connected to Reddit API")
        print(f"Read-only: {self.reddit.read_only}")

    def collect_nike_posts(self, max_posts=500, subreddits=['all']):
        nike_keywords = [
            'Nike', 'nike', 'Air Jordan', 'air jordan',
            'Nike Air Max', 'nike air max', 'Just Do It',
            'Nike Dunk', 'nike dunk', 'swoosh', 'Nike shoes'
        ]

        all_posts = []

        for keyword in nike_keywords:
            print(f"Searching for: '{keyword}'")

            for subreddit_name in subreddits:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    posts_per_keyword = max_posts // len(nike_keywords)

                    for submission in subreddit.search(
                        keyword,
                        sort='relevance',
                        time_filter='month',
                        limit=posts_per_keyword
                    ):
                        created_time = datetime.fromtimestamp(
                            submission.created_utc,
                            tz=timezone.utc
                        )

                        post_data = {
                            'id': submission.id,
                            'title': submission.title,
                            'selftext': submission.selftext,
                            'author': str(submission.author) if submission.author else '[deleted]',
                            'created_utc': submission.created_utc,
                            'created_date': created_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'score': submission.score,
                            'upvote_ratio': submission.upvote_ratio,
                            'num_comments': submission.num_comments,
                            'subreddit': str(submission.subreddit),
                            'url': submission.url,
                            'permalink': f"https://reddit.com{submission.permalink}",
                            'search_keyword': keyword,
                            'full_text': f"{submission.title} {submission.selftext}".strip()
                        }

                        all_posts.append(post_data)
                        time.sleep(0.1)

                    print(f"   Found {posts_per_keyword} posts in r/{subreddit_name}")

                except Exception as e:
                    print(f"Error searching r/{subreddit_name} for '{keyword}': {e}")
                    continue

        unique_posts = {}
        for post in all_posts:
            if post['id'] not in unique_posts:
                unique_posts[post['id']] = post

        final_posts = list(unique_posts.values())
        print(f"Total unique posts collected: {len(final_posts)}")

        return final_posts

    def save_data(self, posts, filename='nike_reddit_data.csv'):
        try:
            df = pd.DataFrame(posts)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Data saved to {filename}")
            return df

        except Exception as e:
            print(f"Error saving data: {e}")
            return None

    def analyze_initial_data(self, df):
        print("\n" + "=" * 50)
        print("INITIAL DATA ANALYSIS")
        print("=" * 50)

        print(f"Total Posts: {len(df)}")
        print(f"Date Range: {df['created_date'].min()} to {df['created_date'].max()}")
        print(f"Average Score: {df['score'].mean():.2f}")
        print(f"Total Comments: {df['num_comments'].sum()}")

        print("\nTop Subreddits:")
        print(df['subreddit'].value_counts().head(10))

        print("\nSearch Keywords Distribution:")
        print(df['search_keyword'].value_counts())

        print("\nTop Posts by Score:")
        top_posts = df.nlargest(5, 'score')[['title', 'score', 'subreddit']]
        for idx, row in top_posts.iterrows():
            print(f"  • {row['title'][:60]}... (Score: {row['score']}, r/{row['subreddit']})")

def main():
    print("Starting Nike Reddit Data Collection")
    print("=" * 50)

    collector = NikeRedditCollector(REDDIT_CONFIG)

    target_subreddits = ['all']

    posts = collector.collect_nike_posts(
        max_posts=1000,
        subreddits=target_subreddits
    )

    if posts:
        df = collector.save_data(posts)

        if df is not None:
            collector.analyze_initial_data(df)
            print(f"\nData collection completed successfully!")
        else:
            print("Failed to save data")
    else:
        print("No posts collected")


main()
