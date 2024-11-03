import streamlit as st

st.set_page_config (page_title = "File Uploader")

datafile = st.file_uploaer(label = "Upload your receipt")