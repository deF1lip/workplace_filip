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
if "selected_recipe_link" not in st.session_state:
    st.session_state["selected_recipe_link"] = None
if "recipe_suggestions" not in st.session_state:
    st.session_state["recipe_suggestions"] = None
if "recipe_links" not in st.session_state:
    st.session_state["recipe_links"] = None
if "recipe_confirmed" not in st.session_state:
    st.session_state["recipe_confirmed"] = False

# Recipe suggestion function
def get_recipes_from_inventory(selected_ingredients=None):
    ingredients = selected_ingredients if selected_ingredients else list(st.session_state["inventory"].keys())
    if not ingredients:
        st.warning("Inventory is empty. Please restock.")
        return [], {}
    
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
        recipe_links = {}
        if recipes:
            random.shuffle(recipes)
            st.subheader("Recipe Suggestions")
            for recipe in recipes[:3]:  # Limiting to 3 recipes
                recipe_title = recipe["title"]
                recipe_link = f"https://spoonacular.com/recipes/{recipe_title.replace(' ', '-')}-{recipe['id']}"
                recipe_titles.append(recipe_title)
                recipe_links[recipe_title] = recipe_link
                st.write(f"- **{recipe_title}** ([View Recipe]({recipe_link}))")
                
                missed_ingredients = recipe.get("missedIngredients", [])
                if missed_ingredients:
                    missed_names = [item["name"] for item in missed_ingredients]
                    st.write(f"  *Extra ingredients needed:* {', '.join(missed_names)}")
                
            return recipe_titles, recipe_links
        else:
            st.write("No recipes found with the current ingredients.")
            return [], {}
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
        else:
            st.warning("Please select a user first.")

# Main application flow
def receipt_page():
    st.title("Who wants to cook a recipe?")
    
    selected_user = st.selectbox("Select the roommate:", st.session_state["roommates"])
    st.session_state["selected_user"] = selected_user  # Save selected user to session state
    
    # Recipe Search Options
    st.subheader("Recipe Search Options")
    search_mode = st.radio("Choose a search mode:", ("Automatic (use all inventory)", "Custom (choose ingredients)"))

    # Trigger recipe search only when there's no previous suggestion or on explicit update
    if st.session_state["recipe_suggestions"] is None or st.button("Get Recipe Suggestions"):
        selected_ingredients = None
        if search_mode == "Custom (choose ingredients)":
            selected_ingredients = st.multiselect("Select ingredients from inventory:", st.session_state["inventory"].keys())
        
        # Fetch and display recipes
        recipe_titles, recipe_links = get_recipes_from_inventory(selected_ingredients)
        st.session_state["recipe_suggestions"] = recipe_titles
        st.session_state["recipe_links"] = recipe_links

    # Display recipe suggestions if available
    if st.session_state["recipe_suggestions"]:
        selected_recipe = st.selectbox("Select a recipe to make", st.session_state["recipe_suggestions"], key="selected_recipe_choice")
        st.session_state["selected_recipe"] = selected_recipe
        st.session_state["selected_recipe_link"] = st.session_state["recipe_links"][selected_recipe]
        
        # Confirm the recipe choice
        if st.button("Confirm Recipe Choice"):
            st.session_state["recipe_confirmed"] = True
            st.success(f"You have chosen to make '{selected_recipe}'!")
    
    # Rating section after recipe confirmation
    if st.session_state["recipe_confirmed"]:
        rate_recipe(st.session_state["selected_recipe"], st.session_state["selected_recipe_link"])

    # Ratings summary
    if st.session_state["ratings"]:
        with st.expander("Ratings Summary"):
            for user, user_ratings in st.session_state["ratings"].items():
                st.write(f"**{user}'s Ratings:**")
                for recipe, rating in user_ratings.items():
                    st.write(f"- {recipe}: {rating} stars")

# Run the receipt page
receipt_page()

