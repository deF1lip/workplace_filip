import streamlit as st
from PIL import Image
import pytesseract
import re

# Upload-Widget für das Rechnungsbild
uploaded_file = st.file_uploader("Lade ein Bild deiner Rechnung hoch", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Lade und zeige das Bild an
    image = Image.open(uploaded_file)
    st.image(image, caption='Hochgeladene Rechnung', use_column_width=True)

    # OCR-Anwendung auf das Bild
    st.write("Texterkennung wird ausgeführt...")
    text = pytesseract.image_to_string(image)

    # Zeige den extrahierten Text an
    st.write("Extrahierter Text:")
    st.write(text)

    # Funktion zur Extraktion von Artikeln, Mengen und Preisen
    def extract_items(text):
        items = []
        # Zeilenweise durch den Text gehen
        lines = text.splitlines()
        for line in lines:
            # Regex zum Extrahieren von Artikelnamen, Menge und Preis
            match = re.search(r'(\D+)\s+(\d+)\s+(\d+[\.,]?\d*)', line)
            if match:
                # Artikelnamen, Menge und Preis aus dem Match extrahieren
                item_name = match.group(1).strip()
                quantity = int(match.group(2))
                price = float(match.group(3).replace(',', '.'))
                items.append({"Artikel": item_name, "Menge": quantity, "Preis": price})
        return items

    # Extrahiere die Artikel
    items = extract_items(text)

    # Zeige die extrahierten Artikel an
    if items:
        st.write("Extrahierte Artikel:")
        for item in items:
            st.write(f"Artikel: {item['Artikel']}, Menge: {item['Menge']}, Preis: {item['Preis']} CHF")
    else:
        st.write("Es konnten keine Artikel aus dem Text extrahiert werden.")



