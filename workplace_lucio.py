import streamlit as st
import json
import os
import pandas as pd
from PIL import Image
from datetime import datetime
from settings_page import setup_flat_name, setup_roommates, settingspage
from fridge_page import fridge_page
from barcode_page import barcode_page
from recipe_page import recipepage

# Funktion, um Benutzer zu registrieren und zu speichern
def register_user(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            users = json.load(file)
    else:
        users = {}

    if username in users:
        st.error("Benutzername existiert bereits!")
        return False
    else:
        users[username] = password
        with open("users.json", "w") as file:
            json.dump(users, file)
        return True

# Funktion, um Benutzer anzumelden
def login_user(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            users = json.load(file)
    else:
        st.error("Keine Benutzer gefunden! Bitte registriere dich zuerst.")
        return False

    if username in users and users[username] == password:
        return True
    else:
        st.error("Falscher Benutzername oder falsches Passwort!")
        return False

# Funktion, um WG-Daten zu speichern
def save_data(username, data):
    data_file = f"{username}_data.json"
    with open(data_file, "w") as file:
        json.dump(data, file)

# Funktion, um WG-Daten zu laden
def load_data(username):
    data_file = f"{username}_data.json"
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    else:
        return {}

# Benutzerregistrierung oder -anmeldung
st.title("WG-Manager App")

# Initialisierung der Sitzung
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "data" not in st.session_state:
    st.session_state["data"] = {}

menu = st.sidebar.selectbox("Menü", ["Anmelden", "Registrieren"])

if not st.session_state["logged_in"]:
    username = st.sidebar.text_input("Benutzername")
    password = st.sidebar.text_input("Passwort", type="password")

    if menu == "Registrieren":
        if st.sidebar.button("Registrieren"):
            if register_user(username, password):
                st.success("Erfolgreich registriert! Bitte melde dich an.")
    elif menu == "Anmelden":
        if st.sidebar.button("Anmelden"):
            if login_user(username, password):
                st.success(f"Willkommen, {username}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                # WG-Daten laden
                st.session_state["data"] = load_data(username)
                # WG-Daten in den Session State laden
                st.session_state.update(st.session_state["data"])

# Sicherstellen, dass alle Session-State-Variablen initialisiert sind
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
if "recipe_suggestions" not in st.session_state:
    st.session_state["recipe_suggestions"] = []
if "selected_recipe" not in st.session_state:
    st.session_state["selected_recipe"] = None
if "selected_recipe_link" not in st.session_state:
    st.session_state["selected_recipe_link"] = None
if "cooking_history" not in st.session_state:
    st.session_state["cooking_history"] = []
if "recipe_links" not in st.session_state:
    st.session_state["recipe_links"] = {}

# Wenn der Benutzer angemeldet ist, zeige die Hauptseite
if st.session_state["logged_in"]:
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

    # Funktion zum automatischen Speichern der WG-Daten
    def auto_save():
        st.session_state["data"] = {
            "flate_name": st.session_state.get("flate_name", ""),
            "roommates": st.session_state.get("roommates", []),
            "setup_finished": st.session_state.get("setup_finished", False),
            "inventory": st.session_state.get("inventory", {}),
            "expenses": st.session_state.get("expenses", {}),
            "purchases": st.session_state.get("purchases", {}),
            "consumed": st.session_state.get("consumed", {}),
            "recipe_suggestions": st.session_state.get("recipe_suggestions", []),
            "selected_recipe": st.session_state.get("selected_recipe", None),
            "selected_recipe_link": st.session_state.get("selected_recipe_link", None),
            "cooking_history": st.session_state.get("cooking_history", []),
            "recipe_links": st.session_state.get("recipe_links", {})
        }
        save_data(st.session_state["username"], st.session_state["data"])

    # Page display logic for the selected page
    if st.session_state["page"] == "overview":
        st.title(f"Overview: {st.session_state['flate_name']}")
        st.write("Willkommen auf der Übersichtsseite deiner WG!")
        auto_save()  # Daten automatisch speichern
    elif st.session_state["page"] == "fridge":
        fridge_page()
        auto_save()  # Daten automatisch speichern
    elif st.session_state["page"] == "scan":
        barcode_page()
        auto_save()  # Daten automatisch speichern
    elif st.session_state["page"] == "recipes":
        recipepage()
        auto_save()  # Daten automatisch speichern
    elif st.session_state["page"] == "settings":
        if not st.session_state["setup_finished"]:
            if st.session_state["flate_name"] == "":
                setup_flat_name()
            else:
                setup_roommates()
        else:
            settingspage()
        auto_save()  # Daten automatisch speichern
else:
    st.write("Bitte melde dich an oder registriere dich, um fortzufahren.")
