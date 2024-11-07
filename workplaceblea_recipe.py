import streamlit as st
import requests

# API-Key und URL für Spoonacular
API_KEY = '21c590f808c74caabbaa1494c6196e7a'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# intiatlisierung 
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {
        "Tomato": {"Quantity": 5, "Unit": "gramm", "Price": 3.0},
        "Banana": {"Quantity": 3, "Unit": "gramm", "Price": 5.0} 
    }# Example roommates list
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Example roommates list
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None

# Auswahl des aktuellen Mitbewohner
def select_user():
    st.title("Who are you")
    if st.session_state["roommates"]:
        selected_user = st.selectbox("Choose your name:", st.session_state["roommates"])
        st.session_state["selected_user"] = selected_user
        st.write(f"Hi, {selected_user}!")
    else:
        st.warning("No user was added.")

# Rezeptvorschläge basierend auf Inventar aufrufen
def get_recipes_from_inventory():
    # Zutaten aus dem Inventar laden
    ingredients = list(st.session_state["inventory"].keys())
    if not ingredients:
        st.warning("Inventory is empty. Please move your lazy ass to Migros.")
        return
    # Anfrage an Spoonacular API
    params = {
        "ingredients": ",".join(ingredients), # Zutaten aus Inventory
        "number": 3, # Anzahl an Rezepten
        "apiKey": API_KEY
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    # Ergebnisse anzeigen
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            st.subheader("Recipe Suggestions")
            for recipe in recipes:
                st.write(f"- **{recipe['title']}**")
                st.write(f"  [View Recipe](https://spoonacular.com/recipes/{recipe['id']})")
        else:
            st.write("No recipes found with the current ingredients.")
    else:
        st.error("Error fetching recipes. Please check your API key and try again.")


select_user()

if st.button("Get Recipe Suggestions"):
    if st.session_state["selected_user"]:  # Check if a user is selected
        get_recipes_from_inventory()
    else:
        st.warning("Please select a user first.")