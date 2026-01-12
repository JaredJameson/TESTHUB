"""
Student Test Page - Main Test Interface
"""

import streamlit as st
import time
from modules.ui_components import load_custom_css, progress_bar, section_divider
from modules.auth import AuthManager
from modules.test_engine import TestEngine
from modules.sheets_manager import SheetsManager
from modules.email_service import EmailService

# Page config
st.set_page_config(
    page_title="Test - AI Marketing",
    page_icon="📝",
    layout="centered"
)

load_custom_css()
auth = AuthManager()
test_engine = TestEngine()
email_service = EmailService()

# Require student authentication
auth.require_authentication(user_type="student")

# Initialize test if not started
if 'test_questions' not in st.session_state:
    st.markdown("# Test Zaliczeniowy")
    st.markdown("## AI w Marketingu")
    section_divider()

    st.markdown("### Instrukcje")
    st.markdown("""
    - **Czas trwania:** 30 minut
    - **Liczba pytań:** 27
    - **Próg zaliczenia:** 48% (13 poprawnych odpowiedzi)
    - **Auto-zapis:** Co 5 pytań
    - **Format:** Pytania jednokrotnego wyboru
    """)

    st.warning("⚠️ Po rozpoczęciu testu timer będzie odliczał czas. Test zostanie automatycznie wysłany po upływie 30 minut.")

    if st.button("Rozpocznij Test", use_container_width=True):
        if test_engine.initialize_test(randomize=False):
            st.success("Test zainicjalizowany pomyślnie!")
            st.rerun()
        else:
            st.error("Błąd inicjalizacji testu. Spróbuj ponownie.")

    if st.button("← Wyloguj się"):
        auth.logout()
        st.switch_page("pages/1_Student_Login.py")

    st.stop()

# Check if test already completed
if st.session_state.get('test_completed', False):
    st.success("Test został już ukończony!")
    if st.button("Zobacz Wyniki"):
        st.switch_page("pages/3_Student_Results.py")
    st.stop()

# Check for timeout
if test_engine.is_time_up() and not st.session_state.get('test_completed', False):
    st.warning("⏰ Czas na test się skończył! Wysyłanie wyników...")
    st.session_state.auto_submitted = True
    st.session_state.test_completed = True

    # Calculate and save results
    results = test_engine.calculate_results()
    student_data = {
        'email': st.session_state.email,
        'first_name': st.session_state.first_name,
        'last_name': st.session_state.last_name,
        'student_id': st.session_state.get('student_id', '')
    }

    formatted_results = test_engine.format_results_for_sheets(student_data, results)
    st.session_state.test_results = results

    # Save to Google Sheets
    sheets = SheetsManager()
    if sheets.save_test_result(formatted_results):
        st.success("Wyniki zostały zapisane!")

        # Send email notifications
        student_full_name = f"{st.session_state.first_name} {st.session_state.last_name}"

        # Send to student
        email_service.send_student_result_email(
            student_email=st.session_state.email,
            student_name=student_full_name,
            results=results,
            async_send=True
        )

        # Send to teacher
        email_service.send_teacher_notification_email(
            student_name=student_full_name,
            student_email=st.session_state.email,
            results=results,
            async_send=True
        )
    else:
        st.error("Błąd zapisu wyników. Skontaktuj się z nauczycielem.")

    time.sleep(2)
    st.switch_page("pages/3_Student_Results.py")
    st.stop()

# Main test interface
current_q_index = st.session_state.get('current_question', 0)
total_questions = test_engine.get_total_questions()

# Header with timer
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(f"# Pytanie {current_q_index + 1}/{total_questions}")

with col2:
    answered = test_engine.get_answered_count()
    st.markdown(f"**Odpowiedzi:** {answered}/{total_questions}")

with col3:
    time_remaining = test_engine.get_time_remaining()
    time_str = test_engine.format_time(time_remaining)

    # Color code timer
    if time_remaining < 300:  # Last 5 minutes
        st.markdown(f"<h3 style='color: #8B0000;'>⏰ {time_str}</h3>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3>⏰ {time_str}</h3>", unsafe_allow_html=True)

# Progress bar
progress_pct = test_engine.get_progress_percentage()
st.progress(progress_pct / 100)
st.markdown(f"<p style='text-align: center; font-weight: 600;'>Postęp: {progress_pct}%</p>", unsafe_allow_html=True)

section_divider()

# Get current question
question = test_engine.get_question(current_q_index)

if not question:
    st.error("Błąd wczytywania pytania")
    st.stop()

# Display question
st.markdown(f"### {question['question']}")
st.markdown(f"**Kategoria:** {question['category']}")

st.markdown("---")

# Display options as radio buttons
current_answer = test_engine.get_answer(question['id'])

options_text = {
    'a': question['options']['a'],
    'b': question['options']['b'],
    'c': question['options']['c'],
    'd': question['options']['d']
}

selected = st.radio(
    "Wybierz odpowiedź:",
    options=['a', 'b', 'c', 'd'],
    format_func=lambda x: f"{x}) {options_text[x]}",
    index=['a', 'b', 'c', 'd'].index(current_answer) if current_answer else None,
    key=f"q_{question['id']}"
)

# Save answer when changed
if selected and selected != current_answer:
    test_engine.save_answer(question['id'], selected)

    # Check for auto-save
    if test_engine.should_auto_save():
        answered_count = test_engine.get_answered_count()
        st.info(f"💾 Auto-zapis: Zapisano postęp ({answered_count} pytań)")
        test_engine.mark_auto_saved(answered_count)
        time.sleep(1)

section_divider()

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if current_q_index > 0:
        if st.button("← Poprzednie", use_container_width=True):
            st.session_state.current_question = current_q_index - 1
            st.rerun()

with col2:
    if st.button("Wyloguj się"):
        auth.logout()
        st.switch_page("pages/1_Student_Login.py")

with col3:
    if current_q_index < total_questions - 1:
        if st.button("Następne →", use_container_width=True):
            st.session_state.current_question = current_q_index + 1
            st.rerun()
    else:
        # Last question - show submit button
        if st.button("Zakończ Test", use_container_width=True, type="primary"):
            # Check if all questions answered
            if test_engine.get_answered_count() < total_questions:
                st.warning(f"⚠️ Odpowiedziałeś na {test_engine.get_answered_count()}/{total_questions} pytań. Czy na pewno chcesz zakończyć test?")

                if st.button("Tak, zakończ test"):
                    st.session_state.test_completed = True
                    st.rerun()
            else:
                st.session_state.test_completed = True
                st.rerun()

# Auto-refresh every second for timer
time.sleep(1)
st.rerun()
