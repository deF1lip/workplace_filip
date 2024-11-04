import streamlit as st

# Initialisiere flate_name in st.session_state
st.session_state["flate_name"] = ""



# App neu auflegen
if st.session_state["flate_name"] == "":
    st.title("🏠 Wasteless App - Setup")
    flate_name = st.text_input("Please enter your flat name")
    st.session_state.flate_name =flate_name
    if st.button("Confirm"):
        st.text_input (f"welcome to your new flat {flate_name}. Please enter your name", key=room_mate)
        st.button ("Add a new roommate")
else:
    st.write ("livio best")

        

