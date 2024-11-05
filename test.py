import streamlit as st
import pandas as pd

# Initialisierung der Session-State-Variablen
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Beispielhafte Mitbewohnerliste
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {}
if "expenses" not in st.session_state:
    st.session_state["expenses"] = {mate: 0.0 for mate in st.session_state["roommates"]}

def fridge_page():
    st.title("Kühlschrank")

    # Auswahl des Mitbewohners
    if st.session_state["roommates"]:
        selected_roommate = st.selectbox("Wähle den Mitbewohner:", st.session_state["roommates"])
    else:
        st.warning("Es sind keine Mitbewohner vorhanden.")
        return

    # Auswahl der Aktion: Hinzufügen oder Entfernen
    action = st.selectbox("Möchtest du ein Lebensmittel hinzufügen oder entfernen?", ["Hinzufügen", "Entfernen"])

    if action == "Hinzufügen":
        # Eingabefelder für Lebensmittel, Menge und Preis
        food_item = st.text_input("Gib ein Lebensmittel ein, das du hinzufügen möchtest:")
        quantity = st.number_input("Menge:", min_value=1, step=1)
        price = st.number_input("Preis (in Euro):", min_value=0.0, format="%.2f")

        # Button zum Hinzufügen des Lebensmittels
        if st.button("Lebensmittel hinzufügen"):
            if food_item and quantity > 0 and price >= 0 and selected_roommate:
                if food_item in st.session_state["inventory"]:
                    st.session_state["inventory"][food_item]["Menge"] += quantity
                    st.session_state["inventory"][food_item]["Preis"] += price
                else:
                    st.session_state["inventory"][food_item] = {"Menge": quantity, "Preis": price}
                st.session_state["expenses"][selected_roommate] += price
                st.success(f"'{food_item}' wurde dem Inventar hinzugefügt.")
            else:
                st.warning("Bitte fülle alle Felder aus.")
    elif action == "Entfernen":
        # Auswahl des zu entfernenden Lebensmittels
        if st.session_state["inventory"]:
            food_item = st.selectbox("Wähle ein Lebensmittel zum Entfernen:", list(st.session_state["inventory"].keys()))
            quantity = st.number_input("Menge zum Entfernen:", min_value=1, step=1)

            # Button zum Entfernen des Lebensmittels
            if st.button("Lebensmittel entfernen"):
                if food_item and quantity > 0 and selected_roommate:
                    if food_item in st.session_state["inventory"]:
                        current_quantity = st.session_state["inventory"][food_item]["Menge"]
                        current_price = st.session_state["inventory"][food_item]["Preis"]
                        if quantity <= current_quantity:
                            # Berechnung des Preises pro Einheit
                            price_per_unit = current_price / current_quantity
                            # Berechnung des abzuziehenden Betrags
                            amount_to_deduct = price_per_unit * quantity
                            # Aktualisierung des Inventars
                            st.session_state["inventory"][food_item]["Menge"] -= quantity
                            st.session_state["inventory"][food_item]["Preis"] -= amount_to_deduct
                            # Aktualisierung der Ausgaben des Mitbewohners
                            st.session_state["expenses"][selected_roommate] -= amount_to_deduct
                            st.success(f"'{quantity}' von '{food_item}' wurden entfernt.")
                            # Entfernen des Eintrags, wenn die Menge null erreicht
                            if st.session_state["inventory"][food_item]["Menge"] == 0:
                                del st.session_state["inventory"][food_item]
                        else:
                            st.warning("Die zu entfernende Menge übersteigt die vorhandene Menge.")
                    else:
                        st.warning("Dieses Lebensmittel ist nicht im Inventar.")
                else:
                    st.warning("Bitte fülle alle Felder aus.")
        else:
            st.warning("Das Inventar ist leer.")

    # Anzeige des aktuellen Inventars
    if st.session_state["inventory"]:
        st.write("Aktuelles Inventar:")
        inventory_df = pd.DataFrame.from_dict(st.session_state["inventory"], orient='index')
        inventory_df = inventory_df.reset_index().rename(columns={'index': 'Lebensmittel'})
        st.table(inventory_df)
    else:
        st.write("Das Inventar ist leer.")

    # Anzeige der Gesamtausgaben pro Mitbewohner
    st.write("Gesamtausgaben pro Mitbewohner:")
    expenses_df = pd.DataFrame(list(st.session_state["expenses"].items()), columns=["Mitbewohner", "Gesamtausgaben (€)"])
    st.table(expenses_df)

# Aufruf der Funktion zur Anzeige der Kühlschrank-Seite
fridge_page()
