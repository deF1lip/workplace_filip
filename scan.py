import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Initialization of session state variables
if "roommates" not in st.session_state:
    st.session_state["roommates"] = ["Livio", "Flurin", "Anderin"]  # Example roommates list

# Upload-Widget für die Rechnung
uploaded_file = st.file_uploader("Upload an image of your receipt", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Lade das Bild mit PIL
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Receipt', use_column_width=True)
    
    # Konvertiere das Bild in ein OpenCV-kompatibles Format (von PIL zu numpy)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # OCR (Texterkennung) auf dem Bild anwenden
    result = pytesseract.image_to_string(image)
    st.write("Extracted Text:")
    st.write(result)
#jsdf