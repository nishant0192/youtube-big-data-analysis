from googleapiclient.discovery import build

def fetch_videos_by_category(api_key, category_id=None, region_code="US", max_results=50):
    """
    Fetch trending videos by category ID or region.

    Parameters:
    - api_key: Your YouTube Data API key.
    - category_id: The ID of the video category (e.g., Music: "10", Gaming: "20").
    - region_code: The region to fetch videos for (default: "US").
    - max_results: The maximum number of videos to fetch (default: 50).

    Returns:
    - List of video metadata, including title, views, and video ID.
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        videoCategoryId=category_id,
        maxResults=max_results
    )
    response = request.execute()

    videos = [
        {
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "views": int(item["statistics"]["viewCount"]),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0)),
            "category_id": category_id,
            "published_at": item["snippet"]["publishedAt"]
        }
        for item in response["items"]
    ]
    return videos


def fetch_playlist_videos(playlist_id, api_key):
    """Fetch videos from a YouTube playlist."""
    youtube = build("youtube", "v3", developerKey=api_key)
    videos = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails", playlistId=playlist_id, maxResults=50
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append({
                "videoId": item["contentDetails"]["videoId"],
                "title": item["snippet"]["title"]
            })
        request = youtube.playlistItems().list_next(request, response)
    return videos


def fetch_channel_videos(channel_id, api_key):
    """Fetch videos from a YouTube channel."""
    youtube = build("youtube", "v3", developerKey=api_key)
    videos = []
    request = youtube.search().list(
        part="snippet", channelId=channel_id, maxResults=50, type="video"
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append({
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"]
            })
        request = youtube.search().list_next(request, response)
    return videos
