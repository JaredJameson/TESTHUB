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
from google.oauth2.service_account import Credentials
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
        self.sheet_id = st.secrets['app']['spreadsheet_id']
        self.workbook = self.client.open_by_key(self.sheet_id)

    def _authenticate(self):
        """Authenticate with Google Sheets API using service account"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        # Load credentials from Streamlit secrets
        creds_dict = dict(st.secrets['google_sheets'])

        credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
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
