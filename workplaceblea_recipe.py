import streamlit as st
import requests
import random


# API-Key and URL for Spoonacular
API_KEY = '21c590f808c74caabbaa1494c6196e7a'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# initialisation
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {
        "Tomato": {"Quantity": 5, "Unit": "gram", "Price": 3.0},
        "Banana": {"Quantity": 3, "Unit": "gram", "Price": 5.0},
        "Onion": {"Quantity": 2, "Unit": "piece", "Price": 1.5},
        "Garlic": {"Quantity": 3, "Unit": "clove", "Price": 0.5},
        "Olive Oil": {"Quantity": 1, "Unit": "liter", "Price": 8.0},
        "Chicken Breast": {"Quantity": 2, "Unit": "piece", "Price": 6.0},
        "Pasta": {"Quantity": 500, "Unit": "gram", "Price": 2.5},
        "Rice": {"Quantity": 1000, "Unit": "gram", "Price": 2.0},
        "Salt": {"Quantity": 1, "Unit": "kg", "Price": 1.0},
        "Pepper": {"Quantity": 1, "Unit": "pack", "Price": 1.5},
        "Basil": {"Quantity": 1, "Unit": "bunch", "Price": 2.0},
        "Mozzarella": {"Quantity": 2, "Unit": "piece", "Price": 4.0},
        "Milk": {"Quantity": 1, "Unit": "liter", "Price": 1.5},
        "Egg": {"Quantity": 6, "Unit": "piece", "Price": 3.0},
        "Flour": {"Quantity": 1000, "Unit": "gram", "Price": 1.0},
        "Butter": {"Quantity": 250, "Unit": "gram", "Price": 2.5},
        "Potato": {"Quantity": 5, "Unit": "piece", "Price": 2.0},
        "Carrot": {"Quantity": 4, "Unit": "piece", "Price": 1.5},
        "Bell Pepper": {"Quantity": 2, "Unit": "piece", "Price": 2.5},
        "Cheddar Cheese": {"Quantity": 200, "Unit": "gram", "Price": 3.5},
        "Ground Beef": {"Quantity": 500, "Unit": "gram", "Price": 7.0},
        "Tomato Sauce": {"Quantity": 500, "Unit": "ml", "Price": 2.0},
        "Mushroom": {"Quantity": 200, "Unit": "gram", "Price": 3.0} 
    }
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Bilbo", "Frodo", "Gandalf der Weise"]  # Example roommates list
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None
if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}


# Choose roommate
def select_user():
    st.title("Who are you")
    if st.session_state["roommates"]:
        selected_user = st.selectbox("Choose your name:", st.session_state["roommates"])
        st.session_state["selected_user"] = selected_user
        st.write(f"Hi, {selected_user}!")
    else:
        st.warning("No user was added.")


def number_rating(recipe_title):
    # Displays a numerical rating system (1-5)
    st.write(f"Rate {recipe_title}:")
    rating = st.selectbox("Select a rating:", [1, 2, 3, 4, 5], key=recipe_title)
    if rating:
        st.session_state["ratings"][recipe_title] = rating
        st.success(f"Thanks for rating {recipe_title} with {rating} stars!")



# Call up recipe suggestions based on inventory
def get_recipes_from_inventory():
    # Load Ingredients from Inventory
    ingredients = list(st.session_state["inventory"].keys())
    if not ingredients:
        st.warning("Inventory is empty. Please move your lazy ass to Migros.") 
        return
    # Request to Spoonacular API
    params = {
        "ingredients": ",".join(ingredients), # Ingredients of Inventory
        "number": 100, # Nr of Recipes
        "ranking": 2,  # Prioritize recipes with maximum matching ingredients
        "apiKey": API_KEY
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    # Show results
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            random.shuffle(recipes)
            st.subheader("Recipe Suggestions")
            displayed_recipes = 0
            for recipe in recipes:
                # Show recipes with up to 2 missing ingredients
                missed_ingredients = recipe.get("missedIngredientCount", 0)
                if missed_ingredients <= 2:
                    recipe_link = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}"
                    st.write(f"- **{recipe['title']}** ([View Recipe]({recipe_link}))")
                    displayed_recipes += 1
                    # If there are any missed ingredients, list them
                    if missed_ingredients > 0:
                        missed_names = [item["name"] for item in recipe.get("missedIngredients", [])]
                        st.write(f"  *Extra ingredients needed:* {', '.join(missed_names)}")
                if displayed_recipes >= 3:
                    break
        else:
            st.write("No recipes found with the current ingredients.")
    else:
        st.error("Error fetching recipes. Please check your API key and try again.")


select_user()



if st.button("Get Recipe Suggestions"):
    if st.session_state["selected_user"]:  # Check if a user is selected
        recipe_titles = get_recipes_from_inventory()
        if recipe_titles:
            selected_recipe = st.selectbox("Select a recipe to rate", recipe_titles)
            # Display the rating system after a recipe is selected
            if selected_recipe:
                number_rating(selected_recipe)  # Show rating input for the selected recipe
    else:
        st.warning("Please select a user first.")

if st.session_state["ratings"]:
    st.subheader("Your Ratings")
    for recipe, rating in st.session_state["ratings"].items():
        st.write(f"- {recipe}: {rating} stars")