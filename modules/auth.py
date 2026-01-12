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
