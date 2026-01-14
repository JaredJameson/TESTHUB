"""
Teacher Details - Individual Student Result View
"""

import streamlit as st
import json
from modules.ui_components import load_custom_css, section_divider
from modules.auth import AuthManager
from modules.sheets_manager import SheetsManager
from modules.test_engine import TestEngine

# Page config
st.set_page_config(
    page_title="Szczegóły Studenta",
    page_icon="📋",
    layout="centered"
)

load_custom_css()
auth = AuthManager()
sheets_manager = SheetsManager()
test_engine = TestEngine()

# Require teacher authentication
auth.require_authentication(user_type="teacher")

# Header
st.markdown("# Szczegóły Wyniku Studenta")

section_divider()

# Student email input
student_email = st.text_input("Email studenta", placeholder="student@example.com")

if st.button("Wyszukaj", use_container_width=True):
    if student_email:
        st.session_state.search_email = student_email
        st.rerun()

if 'search_email' in st.session_state and st.session_state.search_email:
    # Get student result
    result_data = sheets_manager.get_student_result(st.session_state.search_email)

    if result_data:
        # Display student info
        st.markdown(f"## {result_data['First_Name']} {result_data['Last_Name']}")
        st.markdown(f"**Email:** {result_data['Email']}")
        if result_data.get('Student_ID'):
            st.markdown(f"**ID Studenta:** {result_data['Student_ID']}")
        st.markdown(f"**Data testu:** {result_data['Timestamp']}")

        section_divider()

        # Main result card
        passed = result_data['Status'] == 'ZALICZONY'
        status_color = "#2D5016" if passed else "#8B0000"
        status_text = "ZALICZONY" if passed else "NIEZALICZONY"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #FFFBF0 100%); border-left: 6px solid {status_color}; border: 1px solid #E0E0E0; border-left: 6px solid {status_color}; border-radius: 16px; padding: 32px; text-align: center; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); animation: fadeIn 0.5s ease-out;">
            <div style="font-size: 36px; font-weight: 700; color: {status_color}; margin-bottom: 16px; animation: slideIn 0.4s ease-out;">
                {status_text}
            </div>
            <div style="font-size: 48px; font-weight: 700; color: #000000; margin-bottom: 8px;">
                {result_data['Percentage']}%
            </div>
            <div style="font-size: 20px; color: #666; margin-bottom: 16px;">
                {result_data['Correct_Count']}/27 poprawnych odpowiedzi
            </div>
            <div style="font-size: 18px; padding: 12px 24px; background: #F5F5F5; border: 1px solid #E0E0E0; border-radius: 24px; display: inline-block; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
                Ocena: {result_data['Grade']} - {result_data['Grade_Text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Time and submission info
        st.markdown(f"**Czas rozwiązywania:** {result_data['Time_Spent_Minutes']} min")

        if result_data.get('Auto_Submitted'):
            st.warning("⏰ Test został automatycznie wysłany po upływie czasu")

        st.markdown(f"**Numer próby:** {result_data.get('Attempt_Number', 1)}")
        st.markdown(f"**Wersja testu:** {result_data.get('Test_Version', 'v1.0')}")

        section_divider()

        # Parse Details JSON
        try:
            details_json = result_data['Details_JSON']
            if isinstance(details_json, str):
                details = json.loads(details_json)
            else:
                details = details_json

            # Category breakdown
            st.markdown("### Wyniki według kategorii")

            category_breakdown = details.get('category_breakdown', {})

            for category, stats in category_breakdown.items():
                percentage = stats.get('percentage', 0)
                correct = stats.get('correct', 0)
                total = stats.get('total', 0)

                # Color code
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
                        <div style="font-weight: 600; color: {color}; min-width: 100px; text-align: right;">
                            {correct}/{total} ({percentage}%)
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            section_divider()

            # Detailed answers
            st.markdown("### Szczegółowe odpowiedzi")

            show_details = st.checkbox("Pokaż wszystkie pytania i odpowiedzi", value=True)

            if show_details:
                answers = details.get('answers', {})

                # Sort by question ID
                sorted_answers = sorted(answers.items(), key=lambda x: int(x[0]))

                for q_id, answer_data in sorted_answers:
                    is_correct = answer_data.get('is_correct', False)

                    # Status badge and color
                    status_badge = f'<span style="background: #2D5016; color: white; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 8px;">POPRAWNE</span>' if is_correct else f'<span style="background: #8B0000; color: white; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 8px;">NIEPOPRAWNE</span>'
                    border_color = "#2D5016" if is_correct else "#8B0000"

                    # Get full question data
                    question = test_engine.get_question(int(q_id) - 1)

                    if question:
                        st.markdown(f"""
                        <div style="background: #FFFFFF; border-left: 4px solid {border_color}; border: 1px solid #E0E0E0; border-left: 4px solid {border_color}; border-radius: 10px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0, 0, 0, 0.12)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0, 0, 0, 0.08)';">
                            <div style="font-weight: 600; font-size: 16px; margin-bottom: 12px;">
                                {status_badge} Pytanie {q_id}: {answer_data.get('category', 'Unknown')}
                            </div>
                            <div style="margin-bottom: 12px; color: #000000;">
                                {question['question']}
                            </div>
                            <div style="background: #F5F5F5; padding: 12px; border: 1px solid #E0E0E0; border-radius: 8px; margin-bottom: 8px;">
                                <strong>Odpowiedź studenta:</strong> {answer_data.get('selected', 'Brak odpowiedzi').upper()}
                                {f"- {question['options'].get(answer_data.get('selected', ''), '')}" if answer_data.get('selected') else ''}
                            </div>
                            <div style="background: #E8F5E9; padding: 12px; border: 1px solid {border_color}; border-radius: 8px; margin-bottom: 8px;">
                                <strong>Poprawna odpowiedź:</strong> {answer_data.get('correct', '').upper()}
                                {f"- {question['options'].get(answer_data.get('correct', ''), '')}" if answer_data.get('correct') else ''}
                            </div>
                            {f'<div style="padding: 8px; color: #666; font-size: 14px;"><em><strong>Wyjaśnienie:</strong> {question.get("explanation", "")}</em></div>' if question.get('explanation') else ''}
                        </div>
                        """, unsafe_allow_html=True)

            section_divider()

            # Metadata
            st.markdown("### Metadane testu")

            metadata = details.get('metadata', {})

            st.markdown(f"""
            - **Czas rozpoczęcia:** {metadata.get('start_time', 'N/A')}
            - **Czas zakończenia:** {metadata.get('end_time', 'N/A')}
            - **Auto-submit:** {'Tak' if metadata.get('auto_submitted', False) else 'Nie'}
            - **Auto-save checkpointy:** {', '.join(map(str, metadata.get('auto_saves', [])))}
            - **Przeglądarka:** {result_data.get('Browser_Info', 'Unknown')}
            """)

        except Exception as e:
            st.error(f"Błąd przetwarzania szczegółów: {e}")

        section_divider()

        # Actions
        col1, col2 = st.columns(2)

        with col1:
            if st.button("← Powrót do dashboardu", use_container_width=True):
                del st.session_state.search_email
                st.switch_page("pages/5_Dashboard_Nauczyciela.py")

        with col2:
            if st.button("Wyloguj się", use_container_width=True):
                auth.logout()
                st.switch_page("app.py")

    else:
        st.warning(f"Nie znaleziono wyników dla email: {st.session_state.search_email}")

        if st.button("← Powrót do dashboardu", use_container_width=True):
            del st.session_state.search_email
            st.switch_page("pages/5_Dashboard_Nauczyciela.py")

else:
    st.info("👆 Wprowadź email studenta aby zobaczyć szczegółowe wyniki")

    if st.button("← Powrót do dashboardu", use_container_width=True):
        st.switch_page("pages/5_Dashboard_Nauczyciela.py")
