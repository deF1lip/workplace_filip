import streamlit as st
from PIL import Image
import easyocr
import re

# Initialisierung des EasyOCR-Lesers
reader = easyocr.Reader(['de', 'en'])  # Unterstützung für Deutsch und Englisch

# Hochlade-Widget für die Rechnung
uploaded_file = st.file_uploader("Lade ein Bild der Rechnung hoch", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Bild laden und anzeigen
    image = Image.open(uploaded_file)
    st.image(image, caption='Hochgeladene Rechnung', use_column_width=True)

    # OCR auf das Bild anwenden
    st.write("Extrahiere Text aus der Rechnung...")
    results = reader.readtext(image)

    # Extrahierten Text Zeile für Zeile anzeigen
    st.write("Extrahierter Text (Zeile für Zeile):")
    for result in results:
        st.write(result[1])  # Jede Textzeile anzeigen

    # Funktion zum Extrahieren von Artikeln, Mengen und Preisen aus jeder Zeile
    def extract_items_from_lines(results):
        items = []
        for result in results:
            line = result[1]

            # Liste möglicher Regex-Muster für verschiedene Rechnungsformate
            patterns = [
                r'(.+?)\s+(\d+,\d{2})\s+(\d+,\d{2})',       # Artikelname, Einzelpreis, Gesamtpreis
                r'(.+?)\s+(\d+)x\s+(\d+,\d{2})\s+(\d+,\d{2})', # Artikelname, Menge, Einzelpreis, Gesamtpreis
                r'(.+?)\s+(\d+,\d{2})'                       # Artikelname und Preis ohne Gesamtpreis
            ]

            # Durchlaufe die Muster, bis eine Übereinstimmung gefunden wird
            matched = False
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    item_name = match.group(1).strip()
                    quantity = 1  # Standardmenge auf 1 setzen
                    price = None
                    total_price = None

                    # Je nach gefundenem Muster die Details extrahieren
                    if len(match.groups()) == 2:
                        price = float(match.group(2).replace(',', '.'))
                        total_price = price
                    elif len(match.groups()) == 3:
                        price = float(match.group(2).replace(',', '.'))
                        total_price = float(match.group(3).replace(',', '.'))
                    elif len(match.groups()) == 4:
                        quantity = int(match.group(2))
                        price = float(match.group(3).replace(',', '.'))
                        total_price = float(match.group(4).replace(',', '.'))

                    items.append({"Artikel": item_name, "Menge": quantity, "Preis": price, "Gesamtpreis": total_price})
                    matched = True
                    break

            # Wenn keine der Regex übereinstimmt, füge die Zeile als unerkannt hinzu
            if not matched:
                st.write(f"Unrecognized line format: {line}")

        return items

    # Informationen aus jeder Zeile extrahieren
    items = extract_items_from_lines(results)

    # Extrahierte Artikel anzeigen
    if items:
        st.write("Extrahierte Artikel:")
        for item in items:
            st.write(f"{item['Artikel']} - Menge: {item['Menge']}, Preis: {item['Preis']} EUR, Gesamtpreis: {item['Gesamtpreis']} EUR")
    else:
        st.write("Es konnten keine Artikel aus dem Text extrahiert werden.")

