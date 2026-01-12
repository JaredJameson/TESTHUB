# 🏗️ SOFTWARE DESIGN DOCUMENT (SOD)
## AI Marketing Test Platform - Technical Architecture

**Version:** 1.0  
**Date:** 2026-01-12  
**Project:** AI Marketing Test Platform  
**Owner:** AI NETWORK (ARTECH CONSULT)

---

## TABLE OF CONTENTS

1. [System Overview](#1-system-overview)
2. [Architecture Design](#2-architecture-design)
3. [Technology Stack](#3-technology-stack)
4. [Component Design](#4-component-design)
5. [Data Architecture](#5-data-architecture)
6. [Security Design](#6-security-design)
7. [Integration Design](#7-integration-design)
8. [Deployment Architecture](#8-deployment-architecture)
9. [Error Handling & Logging](#9-error-handling--logging)
10. [Performance Optimization](#10-performance-optimization)

---

## 1. SYSTEM OVERVIEW

### 1.1 Purpose
Automated test platform for UKEN postgraduate students in AI Marketing course, enabling instant grading, result delivery, and teacher analytics dashboard.

### 1.2 Scope
- Student test interface with 27 multiple-choice questions
- 30-minute timer with auto-submit
- Instant scoring and detailed feedback
- Teacher dashboard with analytics
- Email notifications
- Google Sheets persistence

### 1.3 Constraints
- Streamlit Community Cloud: 50 concurrent users max
- Google Sheets API: 60 requests/minute per user
- Gmail SMTP: 500 emails/day limit
- No database server (using Google Sheets as DB)

---

## 2. ARCHITECTURE DESIGN

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                        │
│              (Student / Teacher Interface)               │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│              STREAMLIT APPLICATION                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │            PRESENTATION LAYER                      │  │
│  │  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │ Student Pages│  │ Teacher Pages│              │  │
│  │  │  - Login     │  │  - Dashboard │              │  │
│  │  │  - Test      │  │  - Analytics │              │  │
│  │  │  - Results   │  │  - Details   │              │  │
│  │  └──────────────┘  └──────────────┘              │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │            BUSINESS LOGIC LAYER                    │  │
│  │  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │Auth Manager  │  │Test Engine   │              │  │
│  │  │Timer Service │  │Score Calculator│             │  │
│  │  │Email Service │  │Analytics Engine│            │  │
│  │  └──────────────┘  └──────────────┘              │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │            DATA ACCESS LAYER                       │  │
│  │  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │Sheets Manager│  │Cache Manager │              │  │
│  │  └──────────────┘  └──────────────┘              │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│  GOOGLE SHEETS  │    │   GMAIL SMTP     │
│   (Database)    │    │  (Notifications) │
└─────────────────┘    └──────────────────┘
```

### 2.2 Application Flow

```
STUDENT FLOW:
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│ Login  │ -> │  Test  │ -> │ Submit │ -> │ Score  │ -> │Results │
│ Page   │    │ (27Q)  │    │        │    │ Calc   │    │ Display│
└────────┘    └────────┘    └────────┘    └────────┘    └────────┘
                  │                             │
                  └──── Timer (30min) ─────────┘
                  │                             │
                  └──── Save to Sheets ─────────┘
                  │                             │
                  └──── Send Emails ────────────┘

TEACHER FLOW:
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│ Login  │ -> │Dashboard│ -> │Student │ -> │Export  │
│ Page   │    │Overview │    │Details │    │CSV     │
└────────┘    └────────┘    └────────┘    └────────┘
                  │
                  └──── Load from Sheets
                  │
                  └──── Calculate Stats
```

---

## 3. TECHNOLOGY STACK

### 3.1 Core Framework
```yaml
Framework: Streamlit 1.30+
Language: Python 3.11+
Deployment: Streamlit Community Cloud
```

### 3.2 Dependencies
```python
# requirements.txt
streamlit==1.30.0
gspread==5.12.0
oauth2client==4.1.3
pandas==2.1.4
plotly==5.18.0
python-dotenv==1.0.0
Pillow==10.1.0
```

### 3.3 External Services
- **Google Sheets API** (v4) - Data persistence
- **Gmail SMTP** (smtp.gmail.com:587) - Email notifications
- **Streamlit Cloud** - Hosting & deployment

---

## 4. COMPONENT DESIGN

### 4.1 Project Structure

```
ai-test-platform/
├── .streamlit/
│   └── config.toml              # Streamlit config
├── assets/
│   ├── logo.png                 # AI NETWORK logo
│   └── styles.css               # Custom CSS
├── modules/
│   ├── __init__.py
│   ├── auth.py                  # Authentication logic
│   ├── test_engine.py           # Test logic & scoring
│   ├── sheets_manager.py        # Google Sheets interface
│   ├── email_service.py         # Email notifications
│   ├── analytics.py             # Dashboard analytics
│   └── ui_components.py         # Reusable UI components
├── pages/
│   ├── 1_Student_Login.py       # Student entry point
│   ├── 2_Student_Test.py        # Test interface
│   ├── 3_Student_Results.py     # Results display
│   ├── 4_Teacher_Login.py       # Teacher entry point
│   ├── 5_Teacher_Dashboard.py   # Main dashboard
│   └── 6_Teacher_Details.py     # Student detail view
├── data/
│   ├── questions.json           # Test questions & answers
│   └── test_config.json         # Test configuration
├── tests/
│   ├── test_auth.py
│   ├── test_scoring.py
│   └── test_sheets.py
├── .env.example                 # Environment variables template
├── .gitignore
├── requirements.txt
├── app.py                       # Main entry point (landing page)
└── README.md
```

### 4.2 Core Modules

#### 4.2.1 Authentication Module (`auth.py`)

```python
"""
Authentication and session management
"""

class AuthManager:
    """Handle user authentication and session state"""
    
    def __init__(self):
        self.session_timeout = 3600  # 1 hour in seconds
        
    def student_login(self, email: str, first_name: str, 
                     last_name: str, student_id: str = "") -> bool:
        """
        Authenticate student and create session
        
        Args:
            email: Student email address
            first_name: Student first name
            last_name: Student last name
            student_id: Optional student ID
            
        Returns:
            bool: True if login successful
        """
        # Validate email format
        if not self._validate_email(email):
            return False
            
        # Check for duplicate test (optional)
        if self._check_duplicate_test(email):
            return False
            
        # Create session
        st.session_state.user_type = "student"
        st.session_state.email = email
        st.session_state.first_name = first_name
        st.session_state.last_name = last_name
        st.session_state.student_id = student_id
        st.session_state.login_time = time.time()
        
        return True
    
    def teacher_login(self, email: str, password: str) -> bool:
        """
        Authenticate teacher with credentials
        
        Args:
            email: Teacher email
            password: Teacher password
            
        Returns:
            bool: True if credentials valid
        """
        # Load teacher credentials from Sheets or config
        credentials = self._load_teacher_credentials()
        
        # Hash password and compare
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if email in credentials and credentials[email] == password_hash:
            st.session_state.user_type = "teacher"
            st.session_state.email = email
            st.session_state.login_time = time.time()
            return True
            
        return False
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated and session valid"""
        if "user_type" not in st.session_state:
            return False
            
        # Check session timeout
        if time.time() - st.session_state.login_time > self.session_timeout:
            self.logout()
            return False
            
        return True
    
    def logout(self):
        """Clear session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _check_duplicate_test(self, email: str) -> bool:
        """Check if student already completed test"""
        # Query Google Sheets for existing test
        # Return True if found, False otherwise
        pass
    
    def _load_teacher_credentials(self) -> dict:
        """Load teacher credentials from secure storage"""
        # Load from environment variables or Sheets
        pass
```

#### 4.2.2 Test Engine (`test_engine.py`)

```python
"""
Test logic, timer, and scoring engine
"""

class TestEngine:
    """Manage test execution and scoring"""
    
    def __init__(self):
        self.questions = self._load_questions()
        self.correct_answers = self._load_answer_key()
        self.time_limit_seconds = 1800  # 30 minutes
        
    def _load_questions(self) -> list:
        """Load questions from JSON file"""
        with open('data/questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_answer_key(self) -> dict:
        """Load correct answers"""
        return {
            "1": "c", "2": "a", "3": "a", "4": "c", "5": "b",
            "6": "d", "7": "c", "8": "a", "9": "d", "10": "c",
            "11": "c", "12": "d", "13": "c", "14": "a", "15": "b",
            "16": "b", "17": "b", "18": "a", "19": "b", "20": "b",
            "21": "d", "22": "a", "23": "c", "24": "d", "25": "a",
            "26": "d", "27": "c"
        }
    
    def start_test(self):
        """Initialize test session"""
        st.session_state.test_started = True
        st.session_state.start_time = time.time()
        st.session_state.answers = {}
        st.session_state.current_question = 1
    
    def get_time_remaining(self) -> int:
        """Get remaining time in seconds"""
        elapsed = time.time() - st.session_state.start_time
        remaining = self.time_limit_seconds - elapsed
        return max(0, int(remaining))
    
    def is_time_up(self) -> bool:
        """Check if time limit exceeded"""
        return self.get_time_remaining() <= 0
    
    def save_answer(self, question_num: int, answer: str):
        """Save student answer"""
        st.session_state.answers[str(question_num)] = answer
    
    def calculate_score(self) -> dict:
        """
        Calculate test score and generate detailed results
        
        Returns:
            dict: {
                'correct_count': int,
                'total_questions': int,
                'percentage': int,
                'grade': float,
                'grade_text': str,
                'passed': bool,
                'time_spent_seconds': int,
                'details': dict  # per-question breakdown
            }
        """
        answers = st.session_state.answers
        correct_count = 0
        details = {}
        
        for q_num in range(1, 28):
            q_str = str(q_num)
            student_answer = answers.get(q_str, "")
            correct_answer = self.correct_answers[q_str]
            is_correct = student_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            details[q_str] = {
                'student_answer': student_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'question_text': self.questions[q_num - 1]['text']
            }
        
        percentage = round((correct_count / 27) * 100)
        grade, grade_text, passed = self._calculate_grade(correct_count)
        
        time_spent = int(time.time() - st.session_state.start_time)
        
        return {
            'correct_count': correct_count,
            'total_questions': 27,
            'percentage': percentage,
            'grade': grade,
            'grade_text': grade_text,
            'passed': passed,
            'time_spent_seconds': time_spent,
            'details': details
        }
    
    @staticmethod
    def _calculate_grade(correct_count: int) -> tuple:
        """
        Calculate grade based on correct answers
        
        Returns:
            tuple: (grade, grade_text, passed)
        """
        if correct_count >= 25:
            return (5.0, "Bardzo dobra", True)
        elif correct_count >= 22:
            return (4.5, "Dobra plus", True)
        elif correct_count >= 19:
            return (4.0, "Dobra", True)
        elif correct_count >= 16:
            return (3.5, "Dostateczna plus", True)
        elif correct_count >= 13:
            return (3.0, "Dostateczna", True)
        else:
            return (2.0, "Niedostateczna", False)
    
    def validate_all_answered(self) -> bool:
        """Check if all 27 questions have answers"""
        return len(st.session_state.answers) == 27
```

#### 4.2.3 Google Sheets Manager (`sheets_manager.py`)

```python
"""
Google Sheets integration for data persistence
"""

class SheetsManager:
    """Handle all Google Sheets operations"""
    
    def __init__(self):
        self.client = self._authenticate()
        self.sheet_id = os.getenv('GOOGLE_SHEETS_ID')
        self.workbook = self.client.open_by_key(self.sheet_id)
        
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Load credentials from environment
        creds_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        creds_dict = json.loads(creds_json)
        
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict, scope
        )
        
        return gspread.authorize(credentials)
    
    def save_test_result(self, result_data: dict) -> bool:
        """
        Save test result to Google Sheets
        
        Args:
            result_data: Dictionary with test results
            
        Returns:
            bool: True if successful
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
                f"{result_data['percentage']}%",
                result_data['grade'],
                result_data['grade_text'],
                "ZALICZONY" if result_data['passed'] else "NIEZALICZONY",
                round(result_data['time_spent_seconds'] / 60, 1),
                json.dumps(result_data['details'])
            ]
            
            worksheet.append_row(row)
            return True
            
        except Exception as e:
            print(f"Error saving to Sheets: {e}")
            return False
    
    def get_all_results(self) -> pd.DataFrame:
        """
        Retrieve all test results
        
        Returns:
            pd.DataFrame: All test results
        """
        try:
            worksheet = self.workbook.worksheet("Wyniki_Testow")
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
                return student_data.iloc[0].to_dict()
            return None
            
        except Exception as e:
            print(f"Error finding student: {e}")
            return None
    
    def verify_teacher_credentials(self, email: str, 
                                   password_hash: str) -> bool:
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
                    return True
            return False
            
        except Exception as e:
            print(f"Error verifying teacher: {e}")
            return False
```

#### 4.2.4 Email Service (`email_service.py`)

```python
"""
Email notification service
"""

class EmailService:
    """Send email notifications via SMTP"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.smtp_email = os.getenv('SMTP_EMAIL')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.teacher_email = os.getenv('TEACHER_EMAIL')
        
    def send_student_notification(self, student_data: dict, 
                                  results: dict) -> bool:
        """
        Send test results to student
        
        Args:
            student_data: Student information
            results: Test results
            
        Returns:
            bool: True if email sent successfully
        """
        subject = self._generate_subject(results['passed'])
        html_body = self._generate_student_email_html(student_data, results)
        
        return self._send_email(
            to_email=student_data['email'],
            subject=subject,
            html_body=html_body
        )
    
    def send_teacher_notification(self, student_data: dict, 
                                  results: dict) -> bool:
        """
        Send notification to teacher about new test submission
        
        Args:
            student_data: Student information
            results: Test results
            
        Returns:
            bool: True if email sent successfully
        """
        subject = f"Nowy test: {student_data['first_name']} {student_data['last_name']}"
        html_body = self._generate_teacher_email_html(student_data, results)
        
        return self._send_email(
            to_email=self.teacher_email,
            subject=subject,
            html_body=html_body
        )
    
    def _send_email(self, to_email: str, subject: str, 
                   html_body: str) -> bool:
        """
        Send email via SMTP
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_body: HTML email body
            
        Returns:
            bool: Success status
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_email
            msg['To'] = to_email
            
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_email, self.smtp_password)
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    @staticmethod
    def _generate_subject(passed: bool) -> str:
        """Generate email subject based on test result"""
        if passed:
            return "Test zaliczony - AI w Marketingu UKEN"
        else:
            return "Test niezaliczony - AI w Marketingu UKEN"
    
    def _generate_student_email_html(self, student_data: dict, 
                                    results: dict) -> str:
        """Generate HTML email for student"""
        # Implementation: HTML template with results
        pass
    
    def _generate_teacher_email_html(self, student_data: dict, 
                                    results: dict) -> str:
        """Generate HTML email for teacher"""
        # Implementation: Simple notification template
        pass
```

#### 4.2.5 Analytics Engine (`analytics.py`)

```python
"""
Dashboard analytics and statistics
"""

class AnalyticsEngine:
    """Calculate dashboard statistics and metrics"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def get_overview_stats(self) -> dict:
        """
        Calculate overview statistics for dashboard
        
        Returns:
            dict: {
                'total_students': int,
                'passed_count': int,
                'average_grade': float,
                'pass_rate': float,
                'average_score': float,
                'hardest_question': int,
                'easiest_question': int
            }
        """
        total = len(self.df)
        passed = len(self.df[self.df['Status'] == 'ZALICZONY'])
        avg_grade = self.df['Ocena'].mean()
        pass_rate = (passed / total * 100) if total > 0 else 0
        avg_score = self.df['Poprawne'].mean()
        
        # Calculate hardest/easiest questions
        hardest, easiest = self._analyze_questions()
        
        return {
            'total_students': total,
            'passed_count': passed,
            'average_grade': round(avg_grade, 2),
            'pass_rate': round(pass_rate, 1),
            'average_score': round(avg_score, 1),
            'hardest_question': hardest,
            'easiest_question': easiest
        }
    
    def _analyze_questions(self) -> tuple:
        """
        Analyze which questions are hardest/easiest
        
        Returns:
            tuple: (hardest_question_num, easiest_question_num)
        """
        # Parse JSON details from all tests
        # Count correct answers per question
        # Return question numbers with lowest/highest success rate
        pass
    
    def get_grade_distribution(self) -> dict:
        """Get distribution of grades for histogram"""
        return self.df['Ocena'].value_counts().to_dict()
    
    def get_timeline_data(self) -> pd.DataFrame:
        """Get test submissions over time"""
        self.df['Date'] = pd.to_datetime(self.df['Timestamp']).dt.date
        timeline = self.df.groupby('Date').size().reset_index(name='Count')
        return timeline
    
    def get_category_breakdown(self, details_json: str) -> dict:
        """
        Calculate performance by test category
        
        Args:
            details_json: JSON string with detailed results
            
        Returns:
            dict: Performance by category
        """
        details = json.loads(details_json)
        
        # Categories defined by question ranges
        categories = {
            'Podstawy AI': (1, 5),
            'Modele LLM': (6, 10),
            'Strategia': (11, 15),
            'Nowa era': (16, 20),
            'Zaawansowane': (21, 27)
        }
        
        category_scores = {}
        
        for cat_name, (start, end) in categories.items():
            correct = sum(
                1 for q in range(start, end + 1) 
                if details[str(q)]['is_correct']
            )
            total = end - start + 1
            percentage = round((correct / total) * 100)
            
            category_scores[cat_name] = {
                'correct': correct,
                'total': total,
                'percentage': percentage
            }
        
        return category_scores
```

---

## 5. DATA ARCHITECTURE

### 5.1 Google Sheets Schema

#### Sheet 1: "Wyniki_Testow"
```
Column A: Timestamp (ISO datetime string)
Column B: Email (string)
Column C: First_Name (string)
Column D: Last_Name (string)
Column E: Student_ID (string, optional)
Column F: Correct_Count (integer, 0-27)
Column G: Percentage (string, "XX%")
Column H: Grade (float, 2.0-5.0)
Column I: Grade_Text (string)
Column J: Status (string, "ZALICZONY"/"NIEZALICZONY")
Column K: Time_Spent_Minutes (float)
Column L: Details_JSON (JSON string)
```

**Details_JSON Structure:**
```json
{
  "1": {
    "student_answer": "c",
    "correct_answer": "c",
    "is_correct": true,
    "question_text": "Kiedy warto stosować..."
  },
  "2": { ... },
  ...
  "27": { ... }
}
```

#### Sheet 2: "Teachers"
```
Column A: Email (string)
Column B: Password_Hash (SHA256 string)
Column C: First_Name (string)
Column D: Last_Name (string)
Column E: Role (string, "admin")
```

### 5.2 Session State Schema

```python
# Student session
st.session_state = {
    'user_type': 'student',
    'email': 'anna.k@example.com',
    'first_name': 'Anna',
    'last_name': 'Kowalska',
    'student_id': '12345',
    'login_time': 1705234567.89,
    'test_started': True,
    'start_time': 1705234600.00,
    'current_question': 15,
    'answers': {
        '1': 'c',
        '2': 'a',
        # ... up to 27
    }
}

# Teacher session
st.session_state = {
    'user_type': 'teacher',
    'email': 'tina@example.com',
    'login_time': 1705234567.89,
    'selected_student': 'anna.k@example.com'  # For detail view
}
```

### 5.3 Questions Data Structure

**File:** `data/questions.json`

```json
[
  {
    "number": 1,
    "category": "Podstawy AI",
    "text": "Kiedy warto stosować szczegółowe, strukturalne prompty (np. C.R.E.A.T.E., DELTA)?",
    "options": [
      "a) Zawsze, przy każdym zapytaniu do AI",
      "b) Nigdy, nowoczesne modele ich nie potrzebują",
      "c) Gdy proste prompty nie dają oczekiwanych rezultatów lub przy bardzo złożonych, wieloetapowych zadaniach",
      "d) Tylko przy tworzeniu chatbotów i asystentów"
    ],
    "correct": "c",
    "explanation": "Nowoczesne modele AI (GPT-4o, Claude Sonnet 4.5, Gemini 1.5 Pro) świetnie radzą sobie z prostymi, naturalnymi instrukcjami..."
  },
  // ... questions 2-27
]
```

---

## 6. SECURITY DESIGN

### 6.1 Authentication & Authorization

```python
# Password hashing
import hashlib

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Teacher credentials stored as hashes in Google Sheets
# Example:
# Email: tina@example.com
# Password: "uken2026"
# Stored hash: "3fc9b689459d738f8c88a3a48aa9e33542016b7a4052e001aaa536fca74813cb"
```

### 6.2 Session Management

```python
# Session timeout: 1 hour
SESSION_TIMEOUT = 3600

def check_session_valid():
    """Verify session hasn't expired"""
    if 'login_time' not in st.session_state:
        return False
    
    elapsed = time.time() - st.session_state.login_time
    if elapsed > SESSION_TIMEOUT:
        logout()
        return False
    
    return True
```

### 6.3 Rate Limiting

```python
# Prevent brute force login attempts
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_TIME = 300  # 5 minutes

def check_rate_limit(email: str) -> bool:
    """Check if user is rate limited"""
    # Store failed attempts in session_state or cache
    # Lock out after 3 failed attempts for 5 minutes
    pass
```

### 6.4 Data Privacy (GDPR/RODO)

```python
# Anonymization function
def anonymize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove PII from dataset"""
    df['Email'] = df['Email'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest()[:8])
    df['First_Name'] = 'XXXXX'
    df['Last_Name'] = 'XXXXX'
    return df

# Data deletion
def delete_student_data(email: str) -> bool:
    """Delete all data for specific student (GDPR compliance)"""
    # Remove from Google Sheets
    # Remove from any cache
    pass
```

### 6.5 Input Validation

```python
# Email validation
def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Sanitize inputs
def sanitize_input(text: str) -> str:
    """Remove potentially harmful characters"""
    # Remove script tags, SQL injection attempts, etc.
    clean = re.sub(r'[<>\"\'%;()&+]', '', text)
    return clean.strip()
```

---

## 7. INTEGRATION DESIGN

### 7.1 Google Sheets API Integration

```python
# OAuth2 Service Account flow
SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# Credentials stored in Streamlit secrets
# secrets.toml:
[google_sheets]
type = "service_account"
project_id = "ai-test-platform"
private_key_id = "xxx"
private_key = "-----BEGIN PRIVATE KEY-----\nxxx\n-----END PRIVATE KEY-----\n"
client_email = "test-platform@ai-test-platform.iam.gserviceaccount.com"
client_id = "xxx"
```

### 7.2 Gmail SMTP Integration

```python
# App Password authentication (not regular password)
SMTP_CONFIG = {
    'server': 'smtp.gmail.com',
    'port': 587,
    'use_tls': True,
    'email': 'notifications@ainetwork.pl',
    'app_password': 'xxxx xxxx xxxx xxxx'  # 16-char app password
}

# Email templates
TEMPLATES = {
    'student_pass': 'templates/email_student_pass.html',
    'student_fail': 'templates/email_student_fail.html',
    'teacher_notification': 'templates/email_teacher.html'
}
```

### 7.3 Error Handling for External Services

```python
# Retry logic for API calls
from functools import wraps
import time

def retry_on_failure(max_attempts=3, delay=2):
    """Decorator to retry failed API calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        continue
                    else:
                        raise e
        return wrapper
    return decorator

@retry_on_failure(max_attempts=3, delay=2)
def save_to_sheets(data):
    """Save with automatic retry"""
    sheets_manager.save_test_result(data)
```

---

## 8. DEPLOYMENT ARCHITECTURE

### 8.1 Streamlit Cloud Deployment

```yaml
# Deployment configuration
Platform: Streamlit Community Cloud
URL: https://aitest-uken.streamlit.app
Branch: main (auto-deploy on push)
Python version: 3.11
Resources:
  - CPU: Shared
  - RAM: 1GB
  - Concurrent users: 50 max
```

### 8.2 Environment Configuration

**File:** `.streamlit/config.toml`

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

**File:** `.streamlit/secrets.toml` (not in git)

```toml
[google_sheets]
type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
private_key = "xxx"
client_email = "xxx"
client_id = "xxx"

[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_email = "xxx"
smtp_password = "xxx"
teacher_email = "tina@example.com"

[auth]
teacher_password_hash = "xxx"
```

### 8.3 GitHub Workflow

```
Repository: github.com/ainetwork/test-platform
Branch structure:
  - main (production, auto-deploy)
  - develop (testing)
  - feature/* (development)

Deployment trigger: Push to main branch
Build time: ~2-3 minutes
```

### 8.4 Monitoring & Logs

```python
# Streamlit Cloud provides basic logs
# Access via: Dashboard → App → Logs

# Custom logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Log important events
logger.info(f"Student logged in: {email}")
logger.info(f"Test submitted: {email}, Score: {score}")
logger.error(f"Failed to save to Sheets: {error}")
```

---

## 9. ERROR HANDLING & LOGGING

### 9.1 Error Handling Strategy

```python
# Global error handler
def handle_error(error: Exception, context: str):
    """
    Centralized error handling
    
    Args:
        error: The exception
        context: Description of what was happening
    """
    logger.error(f"Error in {context}: {str(error)}")
    
    # Show user-friendly message
    st.error(f"Wystąpił błąd: {context}. Spróbuj ponownie lub skontaktuj się z administratorem.")
    
    # Optionally send error notification to admin
    if PRODUCTION:
        notify_admin_of_error(error, context)
```

### 9.2 Specific Error Cases

```python
# Google Sheets unavailable
try:
    sheets_manager.save_test_result(data)
except Exception as e:
    # Fallback: save locally and retry later
    save_to_local_cache(data)
    st.warning("Wyniki zostały zapisane lokalnie. Spróbujemy zapisać do bazy później.")

# Email sending fails
try:
    email_service.send_student_notification(student, results)
except Exception as e:
    # Non-critical: log but don't block
    logger.error(f"Failed to send email: {e}")
    st.info("Wyniki są dostępne, ale email mógł nie zostać wysłany.")

# Timer not working
if not hasattr(st.session_state, 'start_time'):
    st.error("Błąd timera. Odśwież stronę i rozpocznij test ponownie.")
    st.stop()
```

### 9.3 Logging Levels

```python
# DEBUG: Detailed diagnostic information
logger.debug(f"Loading questions from {questions_file}")

# INFO: General informational messages
logger.info(f"Student {email} started test at {timestamp}")

# WARNING: Warning messages (non-critical)
logger.warning(f"Slow API response: {elapsed_time}s")

# ERROR: Error messages (something failed)
logger.error(f"Failed to connect to Google Sheets: {error}")

# CRITICAL: Critical errors (system failure)
logger.critical(f"Database connection lost. Cannot save data.")
```

---

## 10. PERFORMANCE OPTIMIZATION

### 10.1 Caching Strategy

```python
# Cache Google Sheets data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_all_results():
    """Load results with caching"""
    return sheets_manager.get_all_results()

# Cache questions (never changes)
@st.cache_data
def load_questions():
    """Cache questions in memory"""
    with open('data/questions.json', 'r') as f:
        return json.load(f)

# Cache teacher credentials
@st.cache_resource
def get_sheets_client():
    """Cache Google Sheets client"""
    return SheetsManager()
```

### 10.2 Lazy Loading

```python
# Load data only when needed
def teacher_dashboard():
    """Load dashboard data on demand"""
    
    # Only load if viewing dashboard page
    if st.session_state.get('page') == 'dashboard':
        df = load_all_results()
        stats = AnalyticsEngine(df).get_overview_stats()
        display_dashboard(stats, df)
```

### 10.3 Batch Operations

```python
# Batch read from Sheets (not one-by-one)
def get_multiple_students(email_list: list) -> list:
    """Fetch multiple students in one operation"""
    df = load_all_results()
    return df[df['Email'].isin(email_list)].to_dict('records')
```

### 10.4 Asset Optimization

```python
# Optimize images
# - Logo: 200x200px max, PNG optimized
# - Use lazy loading for images
# - Minimize CSS/JS inline code

# Minify CSS
CUSTOM_CSS = """
<style>
.custom-class{background:#F5F5F5;padding:20px;border:1px solid #000}
</style>
"""
```

---

## 11. TESTING STRATEGY

### 11.1 Unit Tests

```python
# tests/test_scoring.py
def test_perfect_score():
    """Test calculation of perfect score"""
    answers = {str(i): correct_answers[str(i)] for i in range(1, 28)}
    result = test_engine.calculate_score(answers)
    assert result['correct_count'] == 27
    assert result['grade'] == 5.0
    assert result['passed'] == True

def test_failing_score():
    """Test failing grade calculation"""
    answers = {str(i): 'a' for i in range(1, 28)}  # All wrong
    result = test_engine.calculate_score(answers)
    assert result['grade'] == 2.0
    assert result['passed'] == False
```

### 11.2 Integration Tests

```python
# tests/test_integration.py
def test_full_student_flow():
    """Test complete student flow"""
    # Login
    assert auth.student_login('test@example.com', 'Test', 'Student')
    
    # Start test
    test_engine.start_test()
    
    # Answer questions
    for i in range(1, 28):
        test_engine.save_answer(i, 'a')
    
    # Calculate score
    results = test_engine.calculate_score()
    
    # Save to sheets (mock)
    assert sheets_manager.save_test_result(results)
```

---

## 12. MAINTENANCE & SUPPORT

### 12.1 Backup Strategy

```python
# Google Sheets auto-backup (Google Drive versioning)
# Manual export script
def export_backup():
    """Export all data to CSV backup"""
    df = load_all_results()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'backup_{timestamp}.csv'
    df.to_csv(filename, index=False)
```

### 12.2 Update Procedures

```python
# Questions update
# 1. Edit data/questions.json
# 2. Test locally
# 3. Push to GitHub
# 4. Auto-deploy to production

# Dependency updates
# requirements.txt
# pip list --outdated
# pip install --upgrade <package>
# Test locally before deploy
```

---

## 13. APPENDIX

### 13.1 API Rate Limits

```
Google Sheets API:
- Read requests: 60 per minute per user
- Write requests: 60 per minute per user

Gmail SMTP:
- 500 emails per day (free Gmail)
- 2000 per day (Google Workspace)

Streamlit Cloud:
- 50 concurrent users
- 1GB RAM per app
```

### 13.2 Dependencies Versions

```
streamlit==1.30.0
gspread==5.12.0
oauth2client==4.1.3
pandas==2.1.4
plotly==5.18.0
python-dotenv==1.0.0
```

---

**Document Status:** ✅ APPROVED FOR DEVELOPMENT  
**Last Updated:** 2026-01-12  
**Next Review:** After MVP completion
