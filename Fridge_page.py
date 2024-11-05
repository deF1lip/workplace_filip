def fridge_page():
    st.title("Fridge")
    st.write("This is the content of the Fridge page.")
    st.text_input("Enter your name:", key="name_input_fridge")
    st.button("Confirm")