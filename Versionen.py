import streamlit as st
import pandas as pd
from PIL import Image
from pyzbar.pyzbar import decode
import requests
from datetime import datetime

# Initialization of session state variables
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""
if "roommates" not in st.session_state:
    st.session_state["roommates"] = []
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "settings"
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {}
if "expenses" not in st.session_state:
    st.session_state["expenses"] = {}
if "purchases" not in st.session_state:
    st.session_state["purchases"] = {}
if "consumed" not in st.session_state:
    st.session_state["consumed"] = {}

# Ensure data structure for each roommate
def initialize_roommate_data(roommate):
    if roommate not in st.session_state["expenses"]:
        st.session_state["expenses"][roommate] = 0.0
    if roommate not in st.session_state["purchases"]:
        st.session_state["purchases"][roommate] = []
    if roommate not in st.session_state["consumed"]:
        st.session_state["consumed"][roommate] = []

# Sidebar navigation with buttons
def setup_sidebar():
    st.sidebar.title("Navigation")
    if st.sidebar.button("Overview"):
        st.session_state["page"] = "overview"
    if st.sidebar.button("Fridge"):
        st.session_state["page"] = "fridge"
    if st.sidebar.button("Recipes"):
        st.session_state["page"] = "recipes"
    if st.sidebar.button("Settings"):
        st.session_state["page"] = "settings"

# Function to add a new roommate with data initialization
def add_roommate(room_mate):
    if room_mate and room_mate not in st.session_state["roommates"]:
        st.session_state["roommates"].append(room_mate)
        initialize_roommate_data(room_mate)
        st.success(f"Roommate '{room_mate}' has been added.")
    elif room_mate in st.session_state["roommates"]:
        st.warning(f"Roommate '{room_mate}' is already on the list.")

# Function to add product to inventory and update roommate expenses
def add_product_to_inventory(food_item, quantity, unit, price, selected_roommate):
    purchase_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    initialize_roommate_data(selected_roommate)
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

# Function to remove a product from inventory and update roommate expenses
def delete_product_from_inventory(food_item, quantity, unit, selected_roommate):
    delete_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    initialize_roommate_data(selected_roommate)
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
            st.success(f"'{quantity}' of '{food_item}' has been removed.")
        else:
            st.warning("The quantity to remove exceeds the available quantity.")
    else:
        st.warning("This item is not in the inventory.")

# Fridge page function
def fridge_page():
    st.title("Fridge")
    selected_roommate = st.selectbox("Select the roommate:", st.session_state["roommates"])

    action = st.selectbox("Would you like to add or remove an item?", ["Add", "Remove"])
    if action == "Add":
        food_item = st.text_input("Enter a food item to add:")
        quantity = st.number_input("Quantity:", min_value=0.0)
        unit = st.selectbox("Unit:", ["Pieces", "Liters", "Grams"])
        price = st.number_input("Price (in CHF):", min_value=0.0)
        if st.button("Add item"):
            add_product_to_inventory(food_item, quantity, unit, price, selected_roommate)
    
    elif action == "Remove" and st.session_state["inventory"]:
        food_item = st.selectbox("Select a food item to remove:", list(st.session_state["inventory"].keys()))
        quantity = st.number_input("Quantity to remove:", min_value=1.0, step=1.0)
        unit = st.session_state["inventory"][food_item]["Unit"]
        if st.button("Remove item"):
            delete_product_from_inventory(food_item, quantity, unit, selected_roommate)
    else:
        st.warning("The inventory is empty.")

    if st.session_state["inventory"]:
        st.write("Current Inventory:")
        inventory_df = pd.DataFrame.from_dict(st.session_state["inventory"], orient='index').reset_index().rename(columns={'index': 'Food Item'})
        st.table(inventory_df)

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

# Page display logic
setup_sidebar()
if st.session_state["page"] == "overview":
    overview_page()
elif st.session_state["page"] == "fridge":
    fridge_page()
elif st.session_state["page"] == "recipes":
    recipes_page()
elif st.session_state["page"] == "settings":
    if not st.session_state["setup_finished"]:
        if st.session_state["flate_name"] == "":
            setup_flat_name()
        else:
            setup_roommates()
    else:
        settings_page()

