import streamlit as st

st.set_page_config (page_title = "File Uploader")

datafile = st.file_uploader(label = "Upload your receipt")