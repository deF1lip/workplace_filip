import streamlit as st

# Initialization of session state variables
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Example roommates list


# Upload-Widget für die Rechnung
uploaded_file = st.file_uploader("Upload an image of your receipt", type=["jpg", "jpeg", "png"])

