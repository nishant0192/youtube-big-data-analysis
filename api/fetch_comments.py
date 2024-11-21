from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from storage.mongodb import store_comments

def fetch_comments_from_youtube(video_id, api_key):
    """Fetch and analyze YouTube comments."""
    analyzer = SentimentIntensityAnalyzer()
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet", videoId=video_id, maxResults=100
        )
        while request:
            response = request.execute()
            for item in response["items"]:
                text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                scores = analyzer.polarity_scores(text)
                sentiment = "Neutral"
                if scores['compound'] >= 0.05:
                    sentiment = "Positive"
                elif scores['compound'] <= -0.05:
                    sentiment = "Negative"
                comments.append({
                    "comment": text,
                    "video_id": video_id,
                    "timestamp": item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                    "sentiment": sentiment,
                })
            request = youtube.commentThreads().list_next(request, response)
    except Exception as e:
        print(f"Error fetching comments: {e}")

    # Store comments only if data exists
    if comments:
        store_comments(comments)
        print(f"Fetched and stored {len(comments)} comments for video ID {video_id}.")
    else:
        print(f"No comments found for video ID {video_id}.")

