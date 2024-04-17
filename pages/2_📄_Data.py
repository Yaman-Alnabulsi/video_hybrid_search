import os
import pandas as pd
import streamlit as st

data_dir = os.path.join("data")

st.set_page_config(
    page_title="Preview Data",
    page_icon="📄",
    layout="wide"
)

st.title("Preview Data 📄")

with st.container():
    with st.spinner():
        st.dataframe(pd.read_json(os.path.join(data_dir, "youtube_data.json"), orient="records"))
