import streamlit as st

# Initialisierung der Session-State-Variablen
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""
if "roommates" not in st.session_state:
    st.session_state["roommates"] = []
if "setup_finished" not in st.session_state:
    st.session_state["setup_finished"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "settings"

# Funktion zum Wechseln der Seiten
def change_page(new_page):
    st.session_state["page"] = new_page

# Sidebar-Navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.selectbox("Seite auswählen:", ["Übersicht", "Kühlschrank", "Rezepte", "Einstellungen"])
if page_selection != st.session_state["page"]:
    change_page(page_selection)

# Funktionen für die einzelnen Seiten
def overview_page():
    st.title("Übersicht")
    st.write("Willkommen auf der Startseite deiner App.")
    st.write("Hier kannst du allgemeine Informationen anzeigen.")

def fridge_page():
    st.title("Kühlschrank")
    st.write("Dies ist der Inhalt der Kühlschrank-Seite.")
    st.text_input("Gib deinen Namen ein:", key="name_input_fridge")
    st.button("Bestätigen")

def recipes_page():
    st.title("Rezepte")
    st.write("Dies ist der Inhalt der Rezepte-Seite.")
    st.slider("Wähle einen Wert:", 0, 100, 50, key="slider_recipes")

def setup_flat_name():
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Bitte gib den Namen deiner WG ein")
    if st.button("WG-Name bestätigen"):
        if flate_name:
            st.session_state["flate_name"] = flate_name
            st.success(f"Du hast den WG-Namen erfolgreich auf '{flate_name}' gesetzt.")
        else:
            st.warning("Bitte gib einen WG-Namen ein.")

def setup_roommates():
    st.title(f"Willkommen in der WG '{st.session_state['flate_name']}'!")
    room_mate = st.text_input("Bitte gib den Namen eines Mitbewohners ein", key="room_mate_input")
    if st.button("Neuen Mitbewohner hinzufügen"):
        add_roommate(room_mate)
    display_roommates()
    if st.button("Setup abschließen"):
        st.session_state["setup_finished"] = True

def add_roommate(room_mate):
    if room_mate and room_mate not in st.session_state["roommates"]:
        st.session_state["roommates"].append(room_mate)
        st.success(f"Mitbewohner '{room_mate}' wurde hinzugefügt.")
    elif room_mate in st.session_state["roommates"]:
        st.warning(f"Mitbewohner '{room_mate}' ist bereits in der Liste.")

def display_roommates():
    if st.session_state["roommates"]:
        st.write("Aktuelle Mitbewohner:")
        for mate in st.session_state["roommates"]:
            st.write(f"- {mate}")

def settings_page():
    st.write("Herzlichen Glückwunsch, deine Einstellungen sind abgeschlossen.")
    change_flat_name()
    manage_roommates()

def change_flat_name():
    with st.expander("WG-Name ändern"):
        flate_name = st.text_input("Bitte gib einen neuen WG-Namen ein")
        if st.button("WG-Name ändern"):
            if flate_name:
                st.session_state["flate_name"] = flate_name
                st.success(f"Du hast den WG-Namen erfolgreich auf '{flate_name}' geändert.")
            else:
                st.warning("Bitte gib einen neuen WG-Namen ein.")

def manage_roommates():
    with st.expander("Mitbewohner verwalten"):
        room_mate = st.text_input("Bitte gib den Namen eines Mitbewohners ein", key="new_room_mate_input")
        if st.button("Neuen Mitbewohner hinzufügen"):
            add_roommate(room_mate)
        display_roommates()
        remove_roommate()

def remove_roommate():
    if st.session_state["roommates"]:
        roommate_to_remove = st.selectbox("Wähle einen Mitbewohner zum Entfernen aus", st.session_state["roommates"])
        if st.button("Mitbewohner entfernen"):
            if roommate_to_remove in st.session_state["roommates"]:
                st.session_state["roommates"].remove(roommate_to_remove)
                st.success(f"Mitbewohner '{roommate_to_remove}' wurde entfernt.")

# Anzeigelogik für die ausgewählte Seite
if st.session_state["page"] == "Übersicht":
    overview_page()
elif st.session_state["page"] == "Kühlschrank":
    fridge_page()
elif st.session_state["page"] == "Rezepte":
    recipes_page()
elif st.session_state["page"] == "Einstellungen":
    if not st.session_state["setup_finished"]:
        if st.session_state["flate_name"] == "":
            setup_flat_name()
        else:
            setup_roommates()
    else:
        settings_page()
