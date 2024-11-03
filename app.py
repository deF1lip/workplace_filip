import streamlit as st

# Funktion, um den WG-Namen zu speichern
def get_wg_name():
    if 'wg_name' not in st.session_state:
        st.session_state['wg_name'] = None

    if st.session_state['wg_name'] is None:
        st.session_state['wg_name'] = st.text_input("Gib den Namen deiner WG ein:", key="wg_input")
        if st.session_state['wg_name']:
            st.success(f"WG-Name '{st.session_state['wg_name']}' wurde gespeichert.")

# App-Layout
st.title("Waistless")

# Initiale Eingabe des WG-Namens
get_wg_name()

# Hauptinhalt der App
if st.session_state['wg_name']:
    st.write(f"Willkommen in der Waistless-App für die WG '{st.session_state['wg_name']}'!")
else:
    st.warning("Bitte gib einen WG-Namen ein, um fortzufahren.")
