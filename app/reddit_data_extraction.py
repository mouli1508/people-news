
import requests
import praw
import json
from datetime import datetime

class RedditDataExtractor:
    def __init__(self, search_api_key, search_engine_id, reddit_client_id, reddit_client_secret, reddit_user_agent):
        self.google_api_key = search_api_key
        self.search_engine_id = search_engine_id
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent,
        )

    def get_reddit_urls(self, query, max_results=20):
        url = "https://www.googleapis.com/customsearch/v1"
        reddit_urls = []
        for start in range(1, max_results + 1, 10):  # Incrementing by 10 for pagination
            params = {
                'key': self.google_api_key,
                'cx': self.search_engine_id,
                'q': f"{query} site:reddit.com",
                'num': 10,
                'start': start,
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results = response.json()
                for item in results.get('items', []):
                    link = item.get('link')
                    if 'reddit.com' in link:
                        reddit_urls.append(link)
            else:
                print(f"Error: {response.status_code}, {response.text}")
                break  # Stop if there's an error
        return reddit_urls

    @staticmethod
    def convert_utc_to_datetime(utc_timestamp):
        """Convert UTC timestamp to readable date and time."""
        return datetime.fromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def fetch_comments(self, submission, max_comments=10):
        """Fetch top comments for a Reddit submission."""
        comments_data = []
        submission.comments.replace_more(limit=0)  # Load all comments
        comments = submission.comments.list()
        for comment in comments:
            if comment and hasattr(comment, 'body'):
                comments_data.append({
                    'comment_body': comment.body,
                    'comment_author': str(comment.author) if comment.author else "N/A",
                    'comment_score': comment.score,
                    'comment_created_utc': comment.created_utc,
                    'comment_created_dt': self.convert_utc_to_datetime(comment.created_utc)
                })
        return comments_data

    def fetch_reddit_data_from_urls(self, urls, max_comments_per_post=10, output_file="reddit_data.json"):
        """Fetch Reddit data from a list of URLs."""
        posts_data = []

        for url in urls:
            try:
                # Extract submission from the URL
                submission = self.reddit.submission(url=url)
                if submission and hasattr(submission, 'title'):
                    post = {
                        'title': submission.title,
                        'selftext': submission.selftext if submission.selftext else "N/A",
                        'url': submission.url,
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'created_utc': submission.created_utc,
                        'created_dt': self.convert_utc_to_datetime(submission.created_utc),
                        'author': str(submission.author) if submission.author else "N/A",
                        'subreddit': str(submission.subreddit),
                        'comments': self.fetch_comments(submission)
                    }
                    posts_data.append(post)
            except Exception as e:
                print(f"Error fetching data for URL: {url}. Error: {e}")

        # Save the data to a JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(posts_data, f, ensure_ascii=False, indent=4)

        print(f"Data saved to {output_file}")
