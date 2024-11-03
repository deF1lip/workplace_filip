import streamlit as st

# Titel der App
st.title("♻️ Wasteless App - Setup")

# Eingabefeld für den WG-Namen
wg_name = st.text_input("Enter your WG name:")

# Button zur Bestätigung des WG-Namens
if st.button("Approve WG Name"):
    if wg_name:
        st.success(f"WG name '{wg_name}' has been set!")
    else:
        st.warning("Please enter a WG name.")
