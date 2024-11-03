import streamlit as st

# Erste Seite: WG-Daten eingeben
def flat_name():
    st.title("♻️ Wasteless App - Setup")
    
    # WG Name eingeben
    flat_name = st.text_input("Enter your flat name:")
    
    # Initialisiere eine leere Liste für Mitbewohner
    if 'flatmates' not in st.session_state:
        st.session_state.flatmates = []
    
    # Eingabefeld für das Hinzufügen von Mitbewohnern
    new_flatmate = st.text_input("Add a flatmate:")
    if st.button("Add"):
        if new_flatmate and new_flatmate not in st.session_state.flatmates:
            st.session_state.flatmates.append(new_flatmate)
            st.success(f"{new_flatmate} added!")

    # Liste der aktuellen Mitbewohner anzeigen
    if st.session_state.flatmates:
        st.write("Current flatmates:")
        for mate in st.session_state.flatmates:
            st.write(f"- {mate}")

