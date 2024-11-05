import streamlit as st

# Initialize session state variables
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""
if "roommates" not in st.session_state:
    st.session_state["roommates"] = []
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "settings"

# Function to change pages
def change_page(new_page):
    st.session_state["page"] = new_page

# Sidebar navigation with buttons
st.sidebar.title("Navigation")
if st.sidebar.button("Overview"):
    change_page("overview")
if st.sidebar.button("Fridge"):
    change_page("fridge")
if st.sidebar.button("Recipes"):
    change_page("recipes")
if st.sidebar.button("Settings"):
    change_page("settings")

# Function for the overview page
def overview_page():
    # Sets the title to "Overview: Name of the flat"
    title = f"Overview: {st.session_state['flate_name']}" if st.session_state["flate_name"] else "Overview"
    st.title(title)
    st.write("Welcome to the main page of your app.")
    st.write("Here you can display general information.")

# Function for the fridge page
def fridge_page():
    st.title("Fridge")
    st.write("This is the content of the Fridge page.")
    st.text_input("Enter your name:", key="name_input_fridge")
    st.button("Confirm")

# Function for the recipes page
def recipes_page():
    st.title("Recipes")
    st.write("This is the content of the Recipes page.")
    st.slider("Choose a value:", 0, 100, 50, key="slider_recipes")

# Setup page for entering the flat name
def setup_flat_name():
    st.dialog("🏠 Wasteless App - Setup")
        flate_name = st.text_input("Please enter your flat name")
        if st.button("Confirm Flat Name"):
            if flate_name:
                st.session_state["flate_name"] = flate_name
                st.success(f"You successfully set the flat name to '{flate_name}'.")
            else:
                st.warning("Please enter a flat name.")

# Main page for entering roommates
def setup_roommates():
    st.title(f"Welcome to the flat '{st.session_state['flate_name']}'!")
    room_mate = st.text_input("Please enter the name of a roommate", key="room_mate_input")
    if st.button("Add a new roommate"):
        add_roommate(room_mate)
    display_roommates()
    if st.button("Finish Setup"):
        st.session_state["setup_finished"] = True

# Function to add a roommate
def add_roommate(room_mate):
    if room_mate and room_mate not in st.session_state["roommates"]:
        st.session_state["roommates"].append(room_mate)
        st.success(f"Roommate '{room_mate}' has been added.")
    elif room_mate in st.session_state["roommates"]:
        st.warning(f"Roommate '{room_mate}' is already on the list.")

# Function to display the list of roommates
def display_roommates():
    if st.session_state["roommates"]:
        st.write("Current roommates:")
        for mate in st.session_state["roommates"]:
            st.write(f"- {mate}")

# Settings page when setup is complete
def settings_page():
    st.write("Congratulations, your settings are complete.")
    change_flat_name()
    manage_roommates()

# Function to change the flat name
def change_flat_name():
    with st.expander("Change Flat Name"):
        flate_name = st.text_input("Please enter a new flat name", key="change_flat_name")
        if st.button("Change Flat Name"):
            if flate_name:
                st.session_state["flate_name"] = flate_name
                st.success(f"You successfully changed the flat name to '{flate_name}'.")
            else:
                st.warning("Please enter a new flat name.")

# Function to manage roommates
def manage_roommates():
    with st.expander("Manage Roommates"):
        room_mate = st.text_input("Please enter the name of a roommate", key="new_room_mate_input")
        if st.button("Add New Roommate"):
            add_roommate(room_mate)
        display_roommates()
        remove_roommate()

# Function to remove a roommate
def remove_roommate():
    if st.session_state["roommates"]:
        roommate_to_remove = st.selectbox("Select a roommate to remove", st.session_state["roommates"])
        if st.button("Remove Roommate"):
            if roommate_to_remove in st.session_state["roommates"]:
                st.session_state["roommates"].remove(roommate_to_remove)
                st.success(f"Roommate '{roommate_to_remove}' has been removed.")



# Page display logic for the selected page
if st.session_state["page"] == "overview":
    overview_page()
elif st.session_state["page"] == "fridge":
    fridge_page()
elif st.session_state["page"] == "recipes":
    recipes_page()
elif st.session_state["page"] == "settings":
    if not st.session_state["setup_finished"]:
        if st.session_state["flate_name"] == "":
            setup_flat_name()
        else:
            setup_roommates()
    else:
        settings_page()


