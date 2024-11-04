import streamlit as st

# Initialisiere flate_name und roommates in st.session_state
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""

if "roommates" not in st.session_state:
    st.session_state["roommates"] = []

if "room_mate_input" not in st.session_state:
    st.session_state["room_mate_input"] = ""

# Setup-Seite anzeigen, wenn der flat name noch nicht festgelegt ist
if st.session_state["flate_name"] == "":
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Please enter your flat name")
    
    if st.button("Confirm Flat Name"):
        if flate_name:  # Überprüfen, ob ein Name eingegeben wurde
            st.session_state["flate_name"] = flate_name  # Speichere den Namen

# Hauptseite anzeigen, wenn der flat name festgelegt wurde
if st.session_state["flate_name"]:
    st.title(f"Welcome to {st.session_state['flate_name']}!")
    
    # Eingabe für den Namen eines Mitbewohners
    room_mate = st.text_input("Please enter the name of a roommate", key="room_mate_input")
    
    # Button zum Hinzufügen des Mitbewohners
    if st.button("Add a new roommate"):
        if room_mate:  # Überprüfen, ob ein Name eingegeben wurde
            if room_mate not in st.session_state["roommates"]:  # Überprüfen, ob der Name nicht schon vorhanden ist
                st.session_state["roommates"].append(room_mate)  # Speichere den Namen
                st.success(f"Roommate {room_mate} has been added!")
                st.session_state["room_mate_input"] = ""  # Eingabefeld leeren
            else:
                st.warning(f"Roommate {room_mate} is already in the list!")
    if st.button ("Finish"):
        st.write("Congratulation, your settigs are done")
        if st.button("change Flat name"):
            flate_name = st.text_input("Please enter your flat name")
            if st.button("Confirm Flat Name"):
                if flate_name:  # Überprüfen, ob ein Name eingegeben wurde
                    st.session_state["flate_name"] = flate_name  # Speichere den Namen
        if st.button("Add a new roommate"):
            room_mate = st.text_input("Please enter the name of a roommate", key="room_mate_input")
            if st.button("Add new roommate"):
                if room_mate:  # Überprüfen, ob ein Name eingegeben wurde
                    if room_mate not in st.session_state["roommates"]:  # Überprüfen, ob der Name nicht schon vorhanden ist
                        st.session_state["roommates"].append(room_mate)  # Speichere den Namen
                        st.success(f"Roommate {room_mate} has been added!")
                        st.session_state["room_mate_input"] = ""  # Eingabefeld leeren
                    else:
                        st.warning(f"Roommate {room_mate} is already in the list!")


        


    # Zeige die Liste der Mitbewohner an
    if st.session_state["roommates"]:
        st.write("Current roommates:")
        for mate in st.session_state["roommates"]:
            st.write(f"- {mate}")

