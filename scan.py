import streamlit as st

# Initialization of session state variables
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Example roommates list


# Upload-Widget für die Rechnung
uploaded_file = st.file_uploader("Upload an image of your receipt", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Lade das Bild und zeige es an
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Receipt', use_column_width=True)