import streamlit as st
from PIL import Image
import pytesseract
import re

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Initialization of session state variables
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]

# Upload widget for the receipt
uploaded_file = st.file_uploader("Upload an image of your receipt", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Receipt', use_column_width=True)

    # Apply OCR (text recognition) to the image
    st.write("Extracting text from the receipt...")
    text = pytesseract.image_to_string(image)

    # Display the extracted text
    st.write("Extracted Text:")
    st.write(text)

    # Function to extract items, quantities, and prices
    def extract_items(text):
        items = []
        lines = text.splitlines()
        for line in lines:
            # Regex to extract item name, quantity, and price
            match = re.search(r'(\D+)\s+(\d+)\s+(?:CHF|chf|€|eur)?\s?(\d+[\.,]?\d*)', line, re.IGNORECAS)

