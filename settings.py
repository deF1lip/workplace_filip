import streamlit as st

# Initialisiere flate_name und roommates in st.session_state
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""

if "roommates" not in st.session_state:
    st.session_state["roommates"] = []

if "room_mate_input" not in st.session_state:
    st.session_state["room_mate_input"] = ""

if "flat_name_confirmed" not in st.session_state:
    st.session_state["flat_name_confirmed"] = False

# Setup-Seite anzeigen, wenn der flat name noch nicht festgelegt ist
if not st.session_state["flat_name_confirmed"]:
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Please enter your flat name")
    
    if st.button("Confirm Flat Name"):
        if flate_name:  # Überprüfen, ob ein Name eingegeben wurde
            st.session_state["flate_name"] = flate_name  # Speichere den Namen
            st.session_state["flat_name_confirmed"] = True  # Bestätigungsstatus setzen

# Hauptseite anzeigen, wenn der flat name festgelegt wurde
if st.session_state["flate_name"] and st.session_state["flat_name_confirmed"]:
    st.title(f"Welcome to {st.session_state['flate_name']}!")
    
    # Eingabe für den Namen eines Mitbewohners
    room_mate = st.text_input("Please enter the name of a roommate", key="room_mate_input")

    # Button zum Hinzufügen des Mitbewohners
    if st.button("Add a new roommate"):
        if room_mate:  # Überprüfen, ob ein Name eingegeben wurde
            if room_mate not in st.session_state["roommates"]:  # Überprüfen, ob der Name nicht schon vorhanden ist
                st.session_state["roommates"].append(room_mate)  # Speichere den Namen
                st.session_state["room_mate_input"] = ""  # Eingabefeld leeren
                st.write(f"Roommate {room_mate} has been added!")
            else:
                st.warning(f"Roommate {room_mate} is already in the list!")

    # Zeige die Liste der Mitbewohner an
    if st.session_state["roommates"]:
        st.write("Current roommates:")
        for mate in st.session_state["roommates"]:
            st.write(f"- {mate}")
