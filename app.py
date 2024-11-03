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

# Eingabefeld für das Hinzufügen eines Mitbewohners
new_flatmate = st.text_input("Enter flatmate name:", key=f"flatmate_{len(st.session_state.flatmates)}")
if st.button("Add Flatmate"):
    if new_flatmate and new_flatmate not in st.session_state.flatmates:
        st.session_state.flatmates.append(new_flatmate)
        st.success(f"{new_flatmate} added!")

# Anzeige der aktuellen Mitbewohner
if st.session_state.flatmates:
    st.write("### Current flatmates:")
    for index, mate in enumerate(st.session_state.flatmates, start=1):
        st.write(f"{index}. {mate}")
