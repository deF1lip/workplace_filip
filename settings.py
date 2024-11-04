import streamlit as st

# Initialisiere flate_name in st.session_state
if "flate_name" not in st.session_state:
    st.session_state["flate_name"] = ""



# App neu auflegen
if st.session_state["flate_name"] == "":
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Please enter your flat name")
    if st.button("Confirm"):
        st.session_state.flate_name =flate_name
        st.text_input (f"welcome to your new flat {flate_name}. Please enter your name", key= "room_mate")
        st.button ("Add a new roommate")
        st.experimental_rerun()
        
else:
    st.write ("livio best")

        

