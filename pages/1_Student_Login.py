"""
Student login page
"""

import streamlit as st
from modules.ui_components import load_custom_css
from modules.auth import AuthManager

# Page config
st.set_page_config(
    page_title="Logowanie - Student",
    page_icon="📝",
    layout="centered"
)

load_custom_css()
auth = AuthManager()

# Header
st.markdown("# Logowanie - Student")
st.markdown("## Test Zaliczeniowy - AI w Marketingu")
st.markdown("---")

# Check if already logged in
if auth.is_authenticated() and st.session_state.user_type == "student":
    st.success(f"Zalogowano jako: {st.session_state.first_name} {st.session_state.last_name}")
    if st.button("Rozpocznij Test"):
        st.switch_page("pages/2_Student_Test.py")
    st.stop()

# Login form
with st.form("student_login_form"):
    st.markdown("### Dane studenta")

    email = st.text_input(
        "Email *",
        placeholder="jan.kowalski@example.com",
        help="Adres email, na który otrzymasz wyniki"
    )

    first_name = st.text_input(
        "Imię *",
        placeholder="Jan"
    )

    last_name = st.text_input(
        "Nazwisko *",
        placeholder="Kowalski"
    )

    student_id = st.text_input(
        "Numer indeksu (opcjonalnie)",
        placeholder="12345"
    )

    submitted = st.form_submit_button("Rozpocznij Test", use_container_width=True)

    if submitted:
        success, message = auth.student_login(email, first_name, last_name, student_id)

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

# Back button
if st.button("← Powrót"):
    st.switch_page("app.py")
