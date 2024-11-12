import streamlit as st
import requests
import random
import pandas as pd
from datetime import datetime

# API-Key and URL for Spoonacular
API_KEY = 'b9265fc480cb489d9223fe572f840f30'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# Initialisation
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {
        "Tomato": {"Quantity": 5, "Unit": "gram", "Price": 3.0},
        "Banana": {"Quantity": 3, "Unit": "gram", "Price": 5.0},
        "Onion": {"Quantity": 2, "Unit": "piece", "Price": 1.5},
        "Garlic": {"Quantity": 3, "Unit": "clove", "Price": 0.5},
        "Olive Oil": {"Quantity": 1, "Unit": "liter", "Price": 8.0},
        # ... (other items as needed)
    }

if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Bilbo", "Frodo", "Gandalf der Weise"]
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None
if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}
if "recipe_suggestions" not in st.session_state:
    st.session_state["recipe_suggestions"] = []
if "selected_recipe" not in st.session_state:
    st.session_state["selected_recipe"] = None
if "selected_recipe_link" not in st.session_state:
    st.session_state["selected_recipe_link"] = None
if "cooking_history" not in st.session_state:
    st.session_state["cooking_history"] = []

# Recipe suggestion function
def get_recipes_from_inventory(selected_ingredients=None):
    ingredients = selected_ingredients if selected_ingredients else list(st.session_state["inventory"].keys())
    if not ingredients:
        st.warning("Inventory is empty. Please restock.")
        return [], {}
    
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
        recipe_links = {}
        for recipe in recipes:
            recipe_link = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}"
            recipe_titles.append(recipe['title'])
            recipe_links[recipe['title']] = recipe_link
        return recipe_titles, recipe_links
    else:
        st.error("Error fetching recipes. Please check your API key and try again.")
        return [], {}

# Rating function
def rate_recipe(recipe_title, recipe_link):
    st.subheader(f"Rate the recipe: {recipe_title}")
    st.write(f"**{recipe_title}**: ([View Recipe]({recipe_link}))")
    rating = st.slider("Rate with stars (1-5):", 1, 5, key=f"rating_{recipe_title}")
    
    if st.button("Submit Rating"):
        user = st.session_state["selected_user"]
        if user:
            if user not in st.session_state["ratings"]:
                st.session_state["ratings"][user] = {}
            st.session_state["ratings"][user][recipe_title] = rating
            st.success(f"You have rated '{recipe_title}' with {rating} stars!")
            
            # Save to cooking history
            st.session_state["cooking_history"].append({
                "user": user,
                "recipe": recipe_title,
                "rating": rating,
                "link": recipe_link,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            st.warning("Please select a user first.")

# Main application flow
def receipt_page():
    st.title("Who wants to cook a recipe?")
    if st.session_state["roommates"]:
        selected_user = st.selectbox("Select the roommate:", st.session_state["roommates"])
        st.session_state["selected_user"] = selected_user  # Save selected user to session state
        
        # Recipe Search Options
        st.subheader("Recipe Search Options")
        search_mode = st.radio("Choose a search mode:", ("Automatic (use all inventory)", "Custom (choose ingredients)"))
        
        # Recipe selection form
        with st.form("recipe_form"):
            if search_mode == "Custom (choose ingredients)":
                selected_ingredients = st.multiselect("Select ingredients from inventory:", st.session_state["inventory"].keys())
            else:
                selected_ingredients = None  # Use the entire inventory
            
            search_button = st.form_submit_button("Get Recipe Suggestions")
            if search_button and not st.session_state["recipe_suggestions"]:
                recipe_titles, recipe_links = get_recipes_from_inventory(selected_ingredients)
                st.session_state["recipe_suggestions"] = recipe_titles
                st.session_state["recipe_links"] = recipe_links

        # Display recipe suggestions
        if st.session_state["recipe_suggestions"]:
            selected_recipe = st.selectbox("Select a recipe to make", ["Please choose..."] + st.session_state["recipe_suggestions"])
            if selected_recipe != "Please choose...":
                st.session_state["selected_recipe"] = selected_recipe
                st.session_state["selected_recipe_link"] = st.session_state["recipe_links"][selected_recipe]
                st.success(f"You have chosen to make '{selected_recipe}'!")

    else:
        st.warning("No roommates available.")
        return

    # Display the rating section if a recipe was selected
    if st.session_state["selected_recipe"] and st.session_state["selected_recipe_link"]:
        rate_recipe(st.session_state["selected_recipe"], st.session_state["selected_recipe_link"])

    # Display the ratings summary in a table
    if st.session_state["ratings"]:
        with st.expander("Ratings Summary"):
            rating_data = [
                {"Recipe": recipe, "Rating": rating}
                for user_ratings in st.session_state["ratings"].values()
                for recipe, rating in user_ratings.items()
            ]
            st.table(pd.DataFrame(rating_data))

    # Display cooking history in a table
    if st.session_state["cooking_history"]:
        with st.expander("Cooking History"):
            history_data = [
                {
                    "Person": entry["user"],
                    "Recipe": entry["recipe"],
                    "Rating": entry["rating"],
                    "Date": entry["timestamp"]
                }
                for entry in st.session_state["cooking_history"]
            ]
            st.table(pd.DataFrame(history_data))

# Run the receipt page
receipt_page()

