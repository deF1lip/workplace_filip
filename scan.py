import streamlit as st
from PIL import Image
import easyocr
import re

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Hier kannst du zusätzliche Sprachen angeben, z.B. ['en', 'de']

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
    results = reader.readtext(image)

    # Combine the recognized text into a single string for easier processing
    text = "\n".join([result[1] for result in results])

    # Display the extracted text
    st.write("Extracted Text:")
    st.write(text)

    # Function to extract items, quantities, and prices based on expected format
    def extract_items(text):
        items = []
        lines = text.splitlines()
        for line in lines:
            # Regex to match a format where we expect:
            # - Quantity (an even number)
            # - Item name
            # - Price with two decimal places and a dot between francs and rappen (e.g., 12.50)
            match = re.search(r'(\d+)\s+([^\d]+?)\s+(\d+\.\d{2})', line)
            if match:
                quantity = int(match.group(1))
                item_name = match.group(2).strip()
                price = float(match.group(3))
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
        st.write("No items found.")

