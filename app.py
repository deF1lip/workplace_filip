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

    # Eingabefeld für die neue Person
    new_flatmate = st.text_input("Enter a flatmate's name:")

    # Button zur Bestätigung der neuen Person
    if st.button("Add Flatmate"):
        if new_flatmate and new_flatmate not in st.session_state.flatmates:
            st.session_state.flatmates.append(new_flatmate)
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

    # Buttons zum Hinzufügen einer weiteren Person oder zum Weitergehen
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add another person"):
            st.experimental_rerun()  # Bleibt auf der Seite, um eine weitere Person hinzuzufügen
    with col2:
        if st.button("Continue"):
            st.write("Proceed to the next step... (implement further functionality here)")

# Steuert die Navigation zwischen den Seiten
if 'page' not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    flat_name_input()
elif st.session_state.page == "add_participants":
    add_participants()



