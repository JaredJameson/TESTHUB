"""
Main landing page for AI Marketing Test Platform
"""

import streamlit as st
from modules.ui_components import load_custom_css, custom_card

# Page configuration
st.set_page_config(
    page_title="AI Marketing Test Platform",
    page_icon="📝",
    layout="centered"
)

# Load custom CSS
load_custom_css()

# Header
st.markdown("# AI NETWORK Test Platform")
st.markdown("## Test Zaliczeniowy - AI w Marketingu")

st.markdown("---")

# Test information
custom_card(
    "Informacje o teście",
    """
    <ul>
        <li><strong>Liczba pytań:</strong> 27</li>
        <li><strong>Czas trwania:</strong> 30 minut</li>
        <li><strong>Próg zaliczenia:</strong> 48% (13 poprawnych odpowiedzi)</li>
        <li><strong>Format:</strong> Pytania jednokrotnego wyboru</li>
    </ul>
    """
)

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Jestem Studentem", use_container_width=True):
        st.switch_page("pages/1_Student_Login.py")

with col2:
    if st.button("Jestem Nauczycielem", use_container_width=True):
        st.switch_page("pages/4_Teacher_Login.py")

# Footer
st.markdown("---")
st.markdown("© 2026 AI NETWORK (ARTECH CONSULT)")
