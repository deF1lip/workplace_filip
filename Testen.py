import streamlit as st
import pandas as pd

# Initialization of session state variables
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Example roommates list
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {}
if "expenses" not in st.session_state:
    st.session_state["expenses"] = {mate: 0.0 for mate in st.session_state["roommates"]}

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
        quantity = st.number_input("Quantity:", min_value=0)
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
            quantity = st.number_input("Quantity to remove:", min_value=1, step=1)

            # Button to remove the item
            if st.button("Remove item"):
                if food_item and quantity > 0 and selected_roommate:
                    if food_item in st.session_state["inventory"]:
                        current_quantity = st.session_state["inventory"][food_item]["Quantity"]
                        current_price = st.session_state["inventory"][food_item]["Price"]
                        if quantity <= current_quantity:
                            # Calculate the price per unit
                            price_per_unit = current_price / current_quantity
                            # Calculate the amount to deduct
                            amount_to_deduct = price_per_unit * quantity
                            # Update inventory
                            st.session_state["inventory"][food_item]["Quantity"] -= quantity
                            st.session_state["inventory"][food_item]["Price"] -= amount_to_deduct
                            # Update roommate's expenses
                            st.session_state["expenses"][selected_roommate] -= amount_to_deduct
                            st.success(f"'{quantity}' of '{food_item}' has been removed.")
                            # Remove item if quantity reaches zero
                            if st.session_state["inventory"][food_item]["Quantity"] == 0:
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

# Call the function to display the fridge page
fridge_page()


