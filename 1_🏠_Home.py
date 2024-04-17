import streamlit as st


st.set_page_config(
    page_title="Video Hybrid Search (Semantic + Keyword)",
    page_icon="🏠",
    layout="wide"
)

st.title("Video Hybrid Search (Semantic + Keyword)")

introduction = """
## Introduction

Welcome to **Video Hybrid Search**! This Streamlit application allows you to perform hybrid search on videos using a weaviate (Vector Database). By leveraging semantic search with keyword search techniques, you can find videos based on their meaning rather than just keywords.
"""

used_tech = """
## Technologies Used

- **Streamlit**: This application is built using Streamlit, a powerful framework for creating data-centric web applications with simple Python scripts.

- **Weaviate (Vector Database)**: The semantic search functionality is powered by Weaviate, a vector database that enables efficient storage and retrieval of vectorized data.

- **Sentence Transformer (all-MiniLM-L6-v2 model)**: This model is used to convert textual data into numerical vectors, facilitating semantic similarity calculations. It plays a crucial role in enabling effective semantic search capabilities within the application.

"""

with st.container():
    st.markdown(introduction)
    start = st.button("Getting Started", type="primary")
    if start:
        st.switch_page(page="pages/3_🔍_Search.py")
    st.markdown(used_tech)
