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
        # Add other items as needed
    }
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Bilbo", "Frodo", "Gandalf der Weise"]
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None
if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}
if "temp_rating" not in st.session_state:
    st.session_state["temp_rating"] = None

# Choose roommate
def select_user():
    st.title("Who are you")
    selected_user = st.selectbox("Choose your name:", st.session_state["roommates"])
    st.session_state["selected_user"] = selected_user
    st.write(f"Hi, {selected_user}!")

def number_rating(recipe_title):
    st.write(f"Rate {recipe_title}:")
    
    # Rating selection (with key for unique state tracking)
    temp_rating = st.selectbox("Select a rating:", [1, 2, 3, 4, 5], key=f"rating_{recipe_title}")
    st.session_state["temp_rating"] = temp_rating
    
    # Submit button
    submit_button_key = f"submit_{recipe_title}"
    if st.button(f"Submit Rating for {recipe_title}", key=submit_button_key):
        if st.session_state["selected_user"]:
            # Ensure ratings are stored per user and per recipe
            user = st.session_state["selected_user"]
            if user not in st.session_state["ratings"]:
                st.session_state["ratings"][user] = {}
            st.session_state["ratings"][user][recipe_title] = st.session_state["temp_rating"]
            st.success(f"{user} rated {recipe_title} with {st.session_state['temp_rating']} stars!")
            st.session_state["temp_rating"] = None  # Clear the temp rating after submission
        else:
            st.warning("Please select a user first.")

# Get recipes based on inventory
def get_recipes_from_inventory():
    ingredients = list(st.session_state["inventory"].keys())
    if not ingredients:
        st.warning("Inventory is empty. Please add items.")
        return []
    
    # API parameters
    params = {
        "ingredients": ",".join(ingredients),
        "number": 100,
        "ranking": 2,
        "apiKey": API_KEY
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    if response.status_code == 200:
        recipes = response.json()
        recipe_titles = []
        if recipes:
            random.shuffle(recipes)
            st.subheader("Recipe Suggestions")
            displayed_recipes = 0
            for recipe in recipes:
                missed_ingredients = recipe.get("missedIngredientCount", 0)
                if missed_ingredients <= 2:
                    recipe_link = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}"
                    st.write(f"- **{recipe['title']}** ([View Recipe]({recipe_link}))")
                    recipe_titles.append(recipe['title'])
                    displayed_recipes += 1
                    if missed_ingredients > 0:
                        missed_names = [item["name"] for item in recipe.get("missedIngredients", [])]
                        st.write(f"  *Extra ingredients needed:* {', '.join(missed_names)}")
                    if displayed_recipes >= 3:
                        break
            return recipe_titles
        else:
            st.write("No recipes found with the current ingredients.")
            return []
    else:
        st.error("Error fetching recipes. Please check your API key and try again.")
        return []

select_user()

# Fetch recipe suggestions if a user is selected
if st.button("Get Recipe Suggestions"):
    if st.session_state["selected_user"]:
        recipe_titles = get_recipes_from_inventory()
        if recipe_titles:
            selected_recipe = st.selectbox("Select a recipe to rate", recipe_titles)
            if selected_recipe:
                number_rating(selected_recipe)
    else:
        st.warning("Please select a user first.")

# Display ratings for each user
if st.session_state["ratings"]:
    st.subheader("Ratings Summary")
    for user, user_ratings in st.session_state["ratings"].items():
        st.write(f"**{user}'s Ratings:**")
        for recipe, rating in user_ratings.items():
            st.write(f"- {recipe}: {rating} stars")