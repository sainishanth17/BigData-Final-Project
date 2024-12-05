'''
import praw
import pandas as pd
import time
from datetime import datetime

reddit = praw.Reddit(
    client_id='xmohPv0Yc8U5g4ROJxjJKQ',
    client_secret='roZdn2iBP9ajSJZLQfhA8INw4eRwAA',
    user_agent='political_sentiment_analysis by u/davaibratan'
)

START_DATE = '2023-01-01'
END_DATE = '2024-11-11'
start_time = int(time.mktime(time.strptime(START_DATE, "%Y-%m-%d")))
end_time = int(time.mktime(time.strptime(END_DATE, "%Y-%m-%d")))


existing_csv = "reddit_data_filtered.csv"
if existing_csv:
    try:
        existing_df = pd.read_csv(existing_csv)
        processed_ids = set(existing_df["id"])
    except FileNotFoundError:
        processed_ids = set()
else:
    processed_ids = set()
    

def fetch_posts_and_comments(topic, subreddits):
    all_data = []
    query = f"{topic} timestamp:{start_time}..{end_time}"

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        print(f"Fetching posts from r/{subreddit_name} for topic '{topic}'...")

        # Fetch posts with 'top' sort
        for submission in subreddit.search(query, sort="controversial", limit=100):
            if submission.id in processed_ids:
                continue  # skip posts already seen

            post_data = {
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "comments_count": submission.num_comments,
                "created_utc": datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                "subreddit": subreddit_name,
                "url": submission.url,
                "topic": topic
            }

            # fetch comments for each post
            submission.comments.replace_more(limit=0)
            comments = [comment.body for comment in submission.comments.list()]
            post_data["comments"] = comments

            all_data.append(post_data)
            processed_ids.add(submission.id)  # Add Post ID to processed set

    return all_data


'''
topics = {
    'Gun Control': ['Firearms', 'GunControl', 'SecondAmendment', 'Politics', 'News'],
    'Abortion': ['AbortionDebate', 'ProLife', 'ProChoice', 'Politics', 'News'],
    'Racial Inequality': ['BlackLivesMatter', 'SocialJustice', 'Racism', 'Politics', 'News'],
    'Climate Change': ['ClimateChange', 'Sustainability', 'EnvironmentalScience', 'Politics', 'News']
}
'''



new_topics_list_1 = ['WorldNews', 'TheDonald', 'conservative', 'progressive', 'democrats', 'liberal']
new_topics_list_2 = ['AskReddit', 'History', 'Law', 'Entertainment', 'Popculturechat', 'Philosophy', 'funny', 'jokes', 'skeptic', 'outoftheloop', 'facepalm', 'mildlyinfuriating']

topics = {
    'Gun Control': new_topics_list_2,
    'Abortion': new_topics_list_2,
    'Racial Inequality': new_topics_list_2,
    'Climate Change': new_topics_list_2
}



final_data = []
for topic, subreddits in topics.items():
    final_data.extend(fetch_posts_and_comments(topic, subreddits))


if final_data:
    new_df = pd.DataFrame(final_data)
    try:
        existing_df = pd.read_csv(existing_csv)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    except FileNotFoundError:
        combined_df = new_df

    combined_df.to_csv(existing_csv, index=False)
    print(f"Data collection complete! Appended to '{existing_csv}'.")
else:
    print("Nothing new.")
'''    
    
    
    
    
    
import praw
import prawcore
import pandas as pd
import time
from datetime import datetime

# Initialize Reddit API credentials
reddit = praw.Reddit(
    client_id='xmohPv0Yc8U5g4ROJxjJKQ',
    client_secret='roZdn2iBP9ajSJZLQfhA8INw4eRwAA',
    user_agent='political_sentiment_analysis by u/davaibratan'
)

# Define date range for the query
START_DATE = '2023-01-01'
END_DATE = '2024-11-11'
start_time = int(time.mktime(time.strptime(START_DATE, "%Y-%m-%d")))
end_time = int(time.mktime(time.strptime(END_DATE, "%Y-%m-%d")))

# File to store results
existing_csv = "reddit_data_filtered.csv"
if existing_csv:
    try:
        existing_df = pd.read_csv(existing_csv)
        processed_ids = set(existing_df["id"])
    except FileNotFoundError:
        processed_ids = set()
else:
    processed_ids = set()

# Function to fetch posts and comments
def fetch_posts_and_comments(topic, subreddit_name, sort_type):
    all_data = []
    query = f"{topic} timestamp:{start_time}..{end_time}"
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        print(f"Fetching '{sort_type}' posts from r/{subreddit_name} for topic '{topic}'...")
        
        for submission in subreddit.search(query, sort=sort_type, limit=100):
            if submission.id in processed_ids:
                continue  # Skip already processed posts
            
            post_data = {
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "comments_count": submission.num_comments,
                "created_utc": datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                "subreddit": subreddit_name,
                "url": submission.url,
                "topic": topic,
            }

            # Fetch comments for each post
            submission.comments.replace_more(limit=0)
            comments = [comment.body for comment in submission.comments.list()]
            post_data["comments"] = comments

            all_data.append(post_data)
            processed_ids.add(submission.id)  # Add Post ID to processed set
    
    except prawcore.exceptions.NotFound:
        print(f"Subreddit '{subreddit_name}' not found. Skipping...")
    except Exception as e:
        print(f"An error occurred with subreddit '{subreddit_name}': {e}")
        

    return all_data


# Subreddits with potential political leanings
political_subreddits = [
    
    'politics', 'news', 'worldnews', 'conservative', 'liberal', 'progressive',
    'democrats', 'Republican', 'Libertarian', 'GreenParty', 'SocialDemocracy',
    'worldpolitics', 'BlackLivesMatter', 'AbortionDebate', 
    'PoliticalHumor', 'ModeratePolitics', 'PoliticalDiscussion', 'worldevents',
    'business', 'economics', 'environment', 'energy', 'law', 'history', 'worldnews2',
    'politics2', 'uspolitics', 'americangovernment', 'lgbtnews', 'worldnews', 'alltheleft',
    'labor', 'democracy', 'freethought', 'equality', 'lgbt'
]

# Sorting methods to iterate through
sort_methods = ['hot', 'top', 'best', 'controversial']

# Topics to search for
topics = ['Gun Control', 'Abortion', 'Racial Inequality', 'Climate Change']

# Main data collection loop
final_data = []
for topic in topics:
    for subreddit in political_subreddits:
        for sort_type in sort_methods:
            # Fetch data for each combination of topic, subreddit, and sort type
            final_data.extend(fetch_posts_and_comments(topic, subreddit, sort_type))
            time.sleep(10)  # Introduce a delay to avoid hitting API limits

# Save the data to the CSV (append if file exists)
if final_data:
    new_df = pd.DataFrame(final_data)
    try:
        existing_df = pd.read_csv(existing_csv)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    except FileNotFoundError:
        combined_df = new_df

    combined_df.to_csv(existing_csv, index=False)
    print(f"Data collection complete! Appended to '{existing_csv}'.")
else:
    print("Nothing new.")
