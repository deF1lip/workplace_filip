import streamlit as st

# Function to save the shared flat name
def name_sharedflat():
    if "SF_name" not in st.session_state:
        st.session_state["SF_name"] = None

    if st.session_state["SF_name"] is None:
        st.session_state["SF_name"] = st.text_input("Enter the name of your shared flat:", key="wg_input")
        if st.session_state["SF_name"]:
            st.success(f"Shared flat '{st.session_state['SF_name']}' has been saved.")

# Function to add flatmates
def add_flatmates():
    if "flatmates" not in st.session_state:
        st.session_state["flatmates"] = []

    with st.form(key='flatmate_form'):
        new_flatmate = st.text_input("Enter the name of a flatmate:", key="flatmate_input")
        submit_button = st.form_submit_button(label="Add Flatmate")

        if submit_button and new_flatmate:
            st.session_state["flatmates"].append(new_flatmate)
            st.success(f"Flatmate '{new_flatmate}' has been added.")

# App layout
if st.session_state.get("SF_name"):
    st.title(f"Waistless - {st.session_state['SF_name']}")
else:
    st.title("Waistless")

# Initial input of the shared flat name
name_sharedflat()

# Display input for flatmates after the shared flat name is set
if st.session_state["SF_name"]:
    st.subheader("Add your flatmates")
    add_flatmates()
    if st.session_state["flatmates"]:
        st.write("Current flatmates:")
        for i, flatmate in enumerate(st.session_state["flatmates"], start=1):
            st.write(f"{i}. {flatmate}")
else:
    st.warning("Please enter a shared flat name to continue.")
