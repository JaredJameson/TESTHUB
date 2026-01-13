"""
Teacher login page - Redirects to unified login
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Logowanie - Nauczyciel",
    page_icon="👨‍🏫",
    layout="centered"
)

# Redirect to main page with unified login
st.info("Przekierowanie do strony logowania...")
st.switch_page("app.py")
