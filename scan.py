import streamlit as st
from PIL import Image
import easyocr
import re

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Optional: add more languages, e.g., ['en', 'de']

# Upload widget for the receipt
uploaded_file = st.file_uploader("Upload an image of your receipt", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Receipt', use_column_width=True)

    # Apply OCR to extract text line by line
    st.write("Extracting text from the receipt...")
    results = reader.readtext(image)

    # Display each line with a dropdown for user input
    st.write("Please classify each line:")
    items = []
    for result in results:
        line = result[1]
        st.write(f"Detected Text: {line}")
        category = st.selectbox(
            "Select the category for this line:",
            ("Ignore", "Item Name", "Quantity", "Price"),
            key=line  # Ensures each selectbox is unique
        )
        
        # Store classified data based on user selection
        if category == "Item Name":
            items.append({"Item": line, "Quantity": None, "Price": None})
        elif category == "Quantity":
            if items:
                items[-1]["Quantity"] = line  # Assign quantity to the last item
        elif category == "Price":
            if items:
                items[-1]["Price"] = line  # Assign price to the last item

    # Display extracted items
    if items:
        st.write("Extracted Items:")
        for item in items:
            st.write(f"Item: {item['Item']}, Quantity: {item['Quantity']}, Price: {item['Price']}")
    else:
        st.write("No items were classified.")

