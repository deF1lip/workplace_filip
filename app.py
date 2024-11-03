import streamlit as st

# Erste Seite: WG-Daten eingeben
def flat_name():
    st.title("♻️ Wasteless App - Setup")

    # WG Name eingeben
    if 'flat_name' not in st.session_state:
        st.session_state.flat_name = ""
    flat_name_input = st.text_input("Enter your flat name:", value=st.session_state.flat_name)
    if flat_name_input:
        st.session_state.flat_name = flat_name_input

    # Erst wenn WG-Name eingegeben ist, wird die Teilnehmer-Eingabe aktiviert
    if st.session_state.flat_name:
        st.write("### Add flatmates")

        if 'flatmates' not in st.session_state:
            st.session_state.flatmates = []

        # Dynamisch generiertes Eingabefeld für jeden neuen Mitbewohner
        new_flatmate = st.text_input("Add a flatmate:", key=f"flatmate_{len(st.session_state.flatmates)}")
        if st.button("Add Flatmate", key=f"add_button_{len(st.session_state.flatmates)}"):
            if new_flatmate and new_flatmate not in st.session_state.flatmates:
                st.session_state.flatmates.append(new_flatmate)
                st.success(f"{new_flatmate} added!")
                # Neues Eingabefeld automatisch generieren
                st.experimental_rerun()

        if st.session_state.flatmates:
            st.write("### Current flatmates:")
            for index, mate in enumerate(st.session_state.flatmates, start=1):
                st.write(f"{index}. {mate}")

        # Button zum Beenden des Hinzufügens und zur Weiterleitung zur nächsten Seite
        if st.button("Finish"):
            st.session_state.finished_setup = True
            st.experimental_rerun()

# Nächste Seite anzeigen, wenn die WG-Daten abgeschlossen sind
def welcome_page():
    st.title("Welcome!")
    st.write(f"### Welcome to {st.session_state.flat_name} WG")

# Streamlit App Logik
if 'finished_setup' not in st.session_state:
    st.session_state.finished_setup = False

if not st.session_state.finished_setup:
    flat_name()
else:
    welcome_page()
