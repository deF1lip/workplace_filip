import streamlit as st
import pandas as pd
import json
import os

# File path for saving data
DATA_FILE = "account_data.json"

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Initialization of session state variables
if "accounts" not in st.session_state:
    st.session_state["accounts"] = load_data()
if "current_account" not in st.session_state:
    st.session_state["current_account"] = None
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "settings"

# Function to set up a new account
def create_account(account_name):
    if account_name and account_name not in st.session_state["accounts"]:
        st.session_state["accounts"][account_name] = {
            "flate_name": account_name,
            "roommates": [],
            "inventory": {},
            "expenses": {},
            "purchases": {},
            "consumed": {},
            "recipe_suggestions": [],
            "selected_recipe": None,
            "selected_recipe_link": None,
            "cooking_history": [],
        }
        st.session_state["current_account"] = account_name
        save_data(st.session_state["accounts"])
        st.success(f"Account '{account_name}' created and selected.")

# Function to select an account
def select_account(account_name):
    if account_name in st.session_state["accounts"]:
        st.session_state["current_account"] = account_name
        st.session_state.update(st.session_state["accounts"][account_name])
        st.success(f"Account '{account_name}' selected.")

# Function to save current account data
def save_current_account_data():
    if st.session_state["current_account"]:
        account_name = st.session_state["current_account"]
        st.session_state["accounts"][account_name] = {
            "flate_name": st.session_state["flate_name"],
            "roommates": st.session_state["roommates"],
            "inventory": st.session_state["inventory"],
            "expenses": st.session_state["expenses"],
            "purchases": st.session_state["purchases"],
            "consumed": st.session_state["consumed"],
            "recipe_suggestions": st.session_state["recipe_suggestions"],
            "selected_recipe": st.session_state["selected_recipe"],
            "selected_recipe_link": st.session_state["selected_recipe_link"],
            "cooking_history": st.session_state["cooking_history"],
        }
        save_data(st.session_state["accounts"])

# Sidebar for account management
st.sidebar.title("Account Management")
account_name = st.sidebar.text_input("Enter account name")
if st.sidebar.button("Create Account"):
    create_account(account_name)
if st.sidebar.selectbox("Select Account", options=list(st.session_state["accounts"].keys()), on_change=lambda: select_account(st.session_state["current_account"])):
    select_account(st.session_state["current_account"])
if st.sidebar.button("Save Data"):
    save_current_account_data()

# Sidebar navigation with buttons
st.sidebar.title("Navigation")
if st.sidebar.button("Overview"):
    st.session_state["page"] = "overview"
if st.sidebar.button("Fridge"):
    st.session_state["page"] = "fridge"
if st.sidebar.button("Scan"):
    st.session_state["page"] = "scan"
if st.sidebar.button("Recipes"):
    st.session_state["page"] = "recipes"
if st.sidebar.button("Settings"):
    st.session_state["page"] = "settings"

# Your existing page logic goes here
