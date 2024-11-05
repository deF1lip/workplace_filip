import streamlit as st

# Initialisierung von Session-State-Variablen
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""
if "roommates" not in st.session_state:
    st.session_state["roommates"] = []
if "room_mate_input" not in st.session_state:
    st.session_state["room_mate_input"] = ""
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "settings"  # Startseite bei erstmaligem Laden

# Funktion zur Seiten-Navigation
def change_page(new_page):
    st.session_state["page"] = new_page

# Setup-Seite für die Eingabe des WG-Namens
def setup_flat_name():
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Please enter your flat name")
    if st.button("Confirm Flat Name"): 
        if flate_name:
            st.session_state["flate_name"] = flate_name
            st.success(f"You successfully saved your flat name: {flate_name}")
        else:
            st.warning("Please enter a flat name")

# Hauptseite zur Eingabe der Mitbewohner
def setup_roommates():
    st.title(f"Welcome to {st.session_state['flate_name']}!")
    room_mate = st.text_input("Please enter the name of a roommate", key="room_mate_input")
    if st.button("Add a new roommate"):
        add_roommate(room_mate)
    display_roommates()
    if st.button("Finish"):
        st.session_state["setup_finished"] = True

# Funktion zum Hinzufügen eines Mitbewohners
def add_roommate(room_mate):
    if room_mate and room_mate not in st.session_state["roommates"]:
        st.session_state["roommates"].append(room_mate)
        st.success(f"Roommate {room_mate} has been added!")
    elif room_mate in st.session_state["roommates"]:
        st.warning(f"Roommate {room_mate} is already in the list!")

# Funktion zur Anzeige der Mitbewohner
def display_roommates():
    if st.session_state["roommates"]:
        st.write("Current roommates:")
        for mate in st.session_state["roommates"]:
            st.write(f"- {mate}")

# Seite für Einstellungen, wenn das Setup abgeschlossen ist
def settings_page():
    st.write("Congratulations, your settings are done.")
    change_flat_name()
    manage_roommates()

# Funktion zum Ändern des WG-Namens
def change_flat_name():
    with st.expander("Flat name"):
        flate_name = st.text_input("Please enter your flat name")
        if st.button("Change Flat Name"):
            if flate_name:
                st.session_state["flate_name"] = flate_name
                st.success(f"You successfully changed your flat name to {flate_name}!")
            else:
                st.warning("Please enter a new flat name")

# Funktion zur Verwaltung der Mitbewohner
def manage_roommates():
    with st.expander("Roommates"):
        room_mate = st.text_input("Please enter the name of a roommate", key="new_room_mate_input")
        if st.button("Add new roommate"):
            add_roommate(room_mate)
        display_roommates()
        remove_roommate()

# Funktion zum Entfernen eines Mitbewohners
def remove_roommate():
    if st.session_state["roommates"]:
        roommate_to_remove = st.selectbox("Select a roommate to remove", st.session_state["roommates"])
        if st.button("Remove roommate"):
            if roommate_to_remove in st.session_state["roommates"]:
                st.session_state["roommates"].remove(roommate_to_remove)
                st.success(f"Roommate {roommate_to_remove} has been removed!")

# Sidebar für die Navigation
st.sidebar.title("Navigation")
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
    st.title("Overview")
    st.write('Willkommen auf der Startseite deiner App.')
    st.write('Hier kannst du allgemeine Informationen anzeigen.')
elif st.session_state["page"] == "fridge":
    st.title("Fridge")
    st.write('Dies ist der Inhalt von Seite 1.')
    st.text_input('Gib deinen Namen ein:', key='name_input_page1')
    st.button('Bestätigen')
elif st.session_state["page"] == "recipes":
    st.title("Recipes")
    st.write('Dies ist der Inhalt von Seite 2.')
    st.slider('Wähle einen Wert:', 0, 100, 50, key='slider_page2')
elif st.session_state["page"] == "settings":
    if not st.session_state["setup_finished"]:
        if st.session_state["flate_name"] == "":
            setup_flat_name()
        else:
            setup_roommates()
    else:
        settings_page()
elif st.session_state["page"] == "Livio":
    st.title("Livio")
    st.write('Dies ist der Inhalt von Seite 1.')
    st.text_input('Gib deinen Namen ein:', key='name_input_page1')
    st.button('Bestätigen')
