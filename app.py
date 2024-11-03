import streamlit as st

# Funktion für die Eingabeseite des Flat-Namens
def flat_name_input():
    st.title("♻️ Wasteless App - Setup")

    # Eingabefeld für den Flat-Namen
    flat_name = st.text_input("Enter your flat name:")

    # Button zur Bestätigung des Flat-Namens
    if st.button("Approve Flat Name"):
        if flat_name:
            st.session_state.flat_name = flat_name  # Speichert den Namen in der Session
            st.session_state.page = "add_participants"  # Wechselt zur nächsten Seite
            st.experimental_rerun()
        else:
            st.warning("Please enter a flat name.")

# Funktion für die Eingabeseite der Teilnehmer
def add_participants():
    st.title(f"Welcome to '{st.session_state.flat_name}' WG!")
    st.write("### Add new flatmates")

    # Initialisiere die Liste der Teilnehmer, falls nicht vorhanden
    if 'flatmates' not in st.session_state:
        st.session_state.flatmates = []

    # Initialisiere den Wert des Eingabefelds für die neue Person
    if 'new_flatmate' not in st.session_state:
        st.session_state.new_flatmate = ""

    # Eingabefeld für die neue Person
    new_flatmate = st.text_input("Enter a flatmate's name:", value=st.session_state.new_flatmate, key="flatmate_input")

    # Button zur Bestätigung der neuen Person
    if st.button("Add Flatmate"):
        if new_flatmate and new_flatmate not in st.session_state.flatmates:
            st.session_state.flatmates.append(new_flatmate)
            st.session_state.new_flatmate = ""  # Leert das Eingabefeld nach dem Hinzufügen
            st.success(f"{new_flatmate} added!")
            st.experimental_rerun()
        elif new_flatmate in st.session_state.flatmates:
            st.warning(f"{new_flatmate} is already added.")
        else:
            st.warning("Please enter a flatmate's name.")

    # Anzeige der aktuellen Liste der Teilnehmer
    if st.session_state.flatmates:
        st.write("### Current flatmates:")
        for index, mate in enumerate(st.session_state.flatmates, start=1):
            st.write(f"{index}. {mate}")

# Steuert die Navigation zwischen den Seiten
if 'page' not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    flat_name_input()
elif st.session_state.page == "add_participants":
    add_participants()

