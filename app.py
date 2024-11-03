import streamlit as st

# Funktion, um den WG-Namen zu speichern
def name_sharedflat():
    if "SF_name" not in st.session_state:
        st.session_state["SF_name"] = None

    if st.session_state["SF_name"] is None:
        st.session_state["SF_name"] = st.text_input("Enter the name of your shared flat:", key="wg_input")
        if st.session_state["SF_name"]:
            st.success(f"Shared flat '{st.session_state['SF_name']}' wurde gespeichert.")

# App-Layout
st.title("Waistless")

# Initiale Eingabe des WG-Namens
name_sharedflat()

# Hauptinhalt der App
if st.session_state["SF_name"]:
    st.write(f"Willkommen in der Waistless-App für die WG '{st.session_state['SF_name']}'!")
else:
    st.warning("Please enter a flat-share name to continue.")
