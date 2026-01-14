"""
Test Engine - Core Logic for AI Marketing Test
Handles test flow, timing, scoring, and results
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import streamlit as st


class TestEngine:
    """
    Manages test logic, timing, and scoring
    """

    def __init__(self):
        """Initialize test engine with questions and config"""
        self.questions = self._load_questions()
        self.config = self._load_config()
        self.test_info = self.questions.get('test_info', {})
        self.categories = self.questions.get('categories', [])

    def _load_questions(self) -> dict:
        """Load questions from JSON file"""
        try:
            with open('data/questions.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Błąd wczytywania pytań: {e}")
            return {}

    def _load_config(self) -> dict:
        """Load test configuration"""
        try:
            with open('data/test_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Błąd wczytywania konfiguracji: {e}")
            return {}

    def initialize_test(self, randomize: bool = False) -> bool:
        """
        Initialize test for student

        Args:
            randomize: Whether to randomize question order

        Returns:
            bool: True if successful
        """
        try:
            # Get questions list
            questions_list = self.questions.get('questions', [])

            if randomize:
                random.shuffle(questions_list)

            # Initialize session state
            st.session_state.test_questions = questions_list
            st.session_state.test_answers = {}
            st.session_state.current_question = 0
            st.session_state.test_start_time = time.time()
            st.session_state.test_completed = False
            st.session_state.auto_saves = []

            # Per-question timing (20 seconds per question)
            st.session_state.question_start_time = time.time()
            st.session_state.question_time_limit = 20  # 20 seconds per question
            st.session_state.locked_questions = set()  # Track locked questions

            return True

        except Exception as e:
            st.error(f"Błąd inicjalizacji testu: {e}")
            return False

    def get_question(self, index: int) -> dict:
        """
        Get question by index

        Args:
            index: Question index (0-based)

        Returns:
            dict: Question data
        """
        questions = st.session_state.get('test_questions', [])
        if 0 <= index < len(questions):
            return questions[index]
        return {}

    def get_total_questions(self) -> int:
        """Get total number of questions"""
        return len(st.session_state.get('test_questions', []))

    def save_answer(self, question_id: int, answer: str) -> None:
        """
        Save student's answer

        Args:
            question_id: Question ID
            answer: Selected answer (a, b, c, or d)
        """
        if 'test_answers' not in st.session_state:
            st.session_state.test_answers = {}

        st.session_state.test_answers[question_id] = {
            'selected': answer,
            'timestamp': time.time()
        }

    def get_answer(self, question_id: int) -> str:
        """
        Get saved answer for question

        Args:
            question_id: Question ID

        Returns:
            str: Selected answer or empty string
        """
        answers = st.session_state.get('test_answers', {})
        answer_data = answers.get(question_id, {})
        return answer_data.get('selected', '')

    def get_question_time_remaining(self) -> int:
        """
        Get remaining time for current question in seconds

        Returns:
            int: Seconds remaining for current question
        """
        start_time = st.session_state.get('question_start_time', time.time())
        time_limit = st.session_state.get('question_time_limit', 20)
        elapsed = time.time() - start_time
        remaining = max(0, time_limit - elapsed)
        return int(remaining)

    def is_question_time_up(self) -> bool:
        """Check if current question time has expired"""
        return self.get_question_time_remaining() <= 0

    def lock_current_question(self) -> None:
        """Lock current question when time expires"""
        current_q_idx = st.session_state.get('current_question', 0)
        if 'locked_questions' not in st.session_state:
            st.session_state.locked_questions = set()
        st.session_state.locked_questions.add(current_q_idx)

    def is_question_locked(self, question_index: int) -> bool:
        """
        Check if question is locked

        Args:
            question_index: Question index to check

        Returns:
            bool: True if question is locked
        """
        locked = st.session_state.get('locked_questions', set())
        return question_index in locked

    def reset_question_timer(self) -> None:
        """Reset timer when moving to new question"""
        st.session_state.question_start_time = time.time()

    def get_time_remaining(self) -> int:
        """
        Get remaining time in seconds (DEPRECATED - use get_question_time_remaining)

        Returns:
            int: Seconds remaining
        """
        return self.get_question_time_remaining()

    def is_time_up(self) -> bool:
        """Check if time has expired (DEPRECATED - use is_question_time_up)"""
        return self.is_question_time_up()

    def format_time(self, seconds: int) -> str:
        """
        Format seconds to MM:SS

        Args:
            seconds: Time in seconds

        Returns:
            str: Formatted time string
        """
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def get_answered_count(self) -> int:
        """Get number of answered questions"""
        return len(st.session_state.get('test_answers', {}))

    def should_auto_save(self) -> bool:
        """
        Check if auto-save should be triggered

        Returns:
            bool: True if should auto-save
        """
        answered = self.get_answered_count()
        interval = self.config.get('test_settings', {}).get('auto_save_interval', 5)
        auto_saves = st.session_state.get('auto_saves', [])

        # Auto-save at every interval (5, 10, 15, 20, 25)
        if answered > 0 and answered % interval == 0:
            # Check if not already saved at this checkpoint
            if answered not in auto_saves:
                return True
        return False

    def mark_auto_saved(self, checkpoint: int) -> None:
        """
        Mark checkpoint as auto-saved

        Args:
            checkpoint: Question number checkpoint
        """
        if 'auto_saves' not in st.session_state:
            st.session_state.auto_saves = []
        st.session_state.auto_saves.append(checkpoint)

    def calculate_results(self) -> dict:
        """
        Calculate test results

        Returns:
            dict: Complete test results
        """
        questions = st.session_state.get('test_questions', [])
        answers = st.session_state.get('test_answers', {})

        correct_count = 0
        total_questions = len(questions)
        category_stats = {}
        details = {}

        # Calculate results for each question
        for question in questions:
            q_id = question['id']
            category = question['category']
            correct_answer = question['correct_answer']

            # Initialize category stats
            if category not in category_stats:
                category_stats[category] = {
                    'correct': 0,
                    'total': 0,
                    'questions': []
                }

            category_stats[category]['total'] += 1
            category_stats[category]['questions'].append(q_id)

            # Get student's answer
            student_answer = answers.get(q_id, {}).get('selected', '')
            is_correct = student_answer == correct_answer

            if is_correct:
                correct_count += 1
                category_stats[category]['correct'] += 1

            # Store detailed answer
            details[q_id] = {
                'selected': student_answer,
                'correct': correct_answer,
                'is_correct': is_correct,
                'category': category,
                'question': question['question'],
                'explanation': question.get('explanation', '')
            }

        # Calculate percentage
        percentage = round((correct_count / total_questions) * 100, 2)

        # Determine grade and pass status
        grade, grade_text = self._calculate_grade(correct_count, percentage)
        passed = percentage >= self.test_info.get('pass_threshold', 0.48) * 100

        # Calculate time spent
        start_time = st.session_state.get('test_start_time', time.time())
        time_spent = int(time.time() - start_time)

        # Calculate category percentages
        for cat, stats in category_stats.items():
            if stats['total'] > 0:
                stats['percentage'] = round((stats['correct'] / stats['total']) * 100, 2)
            else:
                stats['percentage'] = 0

        return {
            'correct_count': correct_count,
            'total_questions': total_questions,
            'percentage': percentage,
            'grade': grade,
            'grade_text': grade_text,
            'passed': passed,
            'time_spent_seconds': time_spent,
            'category_stats': category_stats,
            'details': details
        }

    def _calculate_grade(self, correct_count: int, percentage: float) -> Tuple[str, str]:
        """
        Calculate grade based on grading scale

        Args:
            correct_count: Number of correct answers
            percentage: Percentage score

        Returns:
            tuple: (grade, grade_text)
        """
        grading_scale = self.config.get('grading_scale', {})

        # Sort by min_percentage descending
        grades = sorted(
            grading_scale.items(),
            key=lambda x: x[1]['min_percentage'],
            reverse=True
        )

        for grade, criteria in grades:
            if percentage >= criteria['min_percentage']:
                return (grade, criteria['description'])

        return ('2.0', 'Niedostateczny')

    def format_results_for_sheets(self, student_data: dict, results: dict) -> dict:
        """
        Format results for Google Sheets storage

        Args:
            student_data: Student information from session
            results: Test results from calculate_results()

        Returns:
            dict: Formatted data ready for sheets_manager
        """
        # Prepare details JSON
        details_json = {
            'answers': {},
            'category_breakdown': results['category_stats'],
            'metadata': {
                'test_version': self.config.get('test_settings', {}).get('test_version', 'v1.0'),
                'start_time': datetime.fromtimestamp(
                    st.session_state.get('test_start_time', time.time())
                ).isoformat(),
                'end_time': datetime.now().isoformat(),
                'auto_submitted': st.session_state.get('auto_submitted', False),
                'auto_saves': st.session_state.get('auto_saves', [])
            }
        }

        # Add answer details
        for q_id, detail in results['details'].items():
            details_json['answers'][str(q_id)] = {
                'selected': detail['selected'],
                'correct': detail['correct'],
                'is_correct': detail['is_correct'],
                'category': detail['category']
            }

        return {
            'email': student_data.get('email'),
            'first_name': student_data.get('first_name'),
            'last_name': student_data.get('last_name'),
            'student_id': student_data.get('student_id', ''),
            'correct_count': results['correct_count'],
            'percentage': results['percentage'],
            'grade': results['grade'],
            'grade_text': results['grade_text'],
            'passed': results['passed'],
            'time_spent_seconds': results['time_spent_seconds'],
            'details': details_json,
            'test_version': self.config.get('test_settings', {}).get('test_version', 'v1.0'),
            'browser_info': st.session_state.get('browser_info', 'Unknown'),
            'attempt_number': st.session_state.get('attempt_number', 1),
            'auto_submitted': st.session_state.get('auto_submitted', False)
        }

    def get_progress_percentage(self) -> float:
        """
        Get test completion percentage

        Returns:
            float: Percentage of questions answered
        """
        answered = self.get_answered_count()
        total = self.get_total_questions()
        if total > 0:
            return round((answered / total) * 100, 1)
        return 0.0
