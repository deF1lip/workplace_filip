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
        "Garlic": {"Quantity": 3, "Unit": "clove", "Price": 0.5},
        "Olive Oil": {"Quantity": 1, "Unit": "liter", "Price": 8.0},
        # ... (other items as needed)
    }
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Bilbo", "Frodo", "Gandalf der Weise"]  # Example roommates list
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None
if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}
if "search_triggered" not in st.session_state:
    st.session_state["search_triggered"] = False
if "selected_recipe" not in st.session_state:
    st.session_state["selected_recipe"] = None

# Choose roommate
def select_user():
    st.title("Who are you")
    if st.session_state["roommates"]:
        selected_user = st.selectbox("Choose your name:", st.session_state["roommates"], 
                                     index=st.session_state["roommates"].index(st.session_state["selected_user"]) 
                                     if st.session_state["selected_user"] else 0)
        st.session_state["selected_user"] = selected_user
        st.write(f"Hi, {selected_user}!")
    else:
        st.warning("No user was added.")

# Call up recipe suggestions based on inventory or selected ingredients
def get_recipes_from_inventory(selected_ingredients=None):
    ingredients = selected_ingredients if selected_ingredients else list(st.session_state["inventory"].keys())
    if not ingredients:
        st.warning("Inventory is empty. Please restock.") 
        return []
    
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

# Rating function with stars
def rate_recipe(recipe_title):
    st.subheader(f"Rate the recipe: {recipe_title}")
    rating = st.slider("Rate with stars (1-5):", 1, 5, key=f"rating_{recipe_title}")
    
    if st.button("Submit Rating"):
        user = st.session_state["selected_user"]
        if user:
            # Store rating in session state
            if user not in st.session_state["ratings"]:
                st.session_state["ratings"][user] = {}
            st.session_state["ratings"][user][recipe_title] = rating
            st.success(f"You have rated '{recipe_title}' with {rating} stars!")
        else:
            st.warning("Please select a user first.")

# Main application flow
select_user()

# User choice for recipe search mode
st.subheader("Recipe Search Options")
search_mode = st.radio("Choose a search mode:", ("Automatic (use all inventory)", "Custom (choose ingredients)"))

# Define a form for recipe suggestions
with st.form("recipe_form"):
    if search_mode == "Custom (choose ingredients)":
        selected_ingredients = st.multiselect("Select ingredients from inventory:", st.session_state["inventory"].keys())
    else:
        selected_ingredients = None  # Use the entire inventory

    search_button = st.form_submit_button("Get Recipe Suggestions")
    if search_button:
        st.session_state["search_triggered"] = True  # Mark search as triggered

# Display the recipe suggestions if search was triggered
if st.session_state["search_triggered"]:
    if st.session_state["selected_user"]:
        recipe_titles = get_recipes_from_inventory(selected_ingredients)
        if recipe_titles:
            # Let the user choose one recipe to make
            selected_recipe = st.selectbox("Select a recipe to make", recipe_titles, key="selected_recipe")
            if st.button("Choose this recipe"):
                st.session_state["selected_recipe"] = selected_recipe
                st.success(f"You have chosen to make '{selected_recipe}'!")
            st.session_state["search_triggered"] = False  # Reset the trigger after displaying
    else:
        st.warning("Please select a user first.")

# Display the chosen recipe for rating
if st.session_state["selected_recipe"]:
    rate_recipe(st.session_state["selected_recipe"])
    if st.session_state["ratings"]:
        st.subheader("Ratings Summary")
        for user, user_ratings in st.session_state["ratings"].items():
            st.write(f"**{user}'s Ratings:**")
            for recipe, rating in user_ratings.items():
                st.write(f"- {recipe}: {rating} stars")


