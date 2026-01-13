"""
Teacher login page
"""

import streamlit as st
from modules.ui_components import load_custom_css
from modules.auth import AuthManager

# Page config
st.set_page_config(
    page_title="Logowanie - Nauczyciel",
    page_icon="👨‍🏫",
    layout="centered"
)

load_custom_css()
auth = AuthManager()

# Header
st.markdown("# Logowanie - Nauczyciel")
st.markdown("## Dashboard Administracyjny")
st.markdown("---")

# Check if already logged in
if auth.is_authenticated() and st.session_state.user_type == "teacher":
    st.success(f"Zalogowano jako: {st.session_state.email}")
    if st.button("Przejdź do Dashboard"):
        st.switch_page("pages/5_Dashboard_Nauczyciela.py")
    st.stop()

# Login form
with st.form("teacher_login_form"):
    st.markdown("### Dane logowania")

    email = st.text_input(
        "Email *",
        placeholder="tina@example.com"
    )

    password = st.text_input(
        "Hasło *",
        type="password",
        placeholder="••••••••"
    )

    submitted = st.form_submit_button("Zaloguj się", use_container_width=True)

    if submitted:
        success, message = auth.teacher_login(email, password)

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

# Rate limit warning
if 'login_attempts' in st.session_state and st.session_state.login_attempts > 0:
    attempts_left = 3 - st.session_state.login_attempts
    if attempts_left > 0:
        st.warning(f"Pozostałe próby logowania: {attempts_left}/3")

# Back button
if st.button("← Powrót"):
    st.switch_page("app.py")
