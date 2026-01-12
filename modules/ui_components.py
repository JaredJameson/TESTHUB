"""
UI Components and Custom Styling
Implements brutalist design system from UI/UX guidelines
"""

import streamlit as st

def load_custom_css():
    """
    Load custom CSS to override Streamlit defaults

    Design Rules:
    - NO rounded corners (border-radius: 0)
    - NO shadows or gradients
    - Black borders (1px solid #000000)
    - Yellow accents (#FFD700) for interactive elements
    - Poppins font for all text
    """
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Global Reset */
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        border-radius: 0 !important;  /* CRITICAL: No rounded corners */
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
    }

    /* Button Styles (Primary) */
    .stButton > button {
        background: #FFD700;
        color: #000000;
        border: 1px solid #000000;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        cursor: pointer;
        transition: none;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        background: #FFC700;
        border: 1px solid #000000;
    }

    .stButton > button:active {
        background: #E6BE00;
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #FFFFFF;
        color: #000000;
        border: 1px solid #000000;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 2px solid #FFD700;
        box-shadow: none !important;
    }

    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        font-size: 14px;
        font-weight: 500;
        color: #000000;
        font-family: 'Poppins', sans-serif;
    }

    /* Radio Buttons */
    .stRadio > div {
        background: #FFFFFF;
        border: 1px solid #000000;
        padding: 16px;
        margin-bottom: 8px;
    }

    .stRadio > div:hover {
        background: #F5F5F5;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
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
        border-collapse: collapse;
        width: 100%;
        border: 1px solid #000000;
    }

    th {
        background: #E8E8E8;
        border: 1px solid #000000;
        padding: 16px;
        text-align: left;
        font-weight: 600;
    }

    td {
        border: 1px solid #000000;
        padding: 16px;
    }

    tr:nth-child(even) {
        background: #F5F5F5;
    }

    tbody tr:hover {
        background: #FFD700;
    }

    /* Progress Bar */
    .stProgress > div > div {
        background: #FFFFFF;
        border: 1px solid #000000;
    }

    .stProgress > div > div > div {
        background: #FFD700;
        border-right: 1px solid #000000;
    }

    /* Alerts/Messages */
    .stAlert {
        background: #FFFFFF;
        border: 2px solid #000000;
        padding: 16px;
    }

    /* Cards */
    .element-container {
        background: #FFFFFF;
        border: 1px solid #000000;
        padding: 24px;
        margin-bottom: 24px;
    }

    /* Remove all transitions and animations */
    * {
        transition: none !important;
        animation: none !important;
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
    Custom card component with black border

    Args:
        title: Card header text
        content: Card body HTML content
    """
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #000000; padding: 24px; margin-bottom: 24px;">
        <div style="font-size: 20px; font-weight: 600; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #000000;">
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
        text = "ZALICZONY"
    else:
        color = "#8B0000"
        text = "NIEZALICZONY"

    return f"""
    <span style="display: inline-block; padding: 4px 12px; font-size: 14px; font-weight: 600;
                 border: 1px solid #000000; color: {color}; background: #FFFFFF;">
        {text}
    </span>
    """


def section_divider():
    """Add section divider (black line)"""
    st.markdown('<hr style="border-top: 1px solid #000000; margin: 48px 0;">', unsafe_allow_html=True)


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
