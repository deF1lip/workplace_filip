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
import pandas as pd

# Initialisierung des Inventars im Session State als DataFrame
if "inventory" not in st.session_state:
    st.session_state["inventory"] = pd.DataFrame(columns=["Lebensmittel", "Menge (g/ml)", "Kosten (CHF)"])

def fridge_page():
    st.title("Kühlschrank")

    # Formular zur Eingabe von Lebensmitteln, Menge und Kosten
    with st.form(key="food_form"):
        lebensmittel = st.text_input("Lebensmittel")
        menge = st.number_input("Menge (g/ml)", min_value=0.0, format="%.2f")
        kosten = st.number_input("Kosten (CHF)", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button(label="Hinzufügen")

    # Wenn das Formular abgeschickt wird, füge den Eintrag zum Inventar hinzu
    if submit_button:
        if lebensmittel and menge > 0 and kosten >= 0:
            new_entry = {"Lebensmittel": lebensmittel, "Menge (g/ml)": menge, "Kosten (CHF)": kosten}
            st.session_state["inventory"] = st.session_state["inventory"].append(new_entry, ignore_index=True)
            st.success(f"{lebensmittel} wurde dem Inventar hinzugefügt.")
        else:
            st.error("Bitte geben Sie gültige Werte für alle Felder ein.")

    # Anzeige des aktuellen Inventars in Tabellenform
    if not st.session_state["inventory"].empty:
        st.subheader("Aktuelles Inventar")
        st.dataframe(st.session_state["inventory"])
    else:
        st.info("Das Inventar ist derzeit leer.")






# Funktion
if st.session_state["page"] == "fridge":
    fridge_page()