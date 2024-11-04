import streamlit as st


# open first the setting page to define flate-name and inhabitants
if "pages" not in st.session_state:
    st.session_state ["page"] = "settings"

# Function to change between the pages
def change_page(new_page):
    st.session_state["page"] = new_page


# sidebar; titel
st.sidebar.title("Navigation")

# sidebar: change de side by unsing the buttons
page_selection = st.sidebar.selectbox("Overview:", ["overview", "Livio", "Flurin"])
if page_selection != st.session_state["page"]:
    st.session_state["page"] = page_selection
if st.sidebar.button("Fridge"):
    change_page("fridge")
if st.sidebar.button("Recipes"):
    change_page("recipes")
if st.sidebar.button("Settings"):
    change_page("settings")

# Anzeigelogik für jede Seite
if st.session_state["page"] == "overview":
    st.title("overview")
    st.write('Willkommen auf der Startseite deiner App.')
    st.write('Hier kannst du allgemeine Informationen anzeigen.')
elif st.session_state["page"] == "fridge":
    st.title("fridge")
    st.write('Dies ist der Inhalt von Seite 1.')
    st.text_input('Gib deinen Namen ein:', key='name_input_page1')
    st.button('Bestätigen')
elif st.session_state["page"] == "recipes":
    st.title("recipes")
    st.write('Dies ist der Inhalt von Seite 2.')
    st.slider('Wähle einen Wert:', 0, 100, 50, key='slider_page2')
elif st.session_state["page"] == "settings":
    # Initialisiere Variablen in st.session_state
    if "flate_name" not in st.session_state:
        st.session_state["flate_name"] = ""

    if "roommates" not in st.session_state:
        st.session_state["roommates"] = []

    if "room_mate_input" not in st.session_state:
        st.session_state["room_mate_input"] = ""

    if "setup_finished" not in st.session_state:
        st.session_state["setup_finished"] = False

    # Setup-Seite anzeigen, wenn der flat name noch nicht festgelegt ist
    if not st.session_state["setup_finished"] and st.session_state["flate_name"] == "":
        st.title("🏠 Wasteless App - Setup")
        flate_name = st.text_input("Please enter your flat name")
    
        if st.button("Confirm Flat Name"):
            if flate_name:  # Überprüfen, ob ein Name eingegeben wurde
                st.session_state["flate_name"] = flate_name  # Speichere den Namen

    # Hauptseite anzeigen, wenn der flat name festgelegt wurde und das Setup noch nicht abgeschlossen ist
    if not st.session_state["setup_finished"] and st.session_state["flate_name"]:
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

        # Zeige die Liste der Mitbewohner an
        if st.session_state["roommates"]:
            st.write("Current roommates:")
            for mate in st.session_state["roommates"]:
                st.write(f"- {mate}")

        # Button "Finish" zum Abschluss der Einstellungen
        if st.button("Finish"):
            st.session_state["setup_finished"] = True  # Setzt den Zustand, dass das Setup abgeschlossen ist

    # Nachricht anzeigen, wenn das Setup abgeschlossen ist
    if st.session_state["setup_finished"]:
        st.write("Congratulations, your settings are done.")
        with st.expander("Flat name"):
                flate_name = st.text_input("Please enter your flat name")
                if st.button("Change Flat Name"):
                    if flate_name:  # Überprüfen, ob ein Name eingegeben wurde
                        st.session_state["flate_name"] = flate_name  # Speichere den Namen
        with st.expander("Room mates"):
            room_mate = st.text_input("Please enter the name of a roommate", key="room_mate_input")
            if st.button("Add new roommate"):
                if room_mate:  # Überprüfen, ob ein Name eingegeben wurde
                    if room_mate not in st.session_state["roommates"]:  # Überprüfen, ob der Name nicht schon vorhanden ist
                        st.session_state["roommates"].append(room_mate)  # Speichere den Namen
                        st.success(f"Roommate {room_mate} has been added!")
                        st.session_state["room_mate_input"] = ""  # Eingabefeld leeren
                    else:
                        st.warning(f"Roommate {room_mate} is already in the list!")
            if st.session_state["roommates"]:
                st.write("Current roommates:")
                for mate in st.session_state["roommates"]:
                    st.write(f"- {mate}")

            roommate_to_remove = st.selectbox("Select a roommate to remove", st.session_state["roommates"])
            if st.button("Remove roommate"):
                if roommate_to_remove in st.session_state["roommates"]:
                    st.session_state["roommates"].remove(roommate_to_remove)
                    st.success(f"Roommate {roommate_to_remove} has been removed!")
elif st.session_state["page"] == "Livio":
    st.title("Livio")
    st.write('Dies ist der Inhalt von Seite 1.')
    st.text_input('Gib deinen Namen ein:', key='name_input_page1')
    st.button('Bestätigen')


