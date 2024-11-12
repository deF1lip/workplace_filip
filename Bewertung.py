import streamlit as st
import requests
import random

# API-Key and URL for Spoonacular
API_KEY = '21c590f808c74caabbaa1494c6196e7a'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# Initialisation
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {
        "Tomato": {"Quantity": 5, "Unit": "gram", "Price": 3.0},
        "Banana": {"Quantity": 3, "Unit": "gram", "Price": 5.0},
        "Onion": {"Quantity": 2, "Unit": "piece", "Price": 1.5},
        # ... (and other items as needed)
    }
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Bilbo", "Frodo", "Gandalf der Weise"]
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None
if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}
if "selected_recipe" not in st.session_state:
    st.session_state["selected_recipe"] = None
if "rating_submitted" not in st.session_state:
    st.session_state["rating_submitted"] = False

# Choose roommate
def select_user():
    st.title("Who are you")
    selected_user = st.selectbox("Choose your name:", st.session_state["roommates"], 
                                 index=st.session_state["roommates"].index(st.session_state["selected_user"]) 
                                 if st.session_state["selected_user"] else 0)
    st.session_state["selected_user"] = selected_user
    st.write(f"Hi, {selected_user}!")

# Get recipe suggestions based on inventory
def get_recipes_from_inventory():
    ingredients = list(st.session_state["inventory"].keys())
    if not ingredients:
        st.warning("Inventory is empty. Please restock.")
        return []
    
    params = {
        "ingredients": ",".join(ingredients),
        "number": 3,
        "ranking": 2,
        "apiKey": API_KEY
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    
    if response.status_code == 200:
        recipes = response.json()
        recipe_titles = []
        if recipes:
            random.shuffle(recipes)
            for recipe in recipes[:3]:
                recipe_titles.append(recipe['title'])
            return recipe_titles
        else:
            st.write("No recipes found with the current ingredients.")
            return []
    else:
        st.error("Error fetching recipes. Please check your API key and try again.")
        return []

# Rate the selected recipe
def rate_recipe(recipe_title):
    rating = st.slider("Rate this recipe with stars (1-5):", 1, 5, key="rating_slider")
    if st.button("Submit Rating"):
        user = st.session_state["selected_user"]
        if user:
            if user not in st.session_state["ratings"]:
                st.session_state["ratings"][user] = {}
            st.session_state["ratings"][user][recipe_title] = rating
            st.session_state["rating_submitted"] = True
            st.session_state["selected_recipe"] = recipe_title
            st.success(f"You have rated '{recipe_title}' with {rating} stars!")

# Main application flow
select_user()

# Fetch recipe suggestions only if a user is selected
if st.button("Get Recipe Suggestions"):
    if st.session_state["selected_user"]:
        recipe_titles = get_recipes_from_inventory()
        if recipe_titles:
            selected_recipe = st.selectbox("Select a recipe to make", recipe_titles, key="selected_recipe_choice")
            st.session_state["selected_recipe"] = selected_recipe
            st.write(f"You have selected to make '{selected_recipe}'.")

# Display the rating section if a recipe was selected
if st.session_state["selected_recipe"] and not st.session_state["rating_submitted"]:
    rate_recipe(st.session_state["selected_recipe"])

# Display the ratings summary
if st.session_state["ratings"]:
    st.subheader("Ratings Summary")
    for user, user_ratings in st.session_state["ratings"].items():
        st.write(f"**{user}'s Ratings:**")
        for recipe, rating in user_ratings.items():
            st.write(f"- {recipe}: {rating} stars")

# Reset the rating_submitted flag after displaying success message
if st.session_state["rating_submitted"]:
    st.write(f"You have successfully rated '{st.session_state['selected_recipe']}' with {st.session_state['ratings'][st.session_state['selected_user']][st.session_state['selected_recipe']]} stars.")
    st.session_state["rating_submitted"] = False  # Reset for next rating



