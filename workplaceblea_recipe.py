import streamlit as st

# intiatlisierung 
if "inventory" not in st.session_state:
    st.session_state["inventory"] = {"Tomato", "Banana,"} # Example roommates list
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Example roommates list

# Variabel für ausgewählter Mitbewohner
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None

# Auswahl des aktuellen Mitbewohner
def select_user():
    st.sidebar.title("Who are you")
    if st.session_state["roommates"]:
        selected_user = st.sidebar.selectbox("Choose your name:", st.session_state["roommates"])
        st.session_state["selected_user"] = selected_user
        st.sidebar.write(f"Hi, {selected_user}!")
    else:
        st.sidebar.warning("No user was added.")