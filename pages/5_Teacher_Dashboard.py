"""
Teacher Dashboard - View All Student Results
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.ui_components import load_custom_css, section_divider
from modules.auth import AuthManager
from modules.sheets_manager import SheetsManager
from modules.analytics import Analytics

# Page config
st.set_page_config(
    page_title="Panel Nauczyciela",
    page_icon="👨‍🏫",
    layout="wide"
)

load_custom_css()
auth = AuthManager()
sheets_manager = SheetsManager()
analytics = Analytics(sheets_manager)

# Require teacher authentication
auth.require_authentication(user_type="teacher")

# Header
st.markdown("# Panel Nauczyciela")
st.markdown("## Wyniki Testów - AI w Marketingu")

section_divider()

# Global Statistics
st.markdown("### Statystyki Globalne")

global_stats = analytics.get_global_statistics()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 2px solid #000000; padding: 20px; text-align: center;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">Wszystkie Testy</div>
        <div style="font-size: 36px; font-weight: 700;">{global_stats['total_tests']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    pass_color = "#2D5016" if global_stats['pass_rate'] >= 70 else "#FFD700" if global_stats['pass_rate'] >= 50 else "#8B0000"
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 2px solid #000000; padding: 20px; text-align: center;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">Wskaźnik Zdawalności</div>
        <div style="font-size: 36px; font-weight: 700; color: {pass_color};">{global_stats['pass_rate']}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 2px solid #000000; padding: 20px; text-align: center;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">Średni Wynik</div>
        <div style="font-size: 36px; font-weight: 700;">{global_stats['average_score']}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 2px solid #000000; padding: 20px; text-align: center;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">Średnia Ocena</div>
        <div style="font-size: 36px; font-weight: 700;">{global_stats['average_grade']}</div>
    </div>
    """, unsafe_allow_html=True)

section_divider()

# Category Analysis
st.markdown("### Wyniki według Kategorii")

category_analysis = analytics.get_category_analysis()

if category_analysis:
    for category, stats in category_analysis.items():
        percentage = stats['average_percentage']
        if percentage >= 80:
            color = "#2D5016"
        elif percentage >= 60:
            color = "#FFD700"
        else:
            color = "#8B0000"

        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #000000; padding: 16px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-weight: 600; font-size: 16px; margin-bottom: 8px;">{category}</div>
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="flex: 1; background: #F5F5F5; border: 1px solid #000000; height: 24px;">
                            <div style="background: {color}; width: {percentage}%; height: 100%;"></div>
                        </div>
                        <div style="font-weight: 600; color: {color}; min-width: 100px; text-align: right;">
                            {stats['average_correct']:.1f}/{stats['total_questions']} ({percentage}%)
                        </div>
                    </div>
                </div>
                <div style="margin-left: 24px; font-size: 14px; color: #666;">
                    {stats['students_analyzed']} studentów
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Brak danych kategorii")

section_divider()

# Hardest Questions
st.markdown("### Najtrudniejsze Pytania")

hardest_questions = analytics.get_hardest_questions(top_n=5)

if hardest_questions:
    for q in hardest_questions:
        correct_rate = q['correct_rate']
        if correct_rate >= 70:
            color = "#2D5016"
        elif correct_rate >= 50:
            color = "#FFD700"
        else:
            color = "#8B0000"

        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #000000; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-weight: 600;">Pytanie #{q['question_id']}</span> - {q['category']}
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 14px; color: #666;">
                    {q['correct_count']}/{q['total_attempts']} poprawnych
                </div>
                <div style="font-weight: 700; color: {color}; min-width: 60px; text-align: right;">
                    {correct_rate}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Brak danych o pytaniach")

section_divider()

# Student Results List
st.markdown("### Lista Wyników Studentów")

# Filters
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

with col1:
    status_filter = st.selectbox(
        "Status",
        ["Wszystkie", "Zaliczeni", "Niezaliczeni"]
    )

with col2:
    sort_by = st.selectbox(
        "Sortuj według",
        ["Data (najnowsze)", "Data (najstarsze)", "Wynik (najwyższy)", "Wynik (najniższy)", "Nazwisko A-Z", "Nazwisko Z-A"]
    )

with col3:
    limit = st.selectbox(
        "Pokaż",
        [10, 25, 50, 100, "Wszystkie"]
    )

with col4:
    if st.button("🔄 Odśwież", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Get all results
df = sheets_manager.get_all_results()

if not df.empty:
    # Apply status filter
    if status_filter == "Zaliczeni":
        df = df[df['Status'] == 'ZALICZONY']
    elif status_filter == "Niezaliczeni":
        df = df[df['Status'] == 'NIEZALICZONY']

    # Apply sorting
    if sort_by == "Data (najnowsze)":
        df = df.sort_values(by='Timestamp', ascending=False)
    elif sort_by == "Data (najstarsze)":
        df = df.sort_values(by='Timestamp', ascending=True)
    elif sort_by == "Wynik (najwyższy)":
        df = df.sort_values(by='Percentage', ascending=False)
    elif sort_by == "Wynik (najniższy)":
        df = df.sort_values(by='Percentage', ascending=True)
    elif sort_by == "Nazwisko A-Z":
        df = df.sort_values(by='Last_Name', ascending=True)
    elif sort_by == "Nazwisko Z-A":
        df = df.sort_values(by='Last_Name', ascending=False)

    # Apply limit
    if limit != "Wszystkie":
        df = df.head(limit)

    # Display results count
    st.markdown(f"**Wyników: {len(df)}**")

    # Display results table
    for idx, row in df.iterrows():
        passed = row['Status'] == 'ZALICZONY'
        border_color = "#2D5016" if passed else "#8B0000"
        status_emoji = "✅" if passed else "❌"

        st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid {border_color}; padding: 16px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-size: 18px; font-weight: 600; margin-bottom: 4px;">
                        {status_emoji} {row['First_Name']} {row['Last_Name']}
                    </div>
                    <div style="font-size: 14px; color: #666; margin-bottom: 4px;">
                        {row['Email']} {f"| ID: {row['Student_ID']}" if row.get('Student_ID') else ''}
                    </div>
                    <div style="font-size: 14px; color: #666;">
                        {row['Timestamp']}
                    </div>
                </div>
                <div style="text-align: right; margin-left: 24px;">
                    <div style="font-size: 32px; font-weight: 700; color: {border_color}; margin-bottom: 4px;">
                        {row['Percentage']}%
                    </div>
                    <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">
                        {row['Grade']} - {row['Grade_Text']}
                    </div>
                    <div style="font-size: 14px; color: #666;">
                        {row['Correct_Count']}/27 poprawnych | {row['Time_Spent_Minutes']} min
                    </div>
                    {f'<div style="font-size: 12px; color: #8B0000; margin-top: 4px;">⏰ Auto-submit</div>' if row.get('Auto_Submitted') else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    section_divider()

    # Export functionality
    st.markdown("### Eksport Danych")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Pobierz CSV",
        data=csv,
        file_name=f"wyniki_testow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

else:
    st.info("Brak wyników testów w systemie")

section_divider()

# Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("← Wyloguj się", use_container_width=True):
        auth.logout()
        st.switch_page("app.py")

with col2:
    if st.button("Strona główna", use_container_width=True):
        st.switch_page("app.py")
