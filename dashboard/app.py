import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from datetime import datetime
from api.fetch_metadata import fetch_videos_by_category, fetch_playlist_videos, fetch_channel_videos
from api.fetch_comments import fetch_comments_from_youtube

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Streamlit App Title
st.title("YouTube Big Data Analysis Dashboard")

# Sidebar Configuration
st.sidebar.header("Configuration")
data_type = st.sidebar.selectbox(
    "Choose what to fetch:",
    ["Video Comments", "Playlist Comments", "Channel Comments", "Top Videos"]
)
input_id = st.sidebar.text_input(
    "Enter YouTube Video ID, Playlist ID, or Channel ID (Optional for Top Videos):",
    placeholder="E.g., cc6Y4LbmiLU or PL12345..."
)

time_filter = st.sidebar.radio(
    "Select Time Interval for Analysis:",
    ["Daily", "Monthly", "Yearly"]
)

# Fetch and Analyze Data Button
if st.sidebar.button("Fetch and Analyze Data"):
    if not API_KEY:
        st.error("API key not found. Please add your API key in a .env file.")
    elif data_type != "Top Videos" and not input_id:
        st.error("Please enter a valid ID for fetching comments or videos.")
    else:
        st.info("Fetching data... this may take some time.")
        try:
            if data_type == "Video Comments":
                fetch_comments_from_youtube(video_id=input_id, api_key=API_KEY)
                st.success(f"Comments fetched for Video ID: {input_id}")
            elif data_type == "Playlist Comments":
                videos = fetch_playlist_videos(playlist_id=input_id, api_key=API_KEY)
                for video in videos:
                    fetch_comments_from_youtube(video_id=video["videoId"], api_key=API_KEY)
                st.success(f"Comments fetched for Playlist ID: {input_id}")
            elif data_type == "Channel Comments":
                videos = fetch_channel_videos(channel_id=input_id, api_key=API_KEY)
                for video in videos:
                    fetch_comments_from_youtube(video_id=video["videoId"], api_key=API_KEY)
                st.success(f"Comments fetched for Channel ID: {input_id}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Fetch Top Videos from YouTube API
if data_type == "Top Videos":
    st.info("Fetching Top Videos directly from YouTube API...")
    categories = [
        {"id": "10", "title": "Music"},
        {"id": "20", "title": "Gaming"},
        {"id": "24", "title": "Entertainment"}
    ]  # Example categories
    all_videos = []

    try:
        for category in categories:
            videos = fetch_videos_by_category(
                api_key=API_KEY, category_id=category["id"], region_code="US", max_results=10
            )
            for video in videos:
                video["category"] = category["title"]
            all_videos.extend(videos)

        # Convert to DataFrame
        video_df = pd.DataFrame(all_videos)

        # Top Videos Section
        st.subheader("Top Videos by Views (Fetched from YouTube API)")
        top_videos_fig = px.bar(
            video_df,
            x="title",
            y="views",
            color="category",
            title="Top Videos by Views",
            labels={"title": "Video Title", "views": "Number of Views", "category": "Category"}
        )
        st.plotly_chart(top_videos_fig)

        # Video Selector for Detailed Analysis
        selected_video = st.selectbox(
            "Select a Video for Detailed Analysis:", video_df["title"]
        )

        # Analyze the selected video
        selected_video_data = video_df[video_df["title"] == selected_video].iloc[0]
        st.write(f"**Title:** {selected_video_data['title']}")
        st.write(f"**Views:** {selected_video_data['views']:,}")
        st.write(f"**Likes:** {selected_video_data['likes']:,}")
        st.write(f"**Comments:** {selected_video_data['comments']:,}")

        # Display published date
        st.write(f"**Published Date:** {selected_video_data['published_at']}")

    except Exception as e:
        st.error(f"An error occurred while fetching top videos: {e}")
