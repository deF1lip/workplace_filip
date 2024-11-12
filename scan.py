import streamlit as st
from PIL import Image, ImageEnhance
import easyocr
import numpy as np
from streamlit_drawable_canvas import st_canvas
import re

# Initialisierung des EasyOCR-Lesers
reader = easyocr.Reader(['de', 'en'])  # Unterstützung für Deutsch und Englisch

# Hochlade-Widget für die Rechnung
uploaded_file = st.file_uploader("Lade ein Bild der Rechnung hoch", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Bild laden
    image = Image.open(uploaded_file)
    
    # Bild in der Originalversion anzeigen und interaktive Leinwand hinzufügen
    st.write("Markiere den Bereich, den du für die Texterkennung analysieren möchtest:")
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # Transparente rote Markierung
        stroke_width=2,
        stroke_color="red",
        background_image=image,
        update_streamlit=True,
        height=image.size[1],
        width=image.size[0],
        drawing_mode="rect",  # Rechteck-Auswahlmodus
        key="canvas",
    )

    # Überprüfe, ob ein Bereich ausgewählt wurde
    if canvas_result.json_data is not None:
        for shape in canvas_result.json_data["objects"]:
            # Extrahiere die Position des ausgewählten Bereichs
            left = shape["left"]
            top = shape["top"]
            width = shape["width"]
            height = shape["height"]

            # Bild zuschneiden auf den ausgewählten Bereich
            cropped_image = image.crop((left, top, left + width, top + height))
            
            # Bild anzeigen, das für OCR verwendet wird
            st.image(cropped_image, caption="Ausgewählter Bereich für Texterkennung", use_column_width=True)
            
            # Bildvorverarbeitung (Graustufen und Kontrastverbesserung)
            cropped_image = cropped_image.convert("L")  # Konvertiere in Graustufen
            enhancer = ImageEnhance.Contrast(cropped_image)
            cropped_image = enhancer.enhance(2)  # Kontrasterhöhung für bessere OCR-Erkennung
            
            # OCR auf das zugeschnittene Bild anwenden
            st.write("Extrahiere Text aus dem ausgewählten Bereich...")
            results = reader.readtext(np.array(cropped_image))

            # Funktion zum Extrahieren von Artikeln, Mengen und Preisen aus jeder Zeile
            def extract_items_from_lines(results):
                items = []
                for result in results:
                    line = result[1].strip()

                    # Liste möglicher Regex-Muster für verschiedene Rechnungsformate
                    patterns = [
                        r'(\d+)\s*x?\s*(.+?)\s+(\d+,\d{2})',          # Menge, Artikelname, Preis/Gesamtpreis
                        r'(.+?)\s+(\d+,\d{2})\s+(\d+,\d{2})',        # Artikelname, Einzelpreis, Gesamtpreis
                        r'(.+?)\s+(\d+,\d{2})'                       # Artikelname und Preis ohne Gesamtpreis
                    ]

                    # Durchlaufe die Muster, bis eine Übereinstimmung gefunden wird
                    matched = False
                    for pattern in patterns:
                        match = re.search(pattern, line)
                        if match:
                            quantity = 1  # Standardmenge auf 1 setzen
                            item_name = match.group(1).strip()
                            price = None
                            total_price = None

                            # Je nach gefundenem Muster die Details extrahieren
                            if len(match.groups()) == 2:
                                item_name = match.group(1).strip()
                                price = float(match.group(2).replace(',', '.'))
                                total_price = price
                            elif len(match.groups()) == 3:
                                quantity = int(match.group(1)) if match.group(1).isdigit() else 1
                                item_name = match.group(2).strip()
                                price = float(match.group(3).replace(',', '.'))
                                total_price = price
                            
                            items.append({"Menge": quantity, "Artikel": item_name, "Preis": total_price})
                            matched = True
                            break

                    # Wenn keine der Regex übereinstimmt, füge die Zeile als unerkannt hinzu
                    if not matched:
                        st.write(f"Nicht erkanntes Zeilenformat: {line}")

                return items

            # Informationen aus jeder Zeile extrahieren
            items = extract_items_from_lines(results)

            # Extrahierte Artikel anzeigen
            if items:
                st.write("Extrahierte Artikel:")
                for item in items:
                    st.write(f"Menge: {item['Menge']} - Artikel: {item['Artikel']} - Preis: {item['Preis']} EUR")
            else:
                st.write("Es konnten keine Artikel aus dem Text extrahiert werden.")



