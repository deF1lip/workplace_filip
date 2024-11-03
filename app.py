import streamlit as st

# Function to save the shared flat name
def name_sharedflat():
    if "SF_name" not in st.session_state:
        st.session_state["SF_name"] = None

    if st.session_state["SF_name"] is None:
        st.session_state["SF_name"] = st.text_input("Enter the name of your shared flat:", key="wg_input")
        if st.session_state["SF_name"]:
            st.success(f"Shared flat '{st.session_state['SF_name']}' has been saved.")

# App layout
if st.session_state.get("SF_name"):
    st.title(f"Waistless - {st.session_state['SF_name']}")
else:
    st.title("Waistless")

# Initial input of the shared flat name
name_sharedflat()

# Main content of the app
if st.session_state["SF_name"]:
    st.write(f"Welcome to the Waistless app for the shared flat '{st.session_state['SF_name']}'!")
else:
    st.warning("Please enter a shared flat name to continue.")
