import streamlit as st

# Titel der App
st.title("♻️ Wasteless App - Setup")

# Eingabefeld für den Flat-Namen
flat_name = st.text_input("Enter your flat name:")

# Button zur Bestätigung des Flat-Namens
if st.button("Approve Flat Name"):
    if flat_name:
        st.success(f"Flat name '{flat_name}' has been set!")
    else:
        st.warning("Please enter a flat name.")
