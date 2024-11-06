import streamlit as st
from PIL import Image
import pytesseract
import re

# Setze den Pfad zu Tesseract, wenn erforderlich (z.B. für Windows)
# pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract.exe'

# Initialization of session state variables
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]

# Upload-Widget für die Rechnung
uploaded_file = st.file_uploader("Upload an image of your receipt", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Lade das Bild und zeige es an
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Receipt', use_column_width=True)

    # OCR (Texterkennung) auf dem Bild anwenden
    st.write("Extracting text from the receipt...")
    text = pytesseract.image_to_string(image)

    # Zeige den extrahierten Text an
    st.write("Extracted Text:")
    st.write(text)

    # Funktion zur Extraktion von Lebensmitteln, Mengen und Preisen
    def extract_items(text):
        items = []
        lines = text.splitlines()
        for line in lines:
            # Regex zum Extrahieren von Lebensmittelname, Menge und Preis
            match = re.search(r'(\D+)\s+(\d+)\s+(?:CHF|chf|€|eur)?\s?(\d+[\.,]?\d*)', line, re.IGNORECASE)
            if match:
                item_name = match.group(1).strip()
                quantity = int(match.group(2))
                price = float(match.group(3).replace(',', '.'))
                items.append({"Item": item_name, "Quantity": quantity, "Price": price})
        return items

    # Extrahiere die Informationen
    items = extract_items(text)

    # Zeige die extrahierten Artikel an
    if items:
        st.write("Extracted Items:")
        for item in items:
            st.write(f"{item['Item']} - Quantity: {item['Quantity']}, Price: {item['Price']} CHF")
    else:
        st.write("No items found.")
