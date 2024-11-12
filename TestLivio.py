import streamlit as st
from datetime import datetime

# Flat name
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = "SunnySide Flat"

# Roommates
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Bilbo", "Frodo", "Gandalf der Weise"]

# Setup finished flag
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = True

# Active page
if "page" not in st.session_state:
    st.session_state["page"] = "overview"

# Inventory with sample items
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {
        "Tomato": {"Quantity": 5.0, "Unit": "kg", "Price": 15.0},
        "Banana": {"Quantity": 3.0, "Unit": "kg", "Price": 10.0},
        "Chicken Breast": {"Quantity": 2.0, "Unit": "kg", "Price": 20.0},
        "Onion": {"Quantity": 10.0, "Unit": "piece", "Price": 5.0},
        "Milk": {"Quantity": 2.0, "Unit": "litre", "Price": 3.0}
    }

# Expenses per roommate
if "expenses" not in st.session_state:
    st.session_state["expenses"] = {
        "Bilbo": 45.0,
        "Frodo": 60.0,
        "Gandalf der Weise": 30.0
    }

# Purchases for each roommate
if "purchases" not in st.session_state:
    st.session_state["purchases"] = {
        "Bilbo": [{"Product": "Tomato", "Quantity": 3.0, "Price": 9.0, "Unit": "kg", "Date": "2024-11-01"}],
        "Frodo": [{"Product": "Banana", "Quantity": 1.0, "Price": 5.0, "Unit": "kg", "Date": "2024-11-03"}],
        "Gandalf der Weise": [{"Product": "Chicken Breast", "Quantity": 2.0, "Price": 20.0, "Unit": "kg", "Date": "2024-11-04"}]
    }

# Consumed items for each roommate
if "consumed" not in st.session_state:
    st.session_state["consumed"] = {
        "Bilbo": [{"Product": "Tomato", "Quantity": 1.0, "Date": "2024-11-05"}],
        "Frodo": [{"Product": "Banana", "Quantity": 1.0, "Date": "2024-11-06"}],
        "Gandalf der Weise": [{"Product": "Chicken Breast", "Quantity": 1.0, "Date": "2024-11-07"}]
    }

# Recipe suggestions
if "recipe_suggestions" not in st.session_state:
    st.session_state["recipe_suggestions"] = ["Tomato Soup", "Banana Smoothie", "Grilled Chicken"]
if "recipe_links" not in st.session_state:
    st.session_state["recipe_links"] = {
        "Tomato Soup": "https://example.com/tomato_soup",
        "Banana Smoothie": "https://example.com/banana_smoothie",
        "Grilled Chicken": "https://example.com/grilled_chicken"
    }

# Selected recipe
if "selected_recipe" not in st.session_state:
    st.session_state["selected_recipe"] = "Tomato Soup"
if "selected_recipe_link" not in st.session_state:
    st.session_state["selected_recipe_link"] = "https://example.com/tomato_soup"

# Cooking history with sample entries
if "cooking_history" not in st.session_state:
    st.session_state["cooking_history"] = [
        {"Person": "Bilbo", "Recipe": "Tomato Soup", "Rating": 4, "Link": "https://example.com/tomato_soup", "Date": "2024-11-02"},
        {"Person": "Frodo", "Recipe": "Banana Smoothie", "Rating": 5, "Link": "https://example.com/banana_smoothie", "Date": "2024-11-03"},
        {"Person": "Gandalf der Weise", "Recipe": "Grilled Chicken", "Rating": 3, "Link": "https://example.com/grilled_chicken", "Date": "2024-11-04"}
    ]
