# 📋 IMPLEMENTATION PLAN
## AI Marketing Test Platform - Step-by-Step Build Guide

**Version:** 2.0
**Date:** 2026-01-12
**Estimated Timeline:** 5 days (with 1-day buffer)

---

## TABLE OF CONTENTS

1. [Implementation Overview](#1-implementation-overview)
2. [Phase 1: Foundation](#2-phase-1-foundation)
3. [Phase 2: Core Test Logic](#3-phase-2-core-test-logic)
4. [Phase 3: Notifications & Teacher Dashboard](#4-phase-3-notifications--teacher-dashboard)
5. [Phase 4: Polish & Deployment](#5-phase-4-polish--deployment)
6. [Context Handoff Strategy](#6-context-handoff-strategy)
7. [Testing & Validation](#7-testing--validation)

---

## 1. IMPLEMENTATION OVERVIEW

### 1.1 Development Philosophy

**Build Order Principle:** Foundation → Core → Integration → Polish

```
Phase 1 (Day 1):      Phase 2 (Day 2):      Phase 3 (Day 3):      Phase 4 (Day 4-5):
Foundation           Core Logic            Integration           Quality
├─ Project Setup     ├─ Test Engine        ├─ Email Service      ├─ Testing
├─ Custom CSS        ├─ Questions Data     ├─ Teacher Dashboard  ├─ Mobile
├─ UI Components     ├─ Student Test UI    ├─ Analytics          ├─ Accessibility
├─ Google Sheets     ├─ Results Display    └─ Student Details    ├─ Error Handling
└─ Authentication    └─ Auto-Save                                 └─ Deployment
```

### 1.2 Module Implementation Sequence

```
DAY 1 - FOUNDATION LAYER
┌────────────────────────────────────────┐
│  1. ui_components.py                   │
│  2. sheets_manager.py                  │
│  3. auth.py                            │
│  4. app.py (landing page)              │
│  5. Student/Teacher login pages        │
└────────────────────────────────────────┘

DAY 2 - BUSINESS LOGIC LAYER
┌────────────────────────────────────────┐
│  1. data/questions.json                │
│  2. test_engine.py                     │
│  3. Student test interface             │
│  4. Results display page               │
│  5. Auto-save mechanism                │
└────────────────────────────────────────┘

DAY 3 - INTEGRATION LAYER
┌────────────────────────────────────────┐
│  1. email_service.py                   │
│  2. analytics.py                       │
│  3. Teacher dashboard                  │
│  4. Student detail view                │
│  5. Export CSV functionality           │
└────────────────────────────────────────┘

DAY 4-5 - QUALITY LAYER
┌────────────────────────────────────────┐
│  1. Unit tests                         │
│  2. Mobile responsiveness              │
│  3. Accessibility compliance           │
│  4. Error handling                     │
│  5. Deployment to Streamlit Cloud      │
└────────────────────────────────────────┘
```

### 1.3 Session Boundaries

**Critical:** Each phase is designed for a single context window session.

| Phase | Duration | Context Handoff | Resume Point |
|-------|----------|-----------------|--------------|
| Phase 1 | 8-10h | SESSION_1_HANDOFF.md | modules/test_engine.py |
| Phase 2 | 8-10h | SESSION_2_HANDOFF.md | modules/email_service.py |
| Phase 3 | 6-8h | SESSION_3_HANDOFF.md | testing & polish |
| Phase 4 | 6-8h | N/A (final) | deployment |

---

## 2. PHASE 1: FOUNDATION

**Goal:** Create the visual and data foundation for the entire application

**Duration:** Day 1 (8-10 hours)
**Deliverables:** Working login system + Google Sheets integration + Custom UI

### 2.1 Project Setup

**Step 1.1: Create Project Structure**

```bash
# Create directory structure
mkdir -p ai-test-platform/{modules,pages,data,assets,tests,docs/handoffs}
cd ai-test-platform

# Create files
touch app.py
touch modules/{__init__.py,auth.py,test_engine.py,sheets_manager.py,email_service.py,analytics.py,ui_components.py}
touch pages/{1_Student_Login.py,2_Student_Test.py,3_Student_Results.py,4_Teacher_Login.py,5_Teacher_Dashboard.py,6_Teacher_Details.py}
touch data/{questions.json,test_config.json}
touch .streamlit/{config.toml,secrets.toml}
touch {.env.example,.gitignore,requirements.txt,README.md}
```

**Step 1.2: Initialize Git Repository**

```bash
git init
echo ".env\n.streamlit/secrets.toml\n*.pyc\n__pycache__/\n.DS_Store" > .gitignore
git add .
git commit -m "Initial project structure"
```

**Step 1.3: Create requirements.txt**

```text
streamlit==1.30.0
gspread==5.12.0
oauth2client==4.1.3
pandas==2.1.4
plotly==5.18.0
python-dotenv==1.0.0
Pillow==10.1.0
```

**Step 1.4: Create .streamlit/config.toml**

```toml
[theme]
primaryColor = "#FFD700"
backgroundColor = "#F5F5F5"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#000000"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 1

[browser]
gatherUsageStats = false
```

### 2.2 Custom CSS Implementation

**Step 2.1: Create modules/ui_components.py**

```python
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
```

### 2.3 Google Sheets Integration

**Step 3.1: Setup Google Sheets**

```bash
# Manual steps (document in SETUP_GUIDE.md):
1. Create Google Cloud Project
2. Enable Google Sheets API
3. Create Service Account
4. Download JSON credentials
5. Create Google Sheets with 3 sheets:
   - "Wyniki_Testow" (test results)
   - "Teachers" (teacher credentials)
   - "Config" (system configuration)
6. Share Sheets with service account email
```

**Step 3.2: Create modules/sheets_manager.py**

```python
"""
Google Sheets Manager
Handles all Google Sheets operations with retry logic
"""

import os
import json
import time
from datetime import datetime
from functools import wraps
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st


def retry_on_failure(max_attempts=3, delay=2, backoff='exponential'):
    """
    Decorator for retry logic with exponential backoff

    Args:
        max_attempts: Maximum retry attempts
        delay: Initial delay in seconds
        backoff: 'exponential' or 'linear'
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts - 1:
                        wait_time = delay * (2 ** attempt) if backoff == 'exponential' else delay
                        print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"All {max_attempts} attempts failed: {e}")
                        raise e
        return wrapper
    return decorator


class SheetsManager:
    """
    Google Sheets Manager with caching and error handling
    """

    def __init__(self):
        """Initialize Google Sheets client"""
        self.client = self._authenticate()
        self.sheet_id = st.secrets['google_sheets']['sheet_id']
        self.workbook = self.client.open_by_key(self.sheet_id)

    def _authenticate(self):
        """Authenticate with Google Sheets API using service account"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        # Load credentials from Streamlit secrets
        creds_dict = dict(st.secrets['google_sheets'])
        creds_dict.pop('sheet_id', None)  # Remove sheet_id if present

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        return gspread.authorize(credentials)

    @retry_on_failure(max_attempts=3, delay=2, backoff='exponential')
    def save_test_result(self, result_data: dict) -> bool:
        """
        Save complete test result to Google Sheets

        Args:
            result_data: Dictionary with test results

        Returns:
            bool: True if successful

        Schema:
            A: Timestamp, B: Email, C: First_Name, D: Last_Name, E: Student_ID,
            F: Correct_Count, G: Percentage, H: Grade, I: Grade_Text, J: Status,
            K: Time_Spent_Minutes, L: Details_JSON, M: Test_Version, N: Browser_Info,
            O: Attempt_Number, P: Auto_Submitted
        """
        try:
            worksheet = self.workbook.worksheet("Wyniki_Testow")

            # Prepare row data
            row = [
                datetime.now().isoformat(),
                result_data['email'],
                result_data['first_name'],
                result_data['last_name'],
                result_data.get('student_id', ''),
                result_data['correct_count'],
                result_data['percentage'],
                result_data['grade'],
                result_data['grade_text'],
                "ZALICZONY" if result_data['passed'] else "NIEZALICZONY",
                round(result_data['time_spent_seconds'] / 60, 1),
                json.dumps(result_data['details'], ensure_ascii=False),
                result_data.get('test_version', 'v1.0'),
                result_data.get('browser_info', 'Unknown'),
                result_data.get('attempt_number', 1),
                result_data.get('auto_submitted', False)
            ]

            worksheet.append_row(row)
            return True

        except Exception as e:
            print(f"Error saving to Sheets: {e}")
            # TODO: Save to local cache for retry
            return False

    @retry_on_failure(max_attempts=3, delay=2)
    def auto_save_progress(self, student_data: dict, answers: dict, checkpoint: int) -> bool:
        """
        Auto-save test progress (NEW FEATURE)

        Args:
            student_data: Student information
            answers: Current answers dict
            checkpoint: Question number checkpoint (5, 10, 15, etc.)

        Returns:
            bool: True if successful
        """
        # Could save to separate "Progress" sheet or update row if exists
        # For MVP, we'll implement basic version
        pass  # Implement in Phase 2

    @st.cache_data(ttl=60)
    def get_all_results(_self) -> pd.DataFrame:
        """
        Retrieve all test results (cached for 60 seconds)

        Returns:
            pd.DataFrame: All test results
        """
        try:
            worksheet = _self.workbook.worksheet("Wyniki_Testow")
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error loading from Sheets: {e}")
            return pd.DataFrame()

    def get_student_result(self, email: str) -> dict:
        """
        Get specific student's test result

        Args:
            email: Student email address

        Returns:
            dict: Student's test data or None
        """
        try:
            df = self.get_all_results()
            student_data = df[df['Email'] == email]

            if len(student_data) > 0:
                return student_data.iloc[-1].to_dict()  # Return most recent attempt
            return None

        except Exception as e:
            print(f"Error finding student: {e}")
            return None

    def check_duplicate_test(self, email: str) -> tuple:
        """
        Check if student already completed test

        Args:
            email: Student email

        Returns:
            tuple: (already_taken: bool, attempt_count: int, last_result: dict)
        """
        try:
            df = self.get_all_results()
            existing = df[df['Email'] == email]

            if len(existing) > 0:
                # Check config for max attempts
                max_attempts = 2  # Default, should load from Config sheet
                last_result = existing.iloc[-1].to_dict()

                if len(existing) >= max_attempts:
                    return (True, len(existing), last_result)
                else:
                    return (False, len(existing), last_result)

            return (False, 0, None)

        except Exception as e:
            print(f"Error checking duplicate: {e}")
            return (False, 0, None)

    @retry_on_failure(max_attempts=3, delay=2)
    def verify_teacher_credentials(self, email: str, password_hash: str) -> bool:
        """
        Verify teacher login credentials

        Args:
            email: Teacher email
            password_hash: SHA256 hash of password

        Returns:
            bool: True if valid credentials
        """
        try:
            worksheet = self.workbook.worksheet("Teachers")
            data = worksheet.get_all_records()

            for row in data:
                if row['Email'] == email and row['Password_Hash'] == password_hash:
                    # Update last login time
                    # (implement in Phase 1 if time permits)
                    return True
            return False

        except Exception as e:
            print(f"Error verifying teacher: {e}")
            return False
```

### 2.4 Authentication Module

**Step 4.1: Create modules/auth.py**

```python
"""
Authentication and Session Management
"""

import re
import hashlib
import time
import streamlit as st


class AuthManager:
    """
    Handle user authentication and session management
    """

    def __init__(self):
        self.session_timeout = 3600  # 1 hour in seconds
        self.max_login_attempts = 3
        self.lockout_time = 300  # 5 minutes

    def student_login(self, email: str, first_name: str, last_name: str,
                      student_id: str = "") -> tuple:
        """
        Authenticate student and create session

        Args:
            email: Student email address
            first_name: Student first name
            last_name: Student last name
            student_id: Optional student ID

        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate email format
        if not self._validate_email(email):
            return (False, "Nieprawidłowy format adresu email")

        # Validate required fields
        if not first_name or not last_name:
            return (False, "Imię i nazwisko są wymagane")

        # Check for duplicate test (optional based on config)
        # This will be implemented in Phase 2 with sheets_manager
        # For now, allow all logins

        # Create session
        st.session_state.user_type = "student"
        st.session_state.email = email
        st.session_state.first_name = first_name
        st.session_state.last_name = last_name
        st.session_state.student_id = student_id
        st.session_state.login_time = time.time()

        return (True, "Logowanie pomyślne")

    def teacher_login(self, email: str, password: str) -> tuple:
        """
        Authenticate teacher with credentials

        Args:
            email: Teacher email
            password: Teacher password

        Returns:
            tuple: (success: bool, message: str)
        """
        # Check rate limiting
        if not self._check_rate_limit():
            return (False, "Zbyt wiele prób logowania. Spróbuj ponownie za 5 minut.")

        # Validate email
        if not self._validate_email(email):
            self._record_failed_attempt()
            return (False, "Nieprawidłowy email lub hasło")

        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Verify credentials with sheets_manager
        # (This will be fully integrated in Phase 1)
        from modules.sheets_manager import SheetsManager
        sheets = SheetsManager()

        if sheets.verify_teacher_credentials(email, password_hash):
            # Create session
            st.session_state.user_type = "teacher"
            st.session_state.email = email
            st.session_state.login_time = time.time()
            self._clear_failed_attempts()
            return (True, "Logowanie pomyślne")
        else:
            self._record_failed_attempt()
            return (False, "Nieprawidłowy email lub hasło")

    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated and session is valid

        Returns:
            bool: True if authenticated
        """
        if "user_type" not in st.session_state:
            return False

        # Check session timeout
        if time.time() - st.session_state.login_time > self.session_timeout:
            self.logout()
            return False

        return True

    def require_authentication(self, user_type: str = None):
        """
        Require authentication for page access

        Args:
            user_type: Required user type ("student" or "teacher")
        """
        if not self.is_authenticated():
            st.error("Proszę się zalogować")
            st.stop()

        # Check user type if specified
        if user_type and st.session_state.user_type != user_type:
            st.error("Brak dostępu")
            st.stop()

    def logout(self):
        """Clear session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]

    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _check_rate_limit(self) -> bool:
        """Check if rate limit exceeded"""
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
            st.session_state.lockout_until = None

        # Check if locked out
        if st.session_state.lockout_until:
            if time.time() < st.session_state.lockout_until:
                return False
            else:
                # Lockout expired, reset
                st.session_state.login_attempts = 0
                st.session_state.lockout_until = None

        return st.session_state.login_attempts < self.max_login_attempts

    def _record_failed_attempt(self):
        """Record failed login attempt"""
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0

        st.session_state.login_attempts += 1

        # Apply lockout if max attempts reached
        if st.session_state.login_attempts >= self.max_login_attempts:
            st.session_state.lockout_until = time.time() + self.lockout_time

    def _clear_failed_attempts(self):
        """Clear failed login attempts after successful login"""
        st.session_state.login_attempts = 0
        st.session_state.lockout_until = None
```

### 2.5 Landing Page and Login Pages

**Step 5.1: Create app.py (Landing Page)**

```python
"""
Main landing page for AI Marketing Test Platform
"""

import streamlit as st
from modules.ui_components import load_custom_css, custom_card

# Page configuration
st.set_page_config(
    page_title="AI Marketing Test Platform",
    page_icon="📝",
    layout="centered"
)

# Load custom CSS
load_custom_css()

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

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Jestem Studentem", use_container_width=True):
        st.switch_page("pages/1_Student_Login.py")

with col2:
    if st.button("Jestem Nauczycielem", use_container_width=True):
        st.switch_page("pages/4_Teacher_Login.py")

# Footer
st.markdown("---")
st.markdown("© 2026 AI NETWORK (ARTECH CONSULT)")
```

**Step 5.2: Create pages/1_Student_Login.py**

```python
"""
Student login page
"""

import streamlit as st
from modules.ui_components import load_custom_css
from modules.auth import AuthManager

# Page config
st.set_page_config(
    page_title="Logowanie - Student",
    page_icon="📝",
    layout="centered"
)

load_custom_css()
auth = AuthManager()

# Header
st.markdown("# Logowanie - Student")
st.markdown("## Test Zaliczeniowy - AI w Marketingu")
st.markdown("---")

# Check if already logged in
if auth.is_authenticated() and st.session_state.user_type == "student":
    st.success(f"Zalogowano jako: {st.session_state.first_name} {st.session_state.last_name}")
    if st.button("Rozpocznij Test"):
        st.switch_page("pages/2_Student_Test.py")
    st.stop()

# Login form
with st.form("student_login_form"):
    st.markdown("### Dane studenta")

    email = st.text_input(
        "Email *",
        placeholder="jan.kowalski@example.com",
        help="Adres email, na który otrzymasz wyniki"
    )

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

    submitted = st.form_submit_button("Rozpocznij Test", use_container_width=True)

    if submitted:
        success, message = auth.student_login(email, first_name, last_name, student_id)

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

# Back button
if st.button("← Powrót"):
    st.switch_page("app.py")
```

**Step 5.3: Create pages/4_Teacher_Login.py**

```python
"""
Teacher login page
"""

import streamlit as st
from modules.ui_components import load_custom_css
from modules.auth import AuthManager

# Page config
st.set_page_config(
    page_title="Logowanie - Nauczyciel",
    page_icon="👨‍🏫",
    layout="centered"
)

load_custom_css()
auth = AuthManager()

# Header
st.markdown("# Logowanie - Nauczyciel")
st.markdown("## Dashboard Administracyjny")
st.markdown("---")

# Check if already logged in
if auth.is_authenticated() and st.session_state.user_type == "teacher":
    st.success(f"Zalogowano jako: {st.session_state.email}")
    if st.button("Przejdź do Dashboard"):
        st.switch_page("pages/5_Teacher_Dashboard.py")
    st.stop()

# Login form
with st.form("teacher_login_form"):
    st.markdown("### Dane logowania")

    email = st.text_input(
        "Email *",
        placeholder="tina@example.com"
    )

    password = st.text_input(
        "Hasło *",
        type="password",
        placeholder="••••••••"
    )

    submitted = st.form_submit_button("Zaloguj się", use_container_width=True)

    if submitted:
        success, message = auth.teacher_login(email, password)

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

# Rate limit warning
if 'login_attempts' in st.session_state and st.session_state.login_attempts > 0:
    attempts_left = 3 - st.session_state.login_attempts
    if attempts_left > 0:
        st.warning(f"Pozostałe próby logowania: {attempts_left}/3")

# Back button
if st.button("← Powrót"):
    st.switch_page("app.py")
```

### 2.6 Phase 1 Completion Checklist

**Before ending Phase 1 session:**

- [ ] Project structure created
- [ ] requirements.txt with all dependencies
- [ ] .streamlit/config.toml configured (brutalist theme)
- [ ] Custom CSS fully implemented (NO rounded corners, yellow accents)
- [ ] ui_components.py with reusable components
- [ ] sheets_manager.py with Google Sheets integration + retry logic
- [ ] auth.py with student + teacher authentication
- [ ] app.py landing page functional
- [ ] Student login page functional
- [ ] Teacher login page functional
- [ ] Google Sheets setup with 3 sheets
- [ ] Service account credentials configured
- [ ] Git repository initialized
- [ ] Test student login flow: email → name → session created
- [ ] Test teacher login flow: email + password → dashboard redirect

**Phase 1 Deliverables:**
- Working authentication system (both student and teacher)
- Google Sheets integration with retry logic
- Complete custom CSS (brutalist design)
- All UI components library

**Phase 1 Context Handoff:**
Create `docs/handoffs/SESSION_1_HANDOFF.md` (see Section 6)

---

## 3. PHASE 2: CORE TEST LOGIC

**Goal:** Implement the complete test-taking experience with timer, questions, and scoring

**Duration:** Day 2 (8-10 hours)
**Deliverables:** Working test interface + auto-save + results display

### 3.1 Questions Data

**Step 1.1: Create data/questions.json**

[Content: 27 questions from the final test document]

```json
[
  {
    "number": 1,
    "category": "Podstawy AI",
    "difficulty": "easy",
    "text": "Kiedy warto stosować szczegółowe, strukturalne prompty (np. C.R.E.A.T.E., DELTA)?",
    "options": [
      {"key": "a", "text": "Zawsze, przy każdym zapytaniu do AI"},
      {"key": "b", "text": "Nigdy, nowoczesne modele ich nie potrzebują"},
      {"key": "c", "text": "Gdy proste prompty nie dają oczekiwanych rezultatów lub przy bardzo złożonych, wieloetapowych zadaniach"},
      {"key": "d", "text": "Tylko przy tworzeniu chatbotów i asystentów"}
    ],
    "correct": "c",
    "explanation": "Nowoczesne modele AI (GPT-4o, Claude Sonnet 4.5, Gemini 1.5 Pro) świetnie radzą sobie z prostymi, naturalnymi instrukcjami..."
  }
  // ... Add all 27 questions
]
```

### 3.2 Test Engine Module

**Step 2.1: Create modules/test_engine.py**

[Full implementation with timer, scoring, auto-save]

### 3.3 Student Test Interface

**Step 3.1: Create pages/2_Student_Test.py**

[Full test interface with navigation, timer, progress bar]

### 3.4 Results Display

**Step 4.1: Create pages/3_Student_Results.py**

[Results page with detailed breakdown]

### 3.5 Phase 2 Completion Checklist

[Checklist and handoff document creation]

---

## 4. PHASE 3: NOTIFICATIONS & TEACHER DASHBOARD

[Similar structure for Phase 3]

---

## 5. PHASE 4: POLISH & DEPLOYMENT

[Similar structure for Phase 4]

---

## 6. CONTEXT HANDOFF STRATEGY

### 6.1 Handoff Document Template

**File:** `docs/handoffs/SESSION_X_HANDOFF.md`

```markdown
# SESSION X → SESSION Y HANDOFF

**Date:** YYYY-MM-DD
**Phase Completed:** X
**Next Phase:** Y

## WHAT WAS BUILT

### Files Created:
- module1.py: Description
- module2.py: Description

### Files Modified:
- existing_file.py: What changed

### Key Functions Implemented:
- function_name(): What it does

## WHAT WORKS

### Tested Features:
- [ ] Feature 1: Description of test
- [ ] Feature 2: Description of test

### Known Issues:
- Issue 1: Description + workaround

## NEXT SESSION TASKS

### Priority 1 (Must Complete):
1. Task description
2. Task description

### Priority 2 (Should Complete):
1. Task description

### Files to Read:
- file1.py: Focus on sections X, Y
- file2.py: Understand function Z

### Critical Context:
- Important design decision: Rationale
- Data schema: Key fields and types
- API limits: Rate limits to be aware of

## QUICK START

```bash
# Commands to run next session
cd ai-test-platform
streamlit run app.py
```

### Session State Schema:
```python
# Current session state structure
st.session_state = {...}
```
```

---

## 7. TESTING & VALIDATION

[Testing strategy for each phase]

---

**Document Status:** ✅ READY FOR IMPLEMENTATION
**Next Action:** Begin Phase 1 - Foundation
**Estimated Total Time:** 32-40 hours (4-5 days)
