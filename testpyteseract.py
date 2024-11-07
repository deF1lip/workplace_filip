import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode  # Barcode-Decoder für Bilder
import requests  # Für API-Anfragen an Open Food Facts

# Initialisierung von Session-State-Variablen
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {}  # Das Inventar als Wörterbuch
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Beispielhafte Mitbewohnerliste
if "expenses" not in st.session_state:
    st.session_state["expenses"] = {mate: 0.0 for mate in st.session_state["roommates"]}  # Ausgaben pro Mitbewohner

# Funktion zum Decodieren des Barcodes
def decode_barcode(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode("utf-8")  # Gibt den Barcode als Text zurück
    return None

# Funktion zur Abfrage der Open Food Facts API
def get_product_info(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            product = data["product"]
            return {
                "name": product.get("product_name", "Unknown Product"),
                "brand": product.get("brands", "Unknown Brand")
            }
    return None

# Upload-Widget für das Barcode-Bild
uploaded_file = st.file_uploader("Upload an image with a barcode", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Barcode-Scan und Produktsuche
    st.write("Scanning for barcode...")
    barcode = decode_barcode(image)

    if barcode:
        st.write(f"Barcode found: {barcode}")
        st.write("Looking up product information...")
        product_info = get_product_info(barcode)

        if product_info:
            # Vorab ausgefüllte Felder basierend auf API-Ergebnissen
            food_item = st.text_input("Product:", value=product_info['name'])
            brand = st.text_input("Brand:", value=product_info['brand'])
        else:
            st.write("Product not found in database.")
            food_item = st.text_input("Product:")
            brand = st.text_input("Brand:")

        # Auswahl des Käufers
        selected_roommate = st.selectbox("Who bought the product?", st.session_state["roommates"])

        # Manuelle Eingabe von Menge, Einheit und Preis mit Formatierung auf 2 Dezimalstellen
        quantity = st.number_input("Quantity:", min_value=0.0, step=0.1, format="%.2f")
        unit = st.selectbox("Unit:", ["Pieces", "Liters", "Grams"])
        price = st.number_input("Price (in CHF):", min_value=0.0, step=0.1, format="%.2f")

        # Button zum Hinzufügen des Produkts
        if st.button("Add product to inventory"):
            if food_item and quantity > 0 and price >= 0:
                # Aktualisierung des Inventars
                if food_item in st.session_state["inventory"]:
                    st.session_state["inventory"][food_item]["Quantity"] += quantity
                    st.session_state["inventory"][food_item]["Price"] += price
                else:
                    st.session_state["inventory"][food_item] = {"Quantity": quantity, "Unit": unit, "Price": price}
                
                # Aktualisierung der Ausgaben des Käufers
                st.session_state["expenses"][selected_roommate] += price
                st.success(f"'{food_item}' has been added to the inventory, and {selected_roommate}'s expenses were updated.")
            else:
                st.warning("Please fill in all fields.")
    else:
        st.write("No barcode found in the image.")

    # Display total expenses per roommate
    st.write("Total expenses per roommate:")
    expenses_df = pd.DataFrame(list(st.session_state["expenses"].items()), columns=["Roommate", "Total Expenses (CHF)"])
    st.table(expenses_df)