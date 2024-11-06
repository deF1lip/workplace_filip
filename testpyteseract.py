import streamlit as st
from PIL import Image
import pytesseract
import re

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
            match = re.search(r'(\D+)\s+(\d+)\s+(?:CHF|chf|€|eur)?\s?(\d+[\.,]?\d*)', line, re.IGNORECASE)
            if match:
                item_name = match.group(1).strip()
                quantity = int(match.group(2))
                price = float(match.group(3).replace(',', '.'))
                items.append({"Item": item_name, "Quantity": quantity, "Price": price})
        return items

    # Extract information
    items = extract_items(text)

    # Display extracted items
    if items:
        st.write("Extracted Items:")
        for item in items:
            st.write(f"{item['Item']} - Quantity: {item['Quantity']}, Price: {item['Price']} CHF")
    else:
        st.write("No items could be extracted from the text.")


