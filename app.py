import streamlit as st

# open first the setting page to define flate-name and inhabitants
if "pages" not in st.session_state:
    st.session_state ["page"] = "settings"

# Function to change between the pages
def change_page(new_page):
    st.session_state["page"] = new_page


# sidebar with selectboxes
st.sidebar.title("Navigation")
st.sidebar.selectbox("overview","Livio", "Flurin") )
st.sidebar.button("fridge", on_click=lambda: change_page('fridge'))
st.sidebar.button("recipes", on_click=lambda: change_page("recipes"))
st.sidebar.button("settings", on_click=lambda: change_page("settings"))



# Anzeigelogik für jede Seite
if st.session_state["page"] == "overview":
    st.title("overview")
    st.write('Willkommen auf der Startseite deiner App.')
    st.write('Hier kannst du allgemeine Informationen anzeigen.')
elif st.session_state["page"] == "fridge":
    st.title("fridge")
    st.write('Dies ist der Inhalt von Seite 1.')
    st.text_input('Gib deinen Namen ein:', key='name_input_page1')
    st.button('Bestätigen')
elif st.session_state["page"] == "recipes":
    st.title("recipes")
    st.write('Dies ist der Inhalt von Seite 2.')
    st.slider('Wähle einen Wert:', 0, 100, 50, key='slider_page2')
elif st.session_state["page"] == "settings":
    st.title("settings")
    st.write('Dies ist der Inhalt von Seite 1.')
    st.text_input('Gib deinen Namen ein:', key='name_input_page1')
    st.button('Bestätigen')



