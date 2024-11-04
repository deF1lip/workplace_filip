import streamlit as st

# Initialisiere flate_name in st.session_state
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""

# definiere für Liste
if "roommates" not in st.session_state:
    st.session_state["roommates"] = []


# first Settings einstellen
if st.session_state["flate_name"] == "":
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Please enter your flat name")
    if st.button("Confirm"):
        st.session_state.flate_name =flate_name

# add first name 
if st.session_state["flate_name"]:
    st.title(f"Welcome to {st.session_state['flate_name']}!")
    room_mate = st.text_input("Please enter your name", key="room_mate")
    if st.button("Confirm"):
         if st.button("Add a new roommate"):
              st.text_input ("Please enter the name of youre roommate")
              st.session_state["roommates"].append(room_mate)




        

