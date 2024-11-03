import streamlit as st

# Funktion für die Eingabeseite
def flat_name_input():
    st.title("♻️ Wasteless App - Setup")

    # Eingabefeld für den Flat-Namen
    flat_name = st.text_input("Enter your flat name:")

    # Button zur Bestätigung des Flat-Namens
    if st.button("Approve Flat Name"):
        if flat_name:
            st.session_state.flat_name = flat_name  # Speichert den Namen in der Session
            st.success(f"Flat name '{flat_name}' has been set!")
            st.session_state.page = "welcome"  # Wechselt zur nächsten Seite
            st.experimental_rerun()
        else:
            st.warning("Please enter a flat name.")

# Funktion für die Willkommensseite
def welcome_page():
    st.title("Welcome!")
    if 'flat_name' in st.session_state:
        st.write(f"### Herzlich willkommen in der WG '{st.session_state.flat_name}'!")
        st.write("Bitte gebe die weiteren Teilnehmer ein.")
    else:
        st.warning("No flat name found. Please go back to the setup page.")

# Steuert die Navigation zwischen den Seiten
if 'page' not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    flat_name_input()
elif st.session_state.page == "welcome":
    welcome_page()



