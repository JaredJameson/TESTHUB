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
    <div style="background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #666;">Wszystkie Testy</div>
        <div style="font-size: 36px; font-weight: 700;">{global_stats['total_tests']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    pass_color = "#2D5016" if global_stats['pass_rate'] >= 70 else "#FFD700" if global_stats['pass_rate'] >= 50 else "#8B0000"
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #666;">Wskaźnik Zdawalności</div>
        <div style="font-size: 36px; font-weight: 700; color: {pass_color};">{global_stats['pass_rate']}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #666;">Średni Wynik</div>
        <div style="font-size: 36px; font-weight: 700;">{global_stats['average_score']}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;">
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #666;">Średnia Ocena</div>
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
        <div style="background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 10px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateX(4px)'; this.style.boxShadow='0 4px 8px rgba(0, 0, 0, 0.1)';" onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 2px 4px rgba(0, 0, 0, 0.05)';">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-weight: 600; font-size: 16px; margin-bottom: 8px;">{category}</div>
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="flex: 1; background: #E0E0E0; border-radius: 10px; height: 24px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, {color} 0%, {color}dd 100%); width: {percentage}%; height: 100%; transition: width 0.3s ease;"></div>
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
        <div style="background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 8px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateX(4px)'; this.style.boxShadow='0 4px 8px rgba(0, 0, 0, 0.1)';" onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 2px 4px rgba(0, 0, 0, 0.05)';">
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
    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

    # Custom styled refresh button with SVG icon
    refresh_clicked = st.button(
        "⟳",
        use_container_width=True,
        key="refresh_button",
        help="Odśwież dane"
    )

    # Custom CSS for this specific button
    st.markdown("""
    <style>
    /* Style refresh button */
    div[data-testid="column"]:nth-child(4) button[kind="secondary"] {
        background: #FFD700 !important;
        border: 1px solid #000000 !important;
        border-radius: 8px !important;
        height: 48px !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #000000 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    div[data-testid="column"]:nth-child(4) button[kind="secondary"]:hover {
        background: #FFC700 !important;
        transform: rotate(90deg) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if refresh_clicked:
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
        status_badge = f'<span style="background: #2D5016; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-right: 8px;">ZALICZONY</span>' if passed else f'<span style="background: #8B0000; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-right: 8px;">NIEZALICZONY</span>'

        st.markdown(f"""
        <div style="background: #FFFFFF; border-left: 4px solid {border_color}; border: 1px solid #E0E0E0; border-left: 4px solid {border_color}; border-radius: 10px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.12)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0, 0, 0, 0.08)';">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-size: 18px; font-weight: 600; margin-bottom: 4px;">
                        {status_badge} {row['First_Name']} {row['Last_Name']}
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
                    {f'<div style="font-size: 12px; color: #8B0000; margin-top: 4px;">Wysłano automatycznie</div>' if row.get('Auto_Submitted') else ''}
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
