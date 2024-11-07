import streamlit as st
import requests

# API-Key and URL for Spoonacular
API_KEY = '21c590f808c74caabbaa1494c6196e7a'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# initialisation
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {
        "Tomato": {"Quantity": 5, "Unit": "gramm", "Price": 3.0},
        "Banana": {"Quantity": 3, "Unit": "gramm", "Price": 5.0} 
    }
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Example roommates list
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None

# Choose roommate
def select_user():
    st.title("Who are you")
    if st.session_state["roommates"]:
        selected_user = st.selectbox("Choose your name:", st.session_state["roommates"])
        st.session_state["selected_user"] = selected_user
        st.write(f"Hi, {selected_user}!")
    else:
        st.warning("No user was added.")

# Call up recipe suggestions based on inventory
def get_recipes_from_inventory():
    # Load Ingredients from Inventory
    ingredients = list(st.session_state["inventory"].keys())
    if not ingredients:
        st.warning("Inventory is empty. Please move your lazy ass to Migros.") 
        return
    # Anfrage an Spoonacular API
    params = {
        "ingredients": ",".join(ingredients), # Ingredients of Inventory
        "number": 3, # Nr of Recipes
        "ranking": 1,  # Prioritize recipes with maximum matching ingredients
        "apiKey": API_KEY
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    # Ergebnisse anzeigen
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            st.subheader("Recipe Suggestions")
            for recipe in recipes:
                missed_ingredients = recipe.get("missedIngredientCount", 0)
                if missed_ingredients == 0:  # Show recipes with no extra ingredients required
                    recipe_link = f"https://spoonacular.com/{recipe['title'].replace(' ', '-')}-{recipe['id']}"
                    st.write(f"- **{recipe['title']}** ([View Recipe]({recipe_link}))")
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