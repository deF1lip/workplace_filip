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
        # ... (and other items)
    }
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Bilbo", "Frodo", "Gandalf der Weise"]
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None
if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}
if "temp_rating" not in st.session_state:
    st.session_state["temp_rating"] = None
if "selected_recipe" not in st.session_state:
    st.session_state["selected_recipe"] = None
if "rating_submitted" not in st.session_state:
    st.session_state["rating_submitted"] = False  # Track if rating was just submitted

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

# Function to handle rating
def number_rating(recipe_title):
    st.write(f"Rate {recipe_title}:")
    temp_rating = st.selectbox("Select a rating:", [1, 2, 3, 4, 5], key=f"temp_rating_{recipe_title}")
    st.session_state["temp_rating"] = temp_rating

    if st.button(f"Submit Rating for {recipe_title}"):
        user = st.session_state["selected_user"]
        if user:
            # Store rating in session state
            if user not in st.session_state["ratings"]:
                st.session_state["ratings"][user] = {}
            st.session_state["ratings"][user][recipe_title] = temp_rating
            st.session_state["rating_submitted"] = True  # Indicate rating was submitted
            st.success(f"{user} rated {recipe_title} with {temp_rating} stars!")
        else:
            st.warning("Please select a user first.")

    # Display the current rating for this user and recipe
    user = st.session_state["selected_user"]
    if user in st.session_state["ratings"] and recipe_title in st.session_state["ratings"][user]:
        current_rating = st.session_state["ratings"][user][recipe_title]
        st.write(f"You rated '{recipe_title}' with {current_rating} stars.")

# Call up recipe suggestions based on inventory
def get_recipes_from_inventory():
    ingredients = list(st.session_state["inventory"].keys())
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

# Main application flow
select_user()

# Fetch recipe suggestions only if a user is selected
if st.button("Get Recipe Suggestions"):
    st.session_state["rating_submitted"] = False  # Reset submission flag when fetching new

