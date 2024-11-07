import streamlit as st
import fitz  # PyMuPDF
import re

# Initialization of session state variables
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]

# Upload widget for the receipt
uploaded_file = st.file_uploader("Upload a PDF of your receipt", type=["pdf"])

if uploaded_file is not None:
    # Laden und Auslesen des PDFs
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
        all_text = ""
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            page_text = page.get_text()
            all_text += page_text + "\n"  # Alle Seiten kombinieren
            
    # Zeige den extrahierten Text an
    st.write("Extracted Text:")
    st.write(all_text)

    # Funktion zur Extraktion von Lebensmitteln, Mengen und Preisen
    def extract_items_from_text(text):
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
    items = extract_items_from_text(all_text)

    # Zeige die extrahierten Artikel an
    if items:
        st.write("Extracted Items:")
        for item in items:
            st.write(f"{item['Item']} - Quantity: {item['Quantity']}, Price: {item['Price']} CHF")
    else:
        st.write("No items could be extracted from the text.")

