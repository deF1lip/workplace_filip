import streamlit as st
import pandas as pd


# Initialize session state variables
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
    st.session_state["expenses"] = {mate: 0.0 for mate in st.session_state["roommates"]}


# Function to change pages
def change_page(new_page):
    st.session_state["page"] = new_page

# Sidebar navigation with buttons
st.sidebar.title("Navigation")
if st.sidebar.button("Overview"):
    change_page("overview")
if st.sidebar.button("Fridge"):
    change_page("fridge")
if st.sidebar.button("Recipes"):
    change_page("recipes")
if st.sidebar.button("Settings"):
    change_page("settings")

# Function for the overview page
def overview_page():
    # Sets the title to "Overview: Name of the flat"
    title = f"Overview: {st.session_state['flate_name']}" if st.session_state["flate_name"] else "Overview"
    st.title(title)
    st.write("Welcome to the main page of your app.")
    st.write("Here you can display general information.")


# Function for the recipes page
def fridge_page():
    st.title("Fridge")

    # Roommate selection
    if st.session_state["roommates"]:
        selected_roommate = st.selectbox("Select the roommate:", st.session_state["roommates"])
    else:
        st.warning("No roommates available.")
        return

    # Action selection: Add or Remove
    action = st.selectbox("Would you like to add or remove an item?", ["Add", "Remove"])

    if action == "Add":
        # Input fields for food item, quantity, unit, and price
        food_item = st.text_input("Enter a food item to add:")
        quantity = st.number_input("Quantity:", min_value=0.0)
        unit = st.selectbox("Unit:", ["Pieces", "Liters", "Grams"])
        price = st.number_input("Price (in CHF):", min_value=0.0)

        # Button to add the food item
        if st.button("Add item"):
            if food_item and quantity > 0 and price >= 0 and selected_roommate:
                if food_item in st.session_state["inventory"]:
                    st.session_state["inventory"][food_item]["Quantity"] += quantity
                    st.session_state["inventory"][food_item]["Price"] += price
                else:
                    st.session_state["inventory"][food_item] = {"Quantity": quantity, "Unit": unit, "Price": price}
                st.session_state["expenses"][selected_roommate] += price
                st.success(f"'{food_item}' has been added to the inventory.")
            else:
                st.warning("Please fill in all fields.")
    
    elif action == "Remove":
        # Select the item to remove
        if st.session_state["inventory"]:
            food_item = st.selectbox("Select a food item to remove:", list(st.session_state["inventory"].keys()))
            quantity = st.number_input("Quantity to remove:", min_value=1.0, step=1.0)

            # Button to remove the item
            if st.button("Remove item"):
                if food_item and quantity > 0 and selected_roommate:
                    if food_item in st.session_state["inventory"]:
                        current_quantity = st.session_state["inventory"][food_item]["Quantity"]
                        current_price = st.session_state["inventory"][food_item]["Price"]
                        if quantity <= current_quantity:
                            # Calculate the price per unit
                            price_per_unit = current_price / current_quantity if current_quantity > 0 else 0
                            # Calculate the amount to deduct
                            amount_to_deduct = price_per_unit * quantity
                            # Update inventory
                            st.session_state["inventory"][food_item]["Quantity"] -= quantity
                            st.session_state["inventory"][food_item]["Price"] -= amount_to_deduct
                            # Update roommate's expenses
                            st.session_state["expenses"][selected_roommate] -= amount_to_deduct
                            st.success(f"'{quantity}' of '{food_item}' has been removed.")
                            # Remove item if quantity reaches zero
                            if st.session_state["inventory"][food_item]["Quantity"] <= 0:
                                del st.session_state["inventory"][food_item]
                        else:
                            st.warning("The quantity to remove exceeds the available quantity.")
                    else:
                        st.warning("This item is not in the inventory.")
                else:
                    st.warning("Please fill in all fields.")
        else:
            st.warning("The inventory is empty.")

    # Display current inventory
    if st.session_state["inventory"]:
        st.write("Current Inventory:")
        inventory_df = pd.DataFrame.from_dict(st.session_state["inventory"], orient='index')
        inventory_df = inventory_df.reset_index().rename(columns={'index': 'Food Item'})
        st.table(inventory_df)
    else:
        st.write("The inventory is empty.")

    # Display total expenses per roommate
    st.write("Total expenses per roommate:")
    expenses_df = pd.DataFrame(list(st.session_state["expenses"].items()), columns=["Roommate", "Total Expenses (CHF)"])
    st.table(expenses_df)



# Page display logic for the selected page
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


