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

import streamlit as st

# Initialisierung des Inventars im Session State
if "inventory" not in st.session_state:
    st.session_state["inventory"] = []

def fridge_page():
    st.title("Kühlschrank")

    # Eingabefelder für Lebensmittel, Menge und Preis
    food_item = st.text_input("Geben Sie ein Lebensmittel ein, das Sie hinzufügen möchten:")
    quantity = st.number_input("Menge:", min_value=1, step=1)
    price = st.number_input("Preis (in Euro):", min_value=0.0, format="%.2f")

    # Button zum Hinzufügen des Lebensmittels
    if st.button("Lebensmittel hinzufügen"):
        if food_item and quantity > 0 and price >= 0:
            item_entry = {"Lebensmittel": food_item, "Menge": quantity, "Preis": price}
            st.session_state["inventory"].append(item_entry)
            st.success(f"'{food_item}' wurde zum Inventar hinzugefügt.")
        else:
            st.warning("Bitte geben Sie alle Informationen ein.")

    # Anzeige des aktuellen Inventars
    if st.session_state["inventory"]:
        st.write("Aktuelles Inventar:")
        for item in st.session_state["inventory"]:
            st.write(f"- {item['Lebensmittel']}: {item['Menge']} Stück, Preis: {item['Preis']}€")
    else:
        st.write("Das Inventar ist leer.")



# Funktion
if st.session_state["page"] == "fridge":
    fridge_page()