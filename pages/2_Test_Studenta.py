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
    # Compact, professional test instructions card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #FFFFFF 0%, #FFFBF0 100%);
         border: 1px solid #E0E0E0; border-left: 6px solid #FFD700;
         border-radius: 12px; padding: 40px; margin: 40px 0 32px 0;
         box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">
        <h1 style="margin: 0 0 8px 0; color: #000000; font-size: 32px;">Test Zaliczeniowy</h1>
        <h2 style="margin: 0 0 32px 0; color: #666; font-size: 20px; font-weight: 400;">AI w Marketingu</h2>

        <div style="background: #FFF8E1; border-radius: 8px; padding: 24px; margin-bottom: 24px;">
            <h3 style="margin: 0 0 16px 0; color: #000000; font-size: 18px;">📋 Informacje o teście</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; color: #333;">
                <div><strong>⏱️ Czas trwania:</strong> 30 minut</div>
                <div><strong>📝 Liczba pytań:</strong> 27</div>
                <div><strong>✅ Próg zaliczenia:</strong> 48% (13/27)</div>
                <div><strong>💾 Auto-zapis:</strong> Co 5 pytań</div>
            </div>
        </div>

        <div style="background: #FFF3E0; border-left: 4px solid #FF9800; border-radius: 8px; padding: 16px; margin-bottom: 32px;">
            <strong style="color: #E65100;">⚠️ Uwaga:</strong>
            <span style="color: #333;"> Timer uruchomi się automatycznie. Test zostanie wysłany po 30 minutach.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("🚀 Rozpocznij Test", use_container_width=True, type="primary"):
            if test_engine.initialize_test(randomize=False):
                st.success("Test zainicjalizowany pomyślnie!")
                st.rerun()
            else:
                st.error("Błąd inicjalizacji testu. Spróbuj ponownie.")

    with col2:
        if st.button("← Wyloguj się", use_container_width=True):
            auth.logout()
            st.switch_page("pages/1_Logowanie_Studenta.py")

    st.stop()

# Check if test already completed
if st.session_state.get('test_completed', False):
    st.success("Test został już ukończony!")
    if st.button("Zobacz Wyniki"):
        st.switch_page("pages/3_Wyniki_Studenta.py")
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
    st.switch_page("pages/3_Wyniki_Studenta.py")
    st.stop()

# Main test interface
current_q_index = st.session_state.get('current_question', 0)
total_questions = test_engine.get_total_questions()

# Get current question first
question = test_engine.get_question(current_q_index)

if not question:
    st.error("Błąd wczytywania pytania")
    st.stop()

# Fixed timer in top right corner
time_remaining = test_engine.get_time_remaining()
time_str = test_engine.format_time(time_remaining)
timer_color = "#8B0000" if time_remaining < 300 else "#2D5016"

st.markdown(f"""
<div style="position: fixed; top: 80px; right: 20px; z-index: 999;
     background: white; padding: 12px 20px; border-radius: 8px;
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border: 2px solid {timer_color};">
    <div style="font-size: 14px; color: #666; margin-bottom: 4px;">Pozostały czas:</div>
    <div style="font-size: 24px; font-weight: 700; color: {timer_color};">{time_str}</div>
</div>
""", unsafe_allow_html=True)

# Progress bar - compact
progress_pct = test_engine.get_progress_percentage()
answered = test_engine.get_answered_count()

st.markdown(f"""
<div style="margin: 20px 0;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="font-weight: 600;">Pytanie {current_q_index + 1} z {total_questions}</span>
        <span style="color: #666;">{answered}/{total_questions} odpowiedzi | {progress_pct}%</span>
    </div>
    <div style="background: #E0E0E0; border-radius: 10px; height: 8px; overflow: hidden;">
        <div style="background: linear-gradient(90deg, #2D5016 0%, #4CAF50 100%);
             width: {progress_pct}%; height: 100%; transition: width 0.3s ease;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Unified question card with question + answers in ONE card
current_answer = test_engine.get_answer(question['id'])

options_text = {
    'a': question['options']['a'],
    'b': question['options']['b'],
    'c': question['options']['c'],
    'd': question['options']['d']
}

st.markdown(f"""
<div style="background: linear-gradient(135deg, #FFFFFF 0%, #FFFBF0 100%);
     border: 1px solid #E0E0E0; border-left: 6px solid #FFD700;
     border-radius: 12px; padding: 32px; margin: 24px 0;
     box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">
    <div style="background: #FFF8E1; padding: 8px 16px; border-radius: 6px;
         display: inline-block; margin-bottom: 20px; font-size: 13px;
         font-weight: 600; color: #666;">
        {question['category']}
    </div>
    <h3 style="margin: 0 0 24px 0; color: #000000; font-size: 20px; line-height: 1.5;">
        {question['question']}
    </h3>
</div>
""", unsafe_allow_html=True)

# Radio buttons without label - cleaner look
selected = st.radio(
    "",
    options=['a', 'b', 'c', 'd'],
    format_func=lambda x: f"{x}) {options_text[x]}",
    index=['a', 'b', 'c', 'd'].index(current_answer) if current_answer else None,
    key=f"q_{question['id']}"
)

# Save answer when changed - use toast instead of info to avoid button duplication
if selected and selected != current_answer:
    test_engine.save_answer(question['id'], selected)

    # Check for auto-save - use toast instead of st.info()
    if test_engine.should_auto_save():
        answered_count = test_engine.get_answered_count()
        st.toast(f"💾 Auto-zapis: Zapisano postęp ({answered_count} pytań)", icon="✅")
        test_engine.mark_auto_saved(answered_count)

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
        st.switch_page("pages/1_Logowanie_Studenta.py")

with col3:
    if current_q_index < total_questions - 1:
        if st.button("Następne →", use_container_width=True):
            st.session_state.current_question = current_q_index + 1
            st.rerun()
    else:
        # Last question - show submit button
        # Check if we need confirmation
        if 'show_submit_confirmation' not in st.session_state:
            st.session_state.show_submit_confirmation = False

        if not st.session_state.show_submit_confirmation:
            if st.button("Zakończ Test", use_container_width=True, type="primary"):
                # Check if all questions answered
                if test_engine.get_answered_count() < total_questions:
                    st.session_state.show_submit_confirmation = True
                    st.rerun()
                else:
                    st.session_state.test_completed = True
                    st.rerun()

# Show confirmation dialog if needed (outside columns to avoid duplication)
if st.session_state.get('show_submit_confirmation', False):
    st.markdown("""
    <div style="background: #FFF3E0; border-left: 4px solid #FF9800; border-radius: 8px;
         padding: 20px; margin: 24px 0;">
        <strong style="color: #E65100;">⚠️ Potwierdzenie:</strong>
        <span style="color: #333;"> Odpowiedziałeś na {}/{} pytań. Czy na pewno chcesz zakończyć test?</span>
    </div>
    """.format(test_engine.get_answered_count(), total_questions), unsafe_allow_html=True)

    col_confirm1, col_confirm2 = st.columns(2)
    with col_confirm1:
        if st.button("✅ Tak, zakończ test", use_container_width=True, type="primary"):
            st.session_state.test_completed = True
            st.session_state.show_submit_confirmation = False
            st.rerun()
    with col_confirm2:
        if st.button("❌ Anuluj", use_container_width=True):
            st.session_state.show_submit_confirmation = False
            st.rerun()

# Auto-refresh every second for timer
time.sleep(1)
st.rerun()
