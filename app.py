import streamlit as st


# sidebar with selectboxes
page= st.sidebar.selectbox("overiew","fridge", "recips", "settings")


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


