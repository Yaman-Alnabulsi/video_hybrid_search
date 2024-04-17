import os
import weaviate
import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# load env variables
load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_APIKEY = os.getenv("WEAVIATE_APIKEY")
DEFAULT_WIDTH = 60
DEFAULT_LIMIT = 3
DEFAULT_ALPHA = 0.5

data_dir = os.path.join("data")

# Load Embedding Model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Connect To weaviate
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.auth.AuthApiKey(api_key=WEAVIATE_APIKEY),
)

def shorten_youtube_url(url):
    """
    Shortens a YouTube URL to the format 'https://youtu.be/video_id'

    Args:
    url (str): The YouTube URL to be shortened.

    Returns:
    str: The shortened YouTube URL.
    """
    if "youtube.com/watch?v=" in url:
        video_id = url.split("v=")[1]
        shortened_url = f"https://youtu.be/{video_id}"
        return shortened_url
    else:
        return "Invalid YouTube URL"

st.set_page_config(
    page_title="Search Videos",
    page_icon="🔍",
    layout="wide"
)

st.title("Search Videos 🔍")

with st.container():
    text_search = st.text_input("Write a query", value="graph databases")
    # width = st.sidebar.slider(
    #     label="Width", min_value=0, max_value=100, value=DEFAULT_WIDTH, format="%d%%"
    # )

    width = DEFAULT_WIDTH

    limit = st.sidebar.slider(
        label="Number of results to display", min_value=1, step=1, value=DEFAULT_LIMIT, format="%d"
    )

    alpha = st.sidebar.slider(
        label="alpha", min_value=0.0, max_value=1.0, step=0.01, value=DEFAULT_ALPHA, format="%f"
    )

    st.sidebar.info(
        """
        weighting for each search algorithm:
        - An alpha of 1 is a pure vector search (semantic search).
        - An alpha of 0 is a pure keyword search.
        """,
        icon="ℹ️"
    )
    

    if text_search:
        with st.spinner("Wait for it..."):
            query_vector = model.encode([text_search]).tolist()[0]
            response = (
                client.query
                .get("Video", ["title", "description", "url"])
                .with_hybrid(
                    query=text_search,
                    vector=query_vector,
                    alpha=alpha # An alpha of 1 is a pure vector search (semantic search).
                                # An alpha of 0 is a pure keyword search.
                )
                .with_limit(limit)
                .do()
            )
        
        videos = response.get("data").get("Get").get("Video")

        for video in videos:
            title = video.get("title")
            url = video.get("url")
            short_url = shorten_youtube_url(url)
            st.markdown(f"### {title}")

            width = max(width, 0.01)
            side = max((100 - width) / 2, 0.01)
            container, _, _ = st.columns([width, side, side])
            container.video(data=short_url)

            st.divider()
