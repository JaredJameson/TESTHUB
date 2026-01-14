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
    # Test instructions header
    st.markdown("# Test Zaliczeniowy")
    st.markdown("## AI w Marketingu")

    st.markdown("---")

    # Test information
    st.markdown("### Informacje o teście")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Czas na pytanie:** 20 sekund")
        st.markdown("**Próg zaliczenia:** 48% (13/27)")
    with col2:
        st.markdown("**Liczba pytań:** 27")
        st.markdown("**Auto-zapis:** Co 5 pytań")

    st.markdown("---")

    st.warning("**UWAGA:** Na każde pytanie masz **20 sekund**. Po upływie czasu pytanie zostanie **automatycznie zablokowane** i musisz przejść do następnego.")

    if st.button("Rozpocznij Test", use_container_width=True, type="primary"):
        if test_engine.initialize_test(randomize=False):
            st.success("Test zainicjalizowany pomyślnie!")
            st.rerun()
        else:
            st.error("Błąd inicjalizacji testu. Spróbuj ponownie.")

    if st.button("Wyloguj się", use_container_width=True):
        auth.logout()
        st.switch_page("pages/1_Logowanie_Studenta.py")

    st.stop()

# Check if test already completed
if st.session_state.get('test_completed', False):
    st.success("Test został już ukończony!")
    if st.button("Zobacz Wyniki"):
        st.switch_page("pages/3_Wyniki_Studenta.py")
    st.stop()

# Main test interface
current_q_index = st.session_state.get('current_question', 0)
total_questions = test_engine.get_total_questions()

# Check if current question time is up and lock it
if test_engine.is_question_time_up() and not test_engine.is_question_locked(current_q_index):
    test_engine.lock_current_question()
    st.rerun()

# Get current question first
question = test_engine.get_question(current_q_index)

if not question:
    st.error("Błąd wczytywania pytania")
    st.stop()

# Per-question timer in top right corner
question_time_remaining = test_engine.get_question_time_remaining()
is_locked = test_engine.is_question_locked(current_q_index)

# Color based on time remaining
if is_locked:
    timer_color = "#8B0000"
    timer_text = "ZABLOKOWANE"
elif question_time_remaining <= 5:
    timer_color = "#8B0000"
    timer_text = f"{question_time_remaining}s"
elif question_time_remaining <= 10:
    timer_color = "#FFD700"
    timer_text = f"{question_time_remaining}s"
else:
    timer_color = "#2D5016"
    timer_text = f"{question_time_remaining}s"

st.markdown(f"""
<div style="position: fixed; top: 80px; right: 20px; z-index: 999;
     background: white; padding: 12px 20px; border-radius: 8px;
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border: 2px solid {timer_color};">
    <div style="font-size: 14px; color: #666; margin-bottom: 4px;">Czas na pytanie:</div>
    <div style="font-size: 24px; font-weight: 700; color: {timer_color};">{timer_text}</div>
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

# Show warning if question is locked
if is_locked:
    st.error("**Czas na to pytanie minął!** Pytanie zostało zablokowane. Przejdź do następnego pytania.")

# Radio buttons with hidden label for accessibility
# Disable if question is locked
selected = st.radio(
    "Odpowiedzi",
    options=['a', 'b', 'c', 'd'],
    format_func=lambda x: f"{x}) {options_text[x]}",
    index=['a', 'b', 'c', 'd'].index(current_answer) if current_answer else None,
    key=f"q_{question['id']}",
    label_visibility="collapsed",
    disabled=is_locked
)

# Save answer when changed - use toast instead of info to avoid button duplication
if not is_locked and selected and selected != current_answer:
    test_engine.save_answer(question['id'], selected)

    # Check for auto-save - use toast instead of st.info()
    if test_engine.should_auto_save():
        answered_count = test_engine.get_answered_count()
        st.toast(f"Auto-zapis: Zapisano postęp ({answered_count} pytań)", icon="✅")
        test_engine.mark_auto_saved(answered_count)

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if current_q_index > 0:
        if st.button("← Poprzednie", use_container_width=True):
            st.session_state.current_question = current_q_index - 1
            test_engine.reset_question_timer()
            st.rerun()

with col2:
    if st.button("Wyloguj się"):
        auth.logout()
        st.switch_page("pages/1_Logowanie_Studenta.py")

with col3:
    if current_q_index < total_questions - 1:
        if st.button("Następne →", use_container_width=True):
            st.session_state.current_question = current_q_index + 1
            test_engine.reset_question_timer()
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
