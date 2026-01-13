"""
Student Results Page - Display Test Results
"""

import streamlit as st
from modules.ui_components import load_custom_css, hide_navigation_for_user, status_badge, custom_card, section_divider
from modules.auth import AuthManager
from modules.test_engine import TestEngine
from modules.email_service import EmailService

# Page config
st.set_page_config(
    page_title="Wyniki Testu",
    page_icon="📊",
    layout="centered"
)

load_custom_css()
hide_navigation_for_user()
auth = AuthManager()
test_engine = TestEngine()
email_service = EmailService()

# Require authentication
auth.require_authentication(user_type="student")

# Check if test was completed
if not st.session_state.get('test_completed', False):
    st.warning("Test nie został jeszcze ukończony")
    if st.button("Powrót do testu"):
        st.switch_page("pages/2_Test_Studenta.py")
    st.stop()

# Calculate results if not already done
if 'test_results' not in st.session_state:
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
    from modules.sheets_manager import SheetsManager
    sheets = SheetsManager()
    sheets.save_test_result(formatted_results)

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

results = st.session_state.test_results

# Header
st.markdown("# Wyniki Testu")
st.markdown(f"## {st.session_state.first_name} {st.session_state.last_name}")

section_divider()

# Main results card
passed = results['passed']
status_color = "#2D5016" if passed else "#8B0000"
status_text = "ZALICZONY" if passed else "NIEZALICZONY"

st.markdown(f"""
<div style="background: linear-gradient(135deg, #FFFFFF 0%, #FFFBF0 100%); border-left: 6px solid {status_color}; border: 1px solid #E0E0E0; border-left: 6px solid {status_color}; border-radius: 16px; padding: 32px; margin-bottom: 24px; text-align: center; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); animation: fadeIn 0.5s ease-out;">
    <div style="font-size: 48px; font-weight: 700; color: {status_color}; margin-bottom: 16px; animation: slideIn 0.4s ease-out;">
        {status_text}
    </div>
    <div style="font-size: 64px; font-weight: 700; color: #000000; margin-bottom: 8px;">
        {results['percentage']}%
    </div>
    <div style="font-size: 24px; color: #666; margin-bottom: 16px;">
        {results['correct_count']}/{results['total_questions']} poprawnych odpowiedzi
    </div>
    <div style="font-size: 20px; color: #000000; padding: 12px 24px; background: #F5F5F5; border: 1px solid #E0E0E0; border-radius: 24px; display: inline-block; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
        Ocena: {results['grade']} - {results['grade_text']}
    </div>
</div>
""", unsafe_allow_html=True)

# Time spent
time_minutes = int(results['time_spent_seconds'] / 60)
time_seconds = results['time_spent_seconds'] % 60
st.markdown(f"**Czas rozwiązywania:** {time_minutes} min {time_seconds} sek")

# Auto-submitted info
if st.session_state.get('auto_submitted', False):
    st.info("ℹ️ Test został automatycznie wysłany po upływie czasu")

section_divider()

# Category breakdown
st.markdown("## Wyniki według kategorii")

category_stats = results.get('category_stats', {})

for category, stats in category_stats.items():
    percentage = stats.get('percentage', 0)
    correct = stats.get('correct', 0)
    total = stats.get('total', 0)

    # Color code based on percentage
    if percentage >= 80:
        color = "#2D5016"
    elif percentage >= 60:
        color = "#FFD700"
    else:
        color = "#8B0000"

    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 10px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateX(4px)'; this.style.boxShadow='0 4px 8px rgba(0, 0, 0, 0.1)';" onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 2px 4px rgba(0, 0, 0, 0.05)';">
        <div style="font-weight: 600; font-size: 18px; margin-bottom: 8px;">{category}</div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="flex: 1; background: #E0E0E0; border-radius: 10px; height: 24px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, {color} 0%, {color}dd 100%); width: {percentage}%; height: 100%; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-weight: 600; color: {color}; min-width: 80px; text-align: right;">
                {correct}/{total} ({percentage}%)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

section_divider()

# Detailed answers
st.markdown("## Szczegółowe odpowiedzi")

show_details = st.checkbox("Pokaż szczegóły wszystkich pytań")

if show_details:
    details = results.get('details', {})

    for q_id in sorted([int(k) for k in details.keys()]):
        detail = details[str(q_id)]
        is_correct = detail['is_correct']

        # Icon and color
        icon = "✅" if is_correct else "❌"
        border_color = "#2D5016" if is_correct else "#8B0000"

        st.markdown(f"""
        <div style="background: #FFFFFF; border-left: 4px solid {border_color}; border: 1px solid #E0E0E0; border-left: 4px solid {border_color}; border-radius: 10px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0, 0, 0, 0.12)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0, 0, 0, 0.08)';">
            <div style="font-weight: 600; font-size: 16px; margin-bottom: 12px;">
                {icon} Pytanie {q_id}: {detail['category']}
            </div>
            <div style="margin-bottom: 12px; color: #000000;">
                {detail['question']}
            </div>
            <div style="background: #F5F5F5; padding: 12px; border: 1px solid #E0E0E0; border-radius: 8px; margin-bottom: 8px;">
                <strong>Twoja odpowiedź:</strong> {detail['selected'].upper() if detail['selected'] else 'Brak odpowiedzi'}
            </div>
            <div style="background: #E8F5E9; padding: 12px; border: 1px solid {border_color}; border-radius: 8px; margin-bottom: 8px;">
                <strong>Poprawna odpowiedź:</strong> {detail['correct'].upper()}
            </div>
            {f'<div style="padding: 8px; color: #666; font-size: 14px;"><em>{detail["explanation"]}</em></div>' if detail.get('explanation') else ''}
        </div>
        """, unsafe_allow_html=True)

section_divider()

# Actions
st.markdown("## Co dalej?")

col1, col2 = st.columns(2)

with col1:
    if st.button("Wyloguj się", use_container_width=True):
        auth.logout()
        st.switch_page("app.py")

with col2:
    if st.button("Strona główna", use_container_width=True):
        st.switch_page("app.py")

# Footer
st.markdown("---")
st.info("📧 Wyniki zostały zapisane i będą dostępne dla nauczyciela. Otrzymasz również email z potwierdzeniem.")
