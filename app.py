"""
Main landing page - Unified Login for AI Marketing Test Platform
"""

import streamlit as st
from modules.ui_components import load_custom_css, custom_card
from modules.auth import AuthManager
from modules.sheets_manager import SheetsManager

# Page configuration
st.set_page_config(
    page_title="AI Marketing Test Platform",
    page_icon="📝",
    layout="centered"
)

# Load custom CSS
load_custom_css()

# Hide navigation based on user type
from modules.ui_components import hide_navigation_for_user
hide_navigation_for_user()

auth = AuthManager()
sheets_manager = SheetsManager()

# Check if already logged in
if auth.is_authenticated():
    user_type = st.session_state.user_type
    if user_type == "student":
        st.success(f"Zalogowano jako: {st.session_state.first_name} {st.session_state.last_name}")
        if st.button("Rozpocznij Test", use_container_width=True):
            st.switch_page("pages/2_Test_Studenta.py")
    else:
        st.success(f"Zalogowano jako nauczyciel: {st.session_state.email}")
        if st.button("Przejdź do Dashboard", use_container_width=True):
            st.switch_page("pages/5_Dashboard_Nauczyciela.py")
    st.stop()

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

st.markdown("### Logowanie")

# Step 1: Ask for email
if 'login_email' not in st.session_state:
    st.session_state.login_email = ""

email = st.text_input(
    "Email *",
    value=st.session_state.login_email,
    placeholder="twoj-email@example.com",
    help="Wprowadź swój adres email",
    key="email_input"
)

if email and email != st.session_state.login_email:
    st.session_state.login_email = email
    st.rerun()

# Step 2: Check if teacher and show appropriate form
if email:
    # Check if this email is a teacher
    is_teacher = False
    try:
        teachers_df = sheets_manager.workbook.worksheet("Teachers").get_all_records()
        teacher_emails = [t['Email'].lower() for t in teachers_df if t.get('Email')]
        is_teacher = email.lower() in teacher_emails
    except:
        is_teacher = False

    if is_teacher:
        # Teacher login form
        st.info("👨‍🏫 Wykryto konto nauczyciela")

        with st.form("teacher_login_form"):
            password = st.text_input(
                "Hasło *",
                type="password",
                placeholder="••••••••"
            )

            submitted = st.form_submit_button("Zaloguj się jako nauczyciel", use_container_width=True)

            if submitted:
                if not password:
                    st.error("Proszę podać hasło")
                else:
                    success, message = auth.teacher_login(email, password)
                    if success:
                        st.session_state.login_email = ""
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        # Student login form
        st.info("👨‍🎓 Logowanie jako student")

        with st.form("student_login_form"):
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

            submitted = st.form_submit_button("Zaloguj się jako student", use_container_width=True)

            if submitted:
                if not first_name or not last_name:
                    st.error("Proszę podać imię i nazwisko")
                else:
                    success, message = auth.student_login(email, first_name, last_name, student_id)
                    if success:
                        st.session_state.login_email = ""
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

# Footer
st.markdown("---")
st.markdown("© 2026 AI NETWORK (ARTECH CONSULT)")
