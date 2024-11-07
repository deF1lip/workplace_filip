import streamlit as st
import pandas as pd
from PIL import Image
from pyzbar.pyzbar import decode
import requests
from datetime import datetime

# Initialisierung von Session-State-Variablen
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {}
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]
if "expenses" not in st.session_state:
    st.session_state["expenses"] = {mate: 0.0 for mate in st.session_state["roommates"]}
if "purchases" not in st.session_state:
    st.session_state["purchases"] = {mate: [] for mate in st.session_state["roommates"]}

def decode_barcode(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode("utf-8")
    return None

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

st.title("Upload  barcode ")
uploaded_file = st.file_uploader("Upload an image with a barcode", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.write("Scanning for barcode...")
    barcode = decode_barcode(image)

    if barcode:
        st.write(f"Barcode found: {barcode}")
        st.write("Looking up product information...")
        product_info = get_product_info(barcode)

        if product_info:
            food_item = st.text_input("Product:", value=product_info['name'])
            brand = st.text_input("Brand:", value=product_info['brand'])
        else:
            st.write("Product not found in database.")
            food_item = st.text_input("Product:")
            brand = st.text_input("Brand:")

        selected_roommate = st.selectbox("Who bought the product?", st.session_state["roommates"])
        quantity = st.number_input("Quantity:", min_value=0.0, step=0.1, format="%.2f")
        unit = st.selectbox("Unit:", ["Pieces", "Liters", "Grams"])
        price = st.number_input("Price (in CHF):", min_value=0.0, step=0.1, format="%.2f")

        if st.button("Add product to inventory"):
            if food_item and quantity > 0 and price >= 0:
                purchase_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if food_item in st.session_state["inventory"]:
                    st.session_state["inventory"][food_item]["Quantity"] += quantity
                    st.session_state["inventory"][food_item]["Price"] += price
                else:
                    st.session_state["inventory"][food_item] = {"Quantity": quantity, "Unit": unit, "Price": price}
                
                st.session_state["expenses"][selected_roommate] += price
                st.session_state["purchases"][selected_roommate].append({
                    "Product": food_item,
                    "Quantity": quantity,
                    "Price": price,
                    "Unit": unit,
                    "Date": purchase_time
                })
                st.success(f"'{food_item}' has been added to the inventory, and {selected_roommate}'s expenses were updated.")
            else:
                st.warning("Please fill in all fields.")
    else:
        st.write("No barcode found in the image.")

# Anzeige der Gesamtausgaben pro Mitbewohner
with st.expander("View Total Expenses per Roommate"):
    expenses_df = pd.DataFrame(list(st.session_state["expenses"].items()), columns=["Roommate", "Total Expenses (CHF)"])
    st.table(expenses_df)

# Anzeige der Einkäufe pro Mitbewohner
with st.expander("Purchases per Roommate"):
    for roommate, purchases in st.session_state["purchases"].items():
        st.write(f"**{roommate}**")
        if purchases:
            purchases_df = pd.DataFrame(purchases)
            st.table(purchases_df)
        else:
            st.write("No purchases recorded.")

