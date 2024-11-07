import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode  # Barcode-Decoder für Bilder
import requests  # Für API-Anfragen an Open Food Facts

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
        if data["status"] == 1:
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
            st.write(f"Product: {product_info['name']}")
            st.write(f"Brand: {product_info['brand']}")
        else:
            st.write("Product not found in database.")

        # Manuelle Eingabe von Menge und Preis
        quantity = st.number_input("Quantity:", min_value=0.0, step=0.1)
        price = st.number_input("Price (in CHF):", min_value=0.0, step=0.1)

        # Button zum Hinzufügen des Produkts
        if st.button("Add product to inventory"):
            st.success(f"Added '{product_info['name']}' with quantity {quantity} and price {price} CHF.")
    else:
        st.write("No barcode found in the image.")


