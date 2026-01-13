"""
UI Components and Custom Styling
Implements brutalist design system from UI/UX guidelines
"""

import streamlit as st

def hide_navigation_for_user():
    """
    Hide navigation sidebar based on user authentication and type
    - Hides all navigation for non-authenticated users
    - Hides teacher pages for students
    """
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        # Hide entire navigation for non-authenticated users
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)
    elif st.session_state.get('user_type') == 'student':
        # Hide teacher pages for students
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] li:has(a[href*="Panel_Nauczyciela"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Dashboard_Nauczyciela"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Szczegoly_Studenta"]) {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)


def load_custom_css():
    """
    Load custom CSS to override Streamlit defaults

    Modern Design Rules:
    - Rounded corners (8px for cards, 6px for buttons)
    - Smooth transitions and animations
    - Subtle shadows for depth
    - Yellow accents (#FFD700) for interactive elements
    - Poppins font for all text
    """
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Keyframe Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }

    /* Global Reset */
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Streamlit App Background */
    .stApp {
        background-color: #F5F5F5;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Container Styles */
    .main .block-container {
        max-width: 1200px;
        padding: 40px 40px 40px 40px;
        animation: fadeIn 0.5s ease-out;
    }

    /* Button Styles (Primary) */
    .stButton > button {
        background: #FFD700;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 8px !important;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        background: #FFC700;
        border: 1px solid #000000;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    .stButton > button:active {
        background: #E6BE00;
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: #FFFFFF;
        color: #000000;
        border: 1px solid #E0E0E0;
        border-radius: 8px !important;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 2px solid #FFD700;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
        outline: none;
    }

    .stSelectbox > div > div:hover {
        border-color: #FFD700;
    }

    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        font-size: 14px;
        font-weight: 500;
        color: #000000;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 8px;
    }

    /* Radio Buttons */
    .stRadio > div {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px !important;
        padding: 16px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .stRadio > div:hover {
        background: #FFFBF0;
        border-color: #FFD700;
        transform: translateX(4px);
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        animation: slideIn 0.4s ease-out;
    }

    h1 { font-size: 32px !important; }
    h2 { font-size: 24px !important; }
    h3 { font-size: 20px !important; }

    /* Body Text */
    p, div, span, li {
        color: #000000;
        font-family: 'Poppins', sans-serif;
    }

    /* Tables */
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border: 1px solid #E0E0E0;
        border-radius: 8px !important;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    th {
        background: #F5F5F5;
        border-bottom: 2px solid #E0E0E0;
        padding: 16px;
        text-align: left;
        font-weight: 600;
    }

    td {
        border-bottom: 1px solid #E0E0E0;
        padding: 16px;
        background: #FFFFFF;
    }

    tr:last-child td {
        border-bottom: none;
    }

    tbody tr {
        transition: all 0.2s ease;
    }

    tbody tr:hover {
        background: #FFFBF0;
        transform: scale(1.01);
    }

    /* Progress Bar */
    .stProgress > div > div {
        background: #E0E0E0;
        border: none;
        border-radius: 10px !important;
        overflow: hidden;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FFD700 0%, #FFC700 100%);
        border: none;
        border-radius: 10px !important;
        transition: width 0.3s ease;
    }

    /* Alerts/Messages */
    .stAlert {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-left: 4px solid #FFD700;
        border-radius: 8px !important;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        animation: slideIn 0.3s ease-out;
    }

    /* Cards */
    .element-container {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px !important;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        animation: fadeIn 0.4s ease-out;
    }

    .element-container:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }

    /* Smooth Transitions */
    * {
        transition: background-color 0.2s ease,
                    border-color 0.2s ease,
                    color 0.2s ease,
                    transform 0.2s ease;
    }

    /* Custom Refresh Icon Button */
    .refresh-icon-button {
        background: #FFD700;
        border: 1px solid #000000;
        border-radius: 8px !important;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .refresh-icon-button:hover {
        background: #FFC700;
        transform: rotate(90deg) scale(1.1);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    .refresh-icon-button svg {
        width: 24px;
        height: 24px;
        transition: transform 0.3s ease;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def custom_button(label: str, key: str = None, button_type: str = "primary") -> bool:
    """
    Custom styled button component

    Args:
        label: Button text
        key: Unique key for Streamlit
        button_type: "primary" or "secondary"

    Returns:
        bool: True if button was clicked
    """
    # Streamlit buttons automatically use CSS styling
    return st.button(label, key=key)


def custom_card(title: str, content: str):
    """
    Custom card component with modern design

    Args:
        title: Card header text
        content: Card body HTML content
    """
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); transition: all 0.3s ease; animation: fadeIn 0.4s ease-out;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 16px rgba(0, 0, 0, 0.12)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0, 0, 0, 0.08)';">
        <div style="font-size: 20px; font-weight: 600; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #E0E0E0;">
            {title}
        </div>
        <div style="font-size: 16px; line-height: 1.6;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def status_badge(passed: bool) -> str:
    """
    Status badge component

    Args:
        passed: True for ZALICZONY, False for NIEZALICZONY

    Returns:
        str: HTML for status badge
    """
    if passed:
        color = "#2D5016"
        bg_color = "#E8F5E9"
        text = "ZALICZONY"
    else:
        color = "#8B0000"
        bg_color = "#FFEBEE"
        text = "NIEZALICZONY"

    return f"""
    <span style="display: inline-block; padding: 6px 14px; font-size: 14px; font-weight: 600;
                 border: 1px solid {color}; border-radius: 20px; color: {color}; background: {bg_color};
                 transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
        {text}
    </span>
    """


def section_divider():
    """Add section divider (subtle line)"""
    st.markdown('<hr style="border: none; border-top: 1px solid #E0E0E0; margin: 48px 0;">', unsafe_allow_html=True)


def progress_bar(current: int, total: int):
    """
    Custom progress bar

    Args:
        current: Current progress (e.g., 15)
        total: Total items (e.g., 27)
    """
    percentage = int((current / total) * 100)
    st.progress(current / total)
    st.markdown(f"<p style='text-align: center; font-weight: 600;'>{current}/{total} ({percentage}%)</p>",
                unsafe_allow_html=True)
