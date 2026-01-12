# 🏛️ SYSTEM ARCHITECTURE DOCUMENTATION
## AI Marketing Test Platform - Technical Design

**Version:** 2.0 (Enhanced)
**Date:** 2026-01-12
**Status:** Ready for Implementation

---

## TABLE OF CONTENTS

1. [System Overview](#1-system-overview)
2. [Architecture Patterns](#2-architecture-patterns)
3. [Module Design](#3-module-design)
4. [Data Architecture](#4-data-architecture)
5. [Integration Architecture](#5-integration-architecture)
6. [Security Architecture](#6-security-architecture)
7. [Performance Architecture](#7-performance-architecture)
8. [Critical Design Decisions](#8-critical-design-decisions)

---

## 1. SYSTEM OVERVIEW

### 1.1 Business Context

**Purpose:** Automated assessment platform for UKEN postgraduate AI Marketing course
**Primary Users:** 42 students + 1 teacher (Tina)
**Core Value:** Instant grading + comprehensive analytics + zero manual work

### 1.2 System Boundaries

```
┌─────────────────────────────────────────────────────────┐
│                    SYSTEM BOUNDARY                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │         AI MARKETING TEST PLATFORM                  │ │
│  │  ┌──────────────┐        ┌──────────────────────┐ │ │
│  │  │   STUDENT    │        │      TEACHER         │ │ │
│  │  │   INTERFACE  │        │     DASHBOARD        │ │ │
│  │  │  - Login     │        │  - Analytics         │ │ │
│  │  │  - Test      │        │  - Student Reports   │ │ │
│  │  │  - Results   │        │  - Export Data       │ │ │
│  │  └──────────────┘        └──────────────────────┘ │ │
│  │                                                     │ │
│  │  ┌────────────────────────────────────────────────┐│ │
│  │  │         BUSINESS LOGIC LAYER                   ││ │
│  │  │  Auth | TestEngine | Scoring | Analytics      ││ │
│  │  └────────────────────────────────────────────────┘│ │
│  │                                                     │ │
│  │  ┌────────────────────────────────────────────────┐│ │
│  │  │         DATA ACCESS LAYER                      ││ │
│  │  │  SheetsManager | CacheManager                  ││ │
│  │  └────────────────────────────────────────────────┘│ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  EXTERNAL DEPENDENCIES:                                 │
│  - Google Sheets API (data persistence)                 │
│  - Gmail SMTP (notifications)                           │
│  - Streamlit Cloud (hosting)                            │
└──────────────────────────────────────────────────────────┘
```

### 1.3 Technical Constraints

| Constraint | Value | Impact |
|------------|-------|--------|
| **Hosting** | Streamlit Community Cloud | 50 concurrent users, 1GB RAM |
| **Data Store** | Google Sheets API | 60 requests/minute/user |
| **Email** | Gmail SMTP (free) | 500 emails/day |
| **Tech Stack** | Python 3.11 + Streamlit | No backend server, stateless |

---

## 2. ARCHITECTURE PATTERNS

### 2.1 High-Level Architecture

**Pattern:** Three-Layer Architecture + MVC (Model-View-Controller hybrid)

```
┌─────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                      │
│  (Streamlit Pages + Custom UI Components)               │
│                                                          │
│  Student Flow:           Teacher Flow:                   │
│  ├── Login               ├── Login                       │
│  ├── Test Interface      ├── Dashboard                   │
│  └── Results Display     └── Student Details             │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 BUSINESS LOGIC LAYER                     │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ AuthManager  │  │  TestEngine  │  │EmailService  │ │
│  │              │  │              │  │              │ │
│  │ - Login      │  │ - Timer      │  │ - Student    │ │
│  │ - Session    │  │ - Questions  │  │ - Teacher    │ │
│  │ - Validation │  │ - Scoring    │  │ - Templates  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │           AnalyticsEngine                         │  │
│  │  - Statistics | Grade Distribution | Analysis    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  DATA ACCESS LAYER                       │
│                                                          │
│  ┌─────────────────┐        ┌──────────────────────┐   │
│  │ SheetsManager   │        │   CacheManager       │   │
│  │                 │        │                      │   │
│  │ - CRUD Ops      │        │ - @st.cache_data     │   │
│  │ - Batch Writes  │        │ - @st.cache_resource │   │
│  │ - Retry Logic   │        │ - TTL Management     │   │
│  └─────────────────┘        └──────────────────────┘   │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES                           │
│  - Google Sheets (persistence)                          │
│  - Gmail SMTP (notifications)                           │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow Architecture

**Critical Flow: Student Test Completion**

```
[1] Student Login
     ↓ (AuthManager validates + creates session)

[2] Test Start
     ↓ (TestEngine initializes timer + loads questions)

[3] Answer Questions (1-27)
     ↓ (Store in st.session_state.answers)
     ↓ (Auto-save to Sheets every 5 questions) ← NEW FEATURE

[4] Submit Test (manual or auto at 30 min)
     ↓ (TestEngine.calculate_score())

[5] Save to Sheets
     ↓ (SheetsManager.save_test_result())
     ↓ (Includes timestamp, score, details_json)

[6] Send Email Notifications (async)
     ↓ (EmailService → Student + Teacher)

[7] Display Results
     ↓ (Results page with detailed breakdown)
```

### 2.3 Session State Architecture

**Critical:** Streamlit is stateless by default. All state stored in `st.session_state`.

```python
# Student session schema
st.session_state = {
    # Authentication
    'user_type': 'student',
    'email': 'student@example.com',
    'first_name': 'Jan',
    'last_name': 'Kowalski',
    'student_id': '12345',  # optional
    'login_time': 1705234567.89,

    # Test state
    'test_started': True,
    'start_time': 1705234600.00,
    'current_question': 15,
    'answers': {
        '1': 'c',
        '2': 'a',
        # ... up to 27
    },
    'auto_save_checkpoint': 3,  # Last auto-save at question 15

    # Security
    'session_id': 'uuid-string',
    'login_attempts': 0,
    'lockout_until': None
}

# Teacher session schema
st.session_state = {
    'user_type': 'teacher',
    'email': 'tina@example.com',
    'login_time': 1705234567.89,
    'selected_student': 'student@example.com'  # For detail view
}
```

---

## 3. MODULE DESIGN

### 3.1 Module Dependency Graph

```
Level 0 (Foundation - No dependencies):
├── ui_components.py
│   ├── custom_css()
│   ├── custom_button()
│   ├── custom_card()
│   ├── status_badge()
│   └── progress_bar()
│
└── data/questions.json
    └── [27 questions + answer key]

Level 1 (Core Services):
├── auth.py
│   ├── AuthManager
│   │   ├── student_login()
│   │   ├── teacher_login()
│   │   ├── is_authenticated()
│   │   ├── logout()
│   │   └── _validate_email()
│   │
│   └── SessionManager (NEW)
│       ├── create_session()
│       ├── validate_session()
│       └── extend_session()
│
└── sheets_manager.py
    ├── SheetsManager
    │   ├── _authenticate()
    │   ├── save_test_result()
    │   ├── auto_save_progress() ← NEW
    │   ├── get_all_results()
    │   ├── get_student_result()
    │   ├── verify_teacher_credentials()
    │   └── check_duplicate_test() ← ENHANCED
    │
    └── RetryHandler (NEW)
        ├── retry_on_failure()
        └── exponential_backoff()

Level 2 (Business Logic):
├── test_engine.py
│   ├── TestEngine
│   │   ├── _load_questions()
│   │   ├── _load_answer_key()
│   │   ├── start_test()
│   │   ├── get_time_remaining()
│   │   ├── is_time_up()
│   │   ├── save_answer()
│   │   ├── auto_save_checkpoint() ← NEW
│   │   ├── calculate_score()
│   │   ├── _calculate_grade()
│   │   └── validate_all_answered()
│   │
│   └── QuestionManager (NEW)
│       ├── get_question()
│       ├── get_category()
│       └── track_time_spent() ← NEW
│
└── email_service.py
    ├── EmailService
    │   ├── send_student_notification()
    │   ├── send_teacher_notification()
    │   ├── _send_email()
    │   ├── _generate_subject()
    │   ├── _generate_student_email_html()
    │   └── _generate_teacher_email_html()
    │
    └── AsyncEmailQueue (NEW)
        ├── enqueue()
        ├── process_queue()
        └── retry_failed()

Level 3 (Analytics & UI):
├── analytics.py
│   ├── AnalyticsEngine
│   │   ├── get_overview_stats()
│   │   ├── _analyze_questions()
│   │   ├── get_grade_distribution()
│   │   ├── get_timeline_data()
│   │   ├── get_category_breakdown()
│   │   └── identify_difficult_questions() ← NEW
│   │
│   └── CacheManager
│       ├── cache_with_ttl()
│       └── invalidate_cache()
│
└── pages/
    ├── app.py (Landing)
    ├── 1_Student_Login.py
    ├── 2_Student_Test.py
    ├── 3_Student_Results.py
    ├── 4_Teacher_Login.py
    ├── 5_Teacher_Dashboard.py
    └── 6_Teacher_Details.py
```

### 3.2 Critical Module Specifications

#### AuthManager (auth.py)

**Responsibility:** Authentication, session management, security

**Key Methods:**
```python
def student_login(email: str, first_name: str, last_name: str,
                  student_id: str = "") -> tuple[bool, str]:
    """
    Authenticate student and create session

    Returns:
        (success: bool, message: str)
    """

def teacher_login(email: str, password: str) -> tuple[bool, str]:
    """
    Authenticate teacher with credentials

    Implements:
    - Password hashing (SHA256)
    - Rate limiting (3 attempts / 5 min)
    - Session creation

    Returns:
        (success: bool, message: str)
    """

def check_duplicate_test(email: str) -> tuple[bool, dict]:
    """
    Check if student already took test

    Returns:
        (has_taken: bool, test_data: dict)
    """
```

**Security Features:**
- Email format validation (regex)
- Password strength check (min 8 chars)
- Rate limiting for login attempts
- Session timeout (60 minutes)
- Duplicate test prevention

#### TestEngine (test_engine.py)

**Responsibility:** Test orchestration, timer, scoring

**Key Methods:**
```python
def start_test() -> None:
    """Initialize test with timer and empty answers"""

def get_time_remaining() -> int:
    """Get remaining seconds, handles refresh edge case"""

def save_answer(question_num: int, answer: str) -> None:
    """Save answer + trigger auto-save if needed"""

def auto_save_checkpoint() -> bool:
    """
    Auto-save progress to Sheets every 5 questions

    Prevents data loss on connection failure
    Returns: success status
    """

def calculate_score() -> dict:
    """
    Calculate final score with full breakdown

    Returns:
        {
            'correct_count': int,
            'total_questions': 27,
            'percentage': int,
            'grade': float,
            'grade_text': str,
            'passed': bool,
            'time_spent_seconds': int,
            'details': dict,  # per-question breakdown
            'category_breakdown': dict  # performance by category
        }
    """
```

**Critical Logic:**
```python
# Grade calculation (from PRD)
def _calculate_grade(correct_count: int) -> tuple:
    """
    Official grading scale for UKEN

    Pass threshold: 48% (13/27 questions)
    """
    if correct_count >= 25:    # 93%
        return (5.0, "Bardzo dobra", True)
    elif correct_count >= 22:  # 81%
        return (4.5, "Dobra plus", True)
    elif correct_count >= 19:  # 70%
        return (4.0, "Dobra", True)
    elif correct_count >= 16:  # 59%
        return (3.5, "Dostateczna plus", True)
    elif correct_count >= 13:  # 48% ← PASS THRESHOLD
        return (3.0, "Dostateczna", True)
    else:
        return (2.0, "Niedostateczna", False)
```

---

## 4. DATA ARCHITECTURE

### 4.1 Google Sheets Schema (Enhanced)

#### Sheet 1: "Wyniki_Testow"

```
Column A: Timestamp (ISO 8601: 2026-01-12T15:30:45Z)
Column B: Email (string, primary identifier)
Column C: First_Name (string)
Column D: Last_Name (string)
Column E: Student_ID (string, optional)
Column F: Correct_Count (integer, 0-27)
Column G: Percentage (integer, 0-100)
Column H: Grade (float, 2.0-5.0)
Column I: Grade_Text (string: "Bardzo dobra" | "Dobra plus" | ...)
Column J: Status (string: "ZALICZONY" | "NIEZALICZONY")
Column K: Time_Spent_Minutes (float)
Column L: Details_JSON (JSON string, see schema below)
Column M: Test_Version (string, e.g., "v1.0") ← NEW
Column N: Browser_Info (string, e.g., "Chrome 120") ← NEW
Column O: Attempt_Number (integer, e.g., 1, 2) ← NEW
Column P: Auto_Submitted (boolean, true if time expired) ← NEW
```

#### Details_JSON Schema (Enhanced)

```json
{
  "answers": {
    "1": {
      "selected": "c",
      "correct": "c",
      "is_correct": true,
      "time_spent_seconds": 45,
      "category": "Podstawy AI"
    },
    "2": {
      "selected": "a",
      "correct": "a",
      "is_correct": true,
      "time_spent_seconds": 32,
      "category": "Podstawy AI"
    }
    // ... questions 3-27
  },
  "category_breakdown": {
    "Podstawy AI": {
      "correct": 4,
      "total": 5,
      "percentage": 80,
      "questions": [1, 2, 3, 4, 5]
    },
    "Modele LLM": {
      "correct": 3,
      "total": 5,
      "percentage": 60,
      "questions": [6, 7, 8, 9, 10]
    },
    "Strategia": {
      "correct": 5,
      "total": 5,
      "percentage": 100,
      "questions": [11, 12, 13, 14, 15]
    },
    "Nowa era": {
      "correct": 4,
      "total": 5,
      "percentage": 80,
      "questions": [16, 17, 18, 19, 20]
    },
    "Zaawansowane": {
      "correct": 6,
      "total": 7,
      "percentage": 86,
      "questions": [21, 22, 23, 24, 25, 26, 27]
    }
  },
  "metadata": {
    "test_version": "v1.0",
    "browser": "Chrome 120.0.6099.224",
    "os": "Windows 11",
    "start_time": "2026-01-12T15:00:00Z",
    "end_time": "2026-01-12T15:27:15Z",
    "auto_submitted": false,
    "auto_saves": [
      {"checkpoint": 5, "timestamp": "2026-01-12T15:08:30Z"},
      {"checkpoint": 10, "timestamp": "2026-01-12T15:15:45Z"},
      {"checkpoint": 15, "timestamp": "2026-01-12T15:20:12Z"}
    ]
  }
}
```

#### Sheet 2: "Teachers"

```
Column A: Email (string, unique)
Column B: Password_Hash (SHA256 string)
Column C: First_Name (string)
Column D: Last_Name (string)
Column E: Role (string: "admin")
Column F: Last_Login (ISO datetime) ← NEW
Column G: Login_Count (integer) ← NEW
```

#### Sheet 3: "Config" (NEW - System Configuration)

```
Column A: Key (string, unique)
Column B: Value (string)
Column C: Description (string)
Column D: Last_Updated (ISO datetime)

Rows:
- "pass_threshold", "13", "Minimum correct answers to pass", "2026-01-12T10:00:00Z"
- "time_limit_minutes", "30", "Test time limit", "2026-01-12T10:00:00Z"
- "allow_retakes", "true", "Allow students to retake test", "2026-01-12T10:00:00Z"
- "max_attempts", "2", "Maximum test attempts per student", "2026-01-12T10:00:00Z"
- "auto_save_interval", "5", "Auto-save every N questions", "2026-01-12T10:00:00Z"
- "test_version", "v1.0", "Current test version", "2026-01-12T10:00:00Z"
```

### 4.2 Questions Data Structure

**File:** `data/questions.json`

```json
[
  {
    "number": 1,
    "category": "Podstawy AI",
    "difficulty": "easy",
    "text": "Kiedy warto stosować szczegółowe, strukturalne prompty (np. C.R.E.A.T.E., DELTA)?",
    "options": [
      {
        "key": "a",
        "text": "Zawsze, przy każdym zapytaniu do AI"
      },
      {
        "key": "b",
        "text": "Nigdy, nowoczesne modele ich nie potrzebują"
      },
      {
        "key": "c",
        "text": "Gdy proste prompty nie dają oczekiwanych rezultatów lub przy bardzo złożonych, wieloetapowych zadaniach"
      },
      {
        "key": "d",
        "text": "Tylko przy tworzeniu chatbotów i asystentów"
      }
    ],
    "correct": "c",
    "explanation": "Nowoczesne modele AI (GPT-4o, Claude Sonnet 4.5, Gemini 1.5 Pro) świetnie radzą sobie z prostymi, naturalnymi instrukcjami. Szczegółowe frameworki są potrzebne tylko dla zadań, gdzie prosty prompt zawodzi."
  }
  // ... questions 2-27
]
```

---

## 5. INTEGRATION ARCHITECTURE

### 5.1 Google Sheets API Integration

**Authentication:** OAuth2 Service Account

```python
# Credentials structure (stored in secrets.toml)
{
  "type": "service_account",
  "project_id": "ai-test-platform",
  "private_key_id": "xxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n",
  "client_email": "test-platform@ai-test-platform.iam.gserviceaccount.com",
  "client_id": "xxx",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

**Rate Limit Handling:**

```python
@retry_on_failure(max_attempts=3, delay=2, backoff=exponential)
def save_to_sheets(data):
    """
    Retry logic with exponential backoff

    Attempt 1: Immediate
    Attempt 2: 2s delay
    Attempt 3: 4s delay

    If all fail → save to local cache + log error
    """
```

**Batch Operations:**

```python
# Instead of 27 individual writes (1 per question)
# Use batch write for all answers at once
worksheet.batch_update([{
    'range': 'A2:P2',
    'values': [[row_data]]
}])
```

### 5.2 Gmail SMTP Integration

**Configuration:**

```python
SMTP_CONFIG = {
    'server': 'smtp.gmail.com',
    'port': 587,
    'use_tls': True,
    'email': 'notifications@ainetwork.pl',
    'password': 'xxxx xxxx xxxx xxxx'  # App-specific password
}
```

**Email Sending Architecture:**

```python
# Async email sending (non-blocking)
def send_emails_async(student_data, results):
    """
    Send emails in background thread
    Test completion is NOT blocked by email delivery
    """
    def _send():
        try:
            email_service.send_student_notification(student_data, results)
            email_service.send_teacher_notification(student_data, results)
        except Exception as e:
            logger.error(f"Email failed: {e}")
            # Store in retry queue

    thread = threading.Thread(target=_send, daemon=True)
    thread.start()
```

**Rate Limit Management:**

- Gmail free tier: 500 emails/day
- Expected usage: 42 students × 2 emails = 84 emails per test session
- Buffer: 416 emails remaining (plenty for multiple test sessions)

---

## 6. SECURITY ARCHITECTURE

### 6.1 Authentication Flow

```
Student Login:
┌──────────────────────────────────────────────────────────┐
│ 1. Enter email + name + student_id                       │
│    ↓                                                      │
│ 2. Validate email format (regex)                         │
│    ↓                                                      │
│ 3. Check duplicate test (query Sheets)                   │
│    ↓                                                      │
│ 4. Create session (st.session_state)                     │
│    ↓                                                      │
│ 5. Redirect to test interface                            │
└──────────────────────────────────────────────────────────┘

Teacher Login:
┌──────────────────────────────────────────────────────────┐
│ 1. Enter email + password                                │
│    ↓                                                      │
│ 2. Hash password (SHA256)                                │
│    ↓                                                      │
│ 3. Query Sheets for matching email + hash                │
│    ↓                                                      │
│ 4. Check rate limit (3 attempts / 5 min)                 │
│    ↓                                                      │
│ 5. Create session (st.session_state)                     │
│    ↓                                                      │
│ 6. Redirect to dashboard                                 │
└──────────────────────────────────────────────────────────┘
```

### 6.2 Session Management

```python
# Session validation on every page
def require_authentication(user_type: str = None):
    """
    Decorator to protect pages

    Usage:
        @require_authentication("teacher")
        def teacher_dashboard():
            ...
    """
    if 'user_type' not in st.session_state:
        st.error("Please log in first")
        st.stop()

    # Check session timeout (60 min)
    if time.time() - st.session_state.login_time > 3600:
        st.error("Session expired")
        logout()
        st.stop()

    # Check user type
    if user_type and st.session_state.user_type != user_type:
        st.error("Access denied")
        st.stop()
```

### 6.3 Data Privacy (GDPR/RODO)

**Compliance Checklist:**

- [x] Data minimization: Only collect necessary fields
- [x] Consent: Privacy policy link on login page
- [x] Right to access: Teacher can view all student data
- [x] Right to deletion: `delete_student_data(email)` function
- [x] Data portability: CSV export functionality
- [x] Data location: Google Sheets in EU region
- [x] Data retention: Until course completion + 1 year

**Anonymization Function:**

```python
def anonymize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove PII for analytics/research"""
    df['Email'] = df['Email'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest()[:8])
    df['First_Name'] = 'XXXXX'
    df['Last_Name'] = 'XXXXX'
    df['Student_ID'] = ''
    return df
```

---

## 7. PERFORMANCE ARCHITECTURE

### 7.1 Caching Strategy

```python
# Level 1: Static data (questions)
@st.cache_data
def load_questions():
    """Cache forever - questions never change"""
    return json.load(open('data/questions.json'))

# Level 2: Resource connections
@st.cache_resource
def get_sheets_client():
    """Reuse Sheets API connection"""
    return SheetsManager()

# Level 3: Dynamic data with TTL
@st.cache_data(ttl=60)  # 1 minute cache
def load_all_results():
    """Teacher dashboard data - short TTL for freshness"""
    return sheets_manager.get_all_results()

# Level 4: Expensive computations
@st.cache_data(ttl=300)  # 5 minute cache
def calculate_dashboard_stats(df_hash):
    """Analytics calculations - longer TTL for performance"""
    return analytics_engine.get_overview_stats()
```

### 7.2 Performance Optimizations

**1. Lazy Loading:**
```python
# Don't load Details_JSON by default
# Only parse on demand (student detail view)

def get_student_details(email: str):
    """Load only when viewing specific student"""
    result = sheets_manager.get_student_result(email)
    details = json.loads(result['Details_JSON'])
    return details
```

**2. Pagination:**
```python
# Teacher dashboard: Show 20 students per page
# Prevents slow load with 100+ students

def display_student_list(df: pd.DataFrame, page: int = 1, per_page: int = 20):
    start = (page - 1) * per_page
    end = start + per_page
    return df[start:end]
```

**3. Background Processing:**
```python
# Email sending doesn't block test completion
# Analytics calculations run in background

@st.cache_data(show_spinner=False)
def calculate_expensive_stats():
    """Run in background while showing loading spinner"""
    return heavy_computation()
```

---

## 8. CRITICAL DESIGN DECISIONS

### 8.1 Questions Storage: JSON vs Sheets

**Decision:** Use `data/questions.json` (Option A) for MVP

**Rationale:**
- ✅ Zero API calls during test (faster)
- ✅ Simple implementation
- ✅ Questions unlikely to change during course
- ⚠️ Answer key visible in repo → use private GitHub repo

**Future (v2.0):** Migrate to Google Sheets with encrypted answers

### 8.2 Auto-Save Strategy

**Decision:** Auto-save to Sheets every 5 questions (Option B)

**Rationale:**
- ✅ Prevents data loss on connection failure (critical for 30-min test)
- ✅ Can resume test after refresh
- ✅ Only 5-6 extra API calls per test (acceptable)
- ⚠️ Adds complexity to recovery logic

**Implementation:**
```python
def save_answer(question_num: int, answer: str):
    st.session_state.answers[question_num] = answer

    # Auto-save every 5 questions
    if question_num % 5 == 0:
        auto_save_progress()
```

### 8.3 Duplicate Test Prevention

**Decision:** Email + Name matching with configurable retry policy (Option B)

**Rationale:**
- ✅ Balance between security and usability
- ✅ Allows legitimate retakes (teacher can configure)
- ✅ Prevents accidental duplicate submissions
- ⚠️ Not foolproof (student can use different email)

**Implementation:**
```python
def check_duplicate_test(email: str) -> tuple[bool, int]:
    """
    Returns:
        (already_taken: bool, attempt_number: int)
    """
    df = load_all_results()
    existing = df[df['Email'] == email]

    if len(existing) > 0:
        max_attempts = get_config('max_attempts', default=2)
        if len(existing) >= max_attempts:
            return (True, len(existing))

    return (False, len(existing))
```

### 8.4 Email Sending: Blocking vs Async

**Decision:** Async/background email sending (Option B)

**Rationale:**
- ✅ Test completion not blocked by slow email delivery
- ✅ Better user experience (instant results)
- ✅ Email failures don't affect test data
- ⚠️ Need error handling + retry queue

**Implementation:**
```python
# Non-blocking email
thread = threading.Thread(
    target=send_emails_background,
    args=(student_data, results),
    daemon=True
)
thread.start()

# Test completion continues immediately
display_results(results)
```

---

## ARCHITECTURE STATUS

**Readiness:** ✅ PRODUCTION-READY
**Risk Level:** 🟢 LOW
**Complexity:** 🟡 MEDIUM
**Scalability:** ✅ SUFFICIENT (42 users << 50 limit)
**Maintainability:** ✅ EXCELLENT (modular, documented)

**Next Steps:** Implementation Phase 1 (Foundation)

---

**Document Version:** 2.0
**Last Updated:** 2026-01-12
**Review Date:** After MVP completion
