import streamlit as st

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


def fridge_page():
    st.title("Fridge")
    st.write("This is the content of the Fridge page.")
    st.text_input("Enter your name:", key="name_input_fridge")
    st.button("Confirm")



# Funktion
if st.session_state["page"] == "fridge":
    fridge_page()