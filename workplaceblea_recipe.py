import streamlit as st

# intiatlisierung 
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {"Tomato", "Banana,"} # Example roommates list
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Example roommates list