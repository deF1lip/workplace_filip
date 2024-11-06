import streamlit as st

# intiatlisierung 
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {"Tomato", "Banana,"} # Example roommates list
