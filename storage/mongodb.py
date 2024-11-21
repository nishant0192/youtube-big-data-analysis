from pymongo import MongoClient, errors

# Initialize MongoDB client and database
try:
    # Use Docker's MongoDB hostname
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["youtube_data"]
    comments_collection = db["comments"]
    videos_collection = db["videos"]
    print("Connected to MongoDB successfully.")
except errors.ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")
    raise


def store_comments(comments):
    """Store comments in MongoDB."""
    if not comments:
        print("No comments to store.")
        return

    try:
        operations = [
            {
                "updateOne": {
                    "filter": {"video_id": comment["video_id"], "comment": comment["comment"]},
                    "update": {"$setOnInsert": comment},
                    "upsert": True
                }
            }
            for comment in comments
        ]
        comments_collection.bulk_write(operations)
        print(f"Stored {len(comments)} comments.")
    except Exception as e:
        print(f"Error storing comments: {e}")


def fetch_comments(filter_query=None):
    """Fetch comments from MongoDB."""
    try:
        return list(comments_collection.find(filter_query or {}))
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []


def store_videos(videos):
    """Store videos in MongoDB."""
    if not videos:
        print("No videos to store.")
        return

    try:
        operations = [
            {
                "updateOne": {
                    "filter": {"video_id": video["video_id"]},
                    "update": {"$set": video},
                    "upsert": True
                }
            }
            for video in videos
        ]
        if operations:
            videos_collection.bulk_write(operations)
            print(f"Stored {len(videos)} videos in MongoDB.")
    except Exception as e:
        print(f"Error storing videos: {e}")



def fetch_videos():
    """Fetch videos from MongoDB."""
    try:
        return list(videos_collection.find())
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []
