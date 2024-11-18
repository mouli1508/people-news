import praw
import pandas as pd
from datetime import datetime

# Initialize PRAW with your Reddit credentials
reddit = praw.Reddit(
    client_id="Pr-co5-36bkZzmAr-amBZg",
    client_secret="LhMeEf7Hy9LJS20uJWCwQQWYGWunlQ",
    user_agent="Alternative-Bag-3334"
)

def convert_utc_to_datetime(utc_timestamp):
    """Convert UTC timestamp to readable date and time."""
    return datetime.fromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def fetch_comments(submission, max_comments=10):
    # Retrieve top comments for the post
    comments_data = []
    submission.comments.replace_more(limit=0)  # Load all comments
    comments = submission.comments.list()[:max_comments]
    for comment in comments:
        if comment and hasattr(comment, 'body'):
            comments_data.append({
                'comment_body': comment.body,
                'comment_author': str(comment.author) if comment.author else "N/A",
                'comment_score': comment.score,
                'comment_created_utc': comment.created_utc,
                'comment_created_dt': convert_utc_to_datetime(comment.created_utc)
            })
    return comments_data

def search_reddit_posts(keyword, max_posts=5, max_comments=10):
    posts_data = []

    # Search for posts containing the keyword
    for submission in reddit.subreddit("all").search(keyword, limit=max_posts):
        if submission and hasattr(submission, 'title'):
            post = {
                'keyword': keyword,
                'title': submission.title,
                'selftext': submission.selftext if submission.selftext else "N/A",
                'url': submission.url,
                'score': submission.score,
                'num_comments': submission.num_comments,
                'created_utc': submission.created_utc,
                'created_dt': convert_utc_to_datetime(submission.created_utc),
                'author': str(submission.author) if submission.author else "N/A",
                'subreddit': str(submission.subreddit)
            }
            post['comments'] = fetch_comments(submission, max_comments)
            posts_data.append(post)

    return posts_data

def fetch_posts_for_keywords(keywords, max_posts_per_keyword=5, max_comments_per_post=10, output_file="reddit_posts.csv"):
    all_posts = []

    # Iterate over each keyword and fetch posts
    for keyword in keywords:
        print(f"Fetching posts for keyword: {keyword}")
        posts_data = search_reddit_posts(keyword, max_posts=max_posts_per_keyword, max_comments=max_comments_per_post)
        
        if posts_data:
            all_posts.extend(posts_data)

    # Convert all posts to a flat DataFrame format
    flat_data = []
    for post in all_posts:
        for comment in post['comments']:
            flat_data.append({
                'keyword': post['keyword'],
                'post_title': post['title'],
                'post_text': post['selftext'],
                'post_url': post['url'],
                'post_score': post['score'],
                'post_num_comments': post['num_comments'],
                'post_created_utc': post['created_utc'],
                'post_created_dt': post['created_dt'],
                'post_author': post['author'],
                'post_subreddit': post['subreddit'],
                'comment_body': comment.get('comment_body', "N/A"),
                'comment_author': comment.get('comment_author', "N/A"),
                'comment_score': comment.get('comment_score', 0),
                'comment_created_utc': comment.get('comment_created_utc', "N/A"),
                'comment_created_dt': comment.get('comment_created_dt', "N/A")
            })

    # Create DataFrame from flattened data
    posts_df = pd.DataFrame(flat_data)

    # Save DataFrame to CSV
    posts_df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

# Define keywords and execute the function
keywords = ["Chatgpt", "Robotics", "Employment"]
fetch_posts_for_keywords(keywords, max_posts_per_keyword=5, max_comments_per_post=10, output_file="reddit_posts.csv")
