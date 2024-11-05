import streamlit as st


# Initialisierung des Inventars im Session State
if "inventory" not in st.session_state:
    st.session_state["inventory"] = []

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
    import streamlit as st



def fridge_page():
    st.title("Kühlschrank")

    # Eingabefeld für Lebensmittel
    food_item = st.text_input("Geben Sie ein Lebensmittel ein, das Sie hinzufügen möchten:")

    # Button zum Hinzufügen des Lebensmittels
    if st.button("Lebensmittel hinzufügen"):
        if food_item:
            st.session_state["inventory"].append(food_item)
            st.success(f"'{food_item}' wurde zum Inventar hinzugefügt.")
        else:
            st.warning("Bitte geben Sie ein Lebensmittel ein.")

    # Anzeige des aktuellen Inventars
    if st.session_state["inventory"]:
        st.write("Aktuelles Inventar:")
        for item in st.session_state["inventory"]:
            st.write(f"- {item}")
    else:
        st.write("Das Inventar ist leer.")



# Funktion
if st.session_state["page"] == "fridge":
    fridge_page()