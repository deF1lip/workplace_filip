import streamlit as st
import json
from datetime import datetime
import pandas as pd

# Dateipfad für die JSON-Speicherung
DATA_FILE = "session_data.json"

# Funktion zum Laden der Daten aus einer JSON-Datei
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        # Standardstruktur, falls die Datei nicht existiert
        return {
            "roommates": ["Livio", "Flurin", "Anderin"],
            "inventory": {},
            "expenses": {mate: 0.0 for mate in ["Livio", "Flurin", "Anderin"]},
            "purchases": {mate: [] for mate in ["Livio", "Flurin", "Anderin"]},
            "consumed": {mate: [] for mate in ["Livio", "Flurin", "Anderin"]}
        }

# Funktion zum Speichern der Daten in einer JSON-Datei
def save_data():
    data = {
        "roommates": st.session_state["roommates"],
        "inventory": st.session_state["inventory"],
        "expenses": st.session_state["expenses"],
        "purchases": st.session_state["purchases"],
        "consumed": st.session_state["consumed"]
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialisiere oder lade die Session-States beim Start
data = load_data()
if "roommates" not in st.session_state:
    st.session_state["roommates"] = data["roommates"]
if "inventory" not in st.session_state:
    st.session_state["inventory"] = data["inventory"]
if "expenses" not in st.session_state:
    st.session_state["expenses"] = data["expenses"]
if "purchases" not in st.session_state:
    st.session_state["purchases"] = data["purchases"]
if "consumed" not in st.session_state:
    st.session_state["consumed"] = data["consumed"]

# Funktion zum Hinzufügen eines Produkts
def add_product_to_inventory(food_item, quantity, unit, price, selected_roommate):
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
    save_data()  # Speichern nach der Aktualisierung
    st.success(f"'{food_item}' has been added to the inventory, and {selected_roommate}'s expenses were updated.")

# Funktion zum Entfernen eines Produkts
def delete_product_from_inventory(food_item, quantity, unit, selected_roommate):
    delete_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if food_item and quantity > 0 and selected_roommate:
        if food_item in st.session_state["inventory"]:
            current_quantity = st.session_state["inventory"][food_item]["Quantity"]
            current_price = st.session_state["inventory"][food_item]["Price"]
            if quantity <= current_quantity:
                price_per_unit = current_price / current_quantity if current_quantity > 0 else 0
                amount_to_deduct = price_per_unit * quantity
                st.session_state["inventory"][food_item]["Quantity"] -= quantity
                st.session_state["inventory"][food_item]["Price"] -= amount_to_deduct
                st.session_state["expenses"][selected_roommate] -= amount_to_deduct
                st.session_state["consumed"][selected_roommate].append({
                    "Product": food_item,
                    "Quantity": quantity,
                    "Price": amount_to_deduct,
                    "Unit": unit,
                    "Date": delete_time
                })
                if st.session_state["inventory"][food_item]["Quantity"] <= 0:
                    del st.session_state["inventory"][food_item]
                save_data()  # Speichern nach der Aktualisierung
                st.success(f"'{quantity}' of '{food_item}' has been removed.")
            else:
                st.warning("The quantity to remove exceeds the available quantity.")
        else:
            st.warning("This item is not in the inventory.")
    else:
        st.warning("Please fill in all fields.")

# Hauptseite für den Kühlschrank
def fridge_page():
    st.title("Fridge")

    # Roommate selection
    if st.session_state["roommates"]:
        selected_roommate = st.selectbox("Select the roommate:", st.session_state["roommates"])
    else:
        st.warning("No roommates available.")
        return

    # Auswahl: Hinzufügen oder Entfernen
    action = st.selectbox("Would you like to add or remove an item?", ["Add", "Remove"])

    if action == "Add":
        food_item = st.text_input("Enter a food item to add:")
        quantity = st.number_input("Quantity:", min_value=0.0)
        unit = st.selectbox("Unit:", ["Pieces", "Liters", "Grams"])
        price = st.number_input("Price (in CHF):", min_value=0.0)

        if st.button("Add item"):
            if food_item and quantity > 0 and price >= 0 and selected_roommate:
                add_product_to_inventory(food_item, quantity, unit, price, selected_roommate)
            else:
                st.warning("Please fill in all fields.")
    
    elif action == "Remove":
        if st.session_state["inventory"]:
            food_item = st.selectbox("Select a food item to remove:", list(st.session_state["inventory"].keys()))
            quantity = st.number_input("Quantity to remove:", min_value=1.0, step=1.0)
            unit = st.session_state["inventory"][food_item]["Unit"]

            if st.button("Remove item"):
                delete_product_from_inventory(food_item, quantity, unit, selected_roommate)
        else:
            st.warning("The inventory is empty.")

    if st.session_state["inventory"]:
        st.write("Current Inventory:")
        inventory_df = pd.DataFrame.from_dict(st.session_state["inventory"], orient='index')
        inventory_df = inventory_df.reset_index().rename(columns={'index': 'Food Item'})
        st.table(inventory_df)
    else:
        st.write("The inventory is empty.")

    st.write("Total expenses per roommate:")
    expenses_df = pd.DataFrame(list(st.session_state["expenses"].items()), columns=["Roommate", "Total Expenses (CHF)"])
    st.table(expenses_df)

    st.write("Purchases and Consumptions per roommate:")
    for mate in st.session_state["roommates"]:
        st.write(f"**{mate}'s Purchases:**")
        purchases_df = pd.DataFrame(st.session_state["purchases"][mate])
        st.table(purchases_df)

        st.write(f"**{mate}'s Consumptions:**")
        consumed_df = pd.DataFrame(st.session_state["consumed"][mate])
        st.table(consumed_df)

fridge_page()
