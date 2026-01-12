"""
Analytics Module - Global Statistics and Analysis
Aggregates and analyzes test results across all students
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime
import streamlit as st


class Analytics:
    """
    Manages analytics and statistics for test results
    """

    def __init__(self, sheets_manager):
        """
        Initialize analytics with sheets manager

        Args:
            sheets_manager: SheetsManager instance for data access
        """
        self.sheets_manager = sheets_manager

    def get_global_statistics(self) -> Dict:
        """
        Calculate global statistics across all test results

        Returns:
            dict: Global statistics including:
                - total_tests: Total number of completed tests
                - pass_rate: Percentage of passed tests
                - average_score: Average percentage score
                - average_grade: Average numeric grade
                - average_time: Average time spent (seconds)
                - grade_distribution: Count per grade
        """
        # Get all results from sheets
        df = self.sheets_manager.get_all_results()

        if df.empty:
            return {
                'total_tests': 0,
                'pass_rate': 0.0,
                'average_score': 0.0,
                'average_grade': 0.0,
                'average_time': 0,
                'grade_distribution': {}
            }

        all_results = df.to_dict('records')

        # Calculate statistics
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r.get('Zdany', False))
        total_score = sum(float(r.get('Procent', 0)) for r in all_results)
        total_time = sum(int(r.get('Czas_Sekundy', 0)) for r in all_results)

        # Grade distribution
        grade_distribution = {}
        grade_values = []
        for result in all_results:
            grade = result.get('Ocena', '0.0')
            grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
            try:
                grade_values.append(float(grade))
            except:
                pass

        return {
            'total_tests': total_tests,
            'pass_rate': round((passed_tests / total_tests * 100), 2) if total_tests > 0 else 0.0,
            'average_score': round(total_score / total_tests, 2) if total_tests > 0 else 0.0,
            'average_grade': round(sum(grade_values) / len(grade_values), 2) if grade_values else 0.0,
            'average_time': int(total_time / total_tests) if total_tests > 0 else 0,
            'grade_distribution': grade_distribution
        }

    def get_category_analysis(self) -> Dict:
        """
        Analyze performance across all categories

        Returns:
            dict: Category-wise statistics with:
                - category_name: {
                    - total_questions: Total questions in category
                    - average_correct: Average correct per category
                    - average_percentage: Average percentage per category
                    - students_analyzed: Number of students
                  }
        """
        df = self.sheets_manager.get_all_results()

        if df.empty:
            return {}

        all_results = df.to_dict('records')

        # Aggregate category data
        category_data = {}

        for result in all_results:
            details_json = result.get('Details_JSON', '{}')
            try:
                if isinstance(details_json, str):
                    details = json.loads(details_json)
                else:
                    details = details_json

                category_breakdown = details.get('category_breakdown', {})

                for category, stats in category_breakdown.items():
                    if category not in category_data:
                        category_data[category] = {
                            'total_questions': stats.get('total', 0),
                            'correct_sum': 0,
                            'percentage_sum': 0.0,
                            'student_count': 0
                        }

                    category_data[category]['correct_sum'] += stats.get('correct', 0)
                    category_data[category]['percentage_sum'] += stats.get('percentage', 0.0)
                    category_data[category]['student_count'] += 1

            except Exception as e:
                st.warning(f"Błąd przetwarzania danych kategorii: {e}")
                continue

        # Calculate averages
        category_analysis = {}
        for category, data in category_data.items():
            student_count = data['student_count']
            if student_count > 0:
                category_analysis[category] = {
                    'total_questions': data['total_questions'],
                    'average_correct': round(data['correct_sum'] / student_count, 2),
                    'average_percentage': round(data['percentage_sum'] / student_count, 2),
                    'students_analyzed': student_count
                }

        return category_analysis

    def get_hardest_questions(self, top_n: int = 10) -> List[Dict]:
        """
        Identify questions with lowest correct answer rate

        Args:
            top_n: Number of hardest questions to return

        Returns:
            list: Questions sorted by difficulty (hardest first) with:
                - question_id: Question ID
                - correct_count: Number of correct answers
                - total_attempts: Total attempts
                - correct_rate: Percentage correct
                - category: Question category
        """
        df = self.sheets_manager.get_all_results()

        if df.empty:
            return []

        all_results = df.to_dict('records')

        # Track question statistics
        question_stats = {}

        for result in all_results:
            details_json = result.get('Details_JSON', '{}')
            try:
                if isinstance(details_json, str):
                    details = json.loads(details_json)
                else:
                    details = details_json

                answers = details.get('answers', {})

                for q_id, answer_data in answers.items():
                    if q_id not in question_stats:
                        question_stats[q_id] = {
                            'question_id': int(q_id),
                            'correct_count': 0,
                            'total_attempts': 0,
                            'category': answer_data.get('category', 'Unknown')
                        }

                    question_stats[q_id]['total_attempts'] += 1
                    if answer_data.get('is_correct', False):
                        question_stats[q_id]['correct_count'] += 1

            except Exception as e:
                continue

        # Calculate correct rates
        question_list = []
        for q_id, stats in question_stats.items():
            total = stats['total_attempts']
            if total > 0:
                stats['correct_rate'] = round((stats['correct_count'] / total * 100), 2)
                question_list.append(stats)

        # Sort by correct rate (ascending - hardest first)
        question_list.sort(key=lambda x: x['correct_rate'])

        return question_list[:top_n]

    def get_easiest_questions(self, top_n: int = 10) -> List[Dict]:
        """
        Identify questions with highest correct answer rate

        Args:
            top_n: Number of easiest questions to return

        Returns:
            list: Questions sorted by easiness (easiest first)
        """
        df = self.sheets_manager.get_all_results()

        if df.empty:
            return []

        all_results = df.to_dict('records')

        # Track question statistics (same as hardest_questions)
        question_stats = {}

        for result in all_results:
            details_json = result.get('Details_JSON', '{}')
            try:
                if isinstance(details_json, str):
                    details = json.loads(details_json)
                else:
                    details = details_json

                answers = details.get('answers', {})

                for q_id, answer_data in answers.items():
                    if q_id not in question_stats:
                        question_stats[q_id] = {
                            'question_id': int(q_id),
                            'correct_count': 0,
                            'total_attempts': 0,
                            'category': answer_data.get('category', 'Unknown')
                        }

                    question_stats[q_id]['total_attempts'] += 1
                    if answer_data.get('is_correct', False):
                        question_stats[q_id]['correct_count'] += 1

            except Exception:
                continue

        # Calculate correct rates
        question_list = []
        for q_id, stats in question_stats.items():
            total = stats['total_attempts']
            if total > 0:
                stats['correct_rate'] = round((stats['correct_count'] / total * 100), 2)
                question_list.append(stats)

        # Sort by correct rate (descending - easiest first)
        question_list.sort(key=lambda x: x['correct_rate'], reverse=True)

        return question_list[:top_n]

    def get_time_analysis(self) -> Dict:
        """
        Analyze time spent on tests

        Returns:
            dict: Time analysis with:
                - fastest_time: Fastest completion (seconds)
                - slowest_time: Slowest completion (seconds)
                - average_time: Average completion (seconds)
                - median_time: Median completion (seconds)
                - auto_submit_count: Tests auto-submitted due to timeout
        """
        df = self.sheets_manager.get_all_results()

        if df.empty:
            return {
                'fastest_time': 0,
                'slowest_time': 0,
                'average_time': 0,
                'median_time': 0,
                'auto_submit_count': 0
            }

        all_results = df.to_dict('records')

        times = []
        auto_submit_count = 0

        for result in all_results:
            time_seconds = int(result.get('Czas_Sekundy', 0))
            if time_seconds > 0:
                times.append(time_seconds)

            # Check auto-submit flag
            auto_submitted = result.get('Auto_Submitted', False)
            if auto_submitted:
                auto_submit_count += 1

        times.sort()

        # Calculate median
        n = len(times)
        if n == 0:
            median = 0
        elif n % 2 == 0:
            median = (times[n // 2 - 1] + times[n // 2]) // 2
        else:
            median = times[n // 2]

        return {
            'fastest_time': min(times) if times else 0,
            'slowest_time': max(times) if times else 0,
            'average_time': sum(times) // len(times) if times else 0,
            'median_time': median,
            'auto_submit_count': auto_submit_count
        }

    def get_student_performance_summary(self, limit: int = None) -> List[Dict]:
        """
        Get summary of all student performances

        Args:
            limit: Optional limit on number of results

        Returns:
            list: Student performances sorted by date (newest first)
        """
        df = self.sheets_manager.get_all_results()

        if df.empty:
            return []

        # Sort by timestamp (newest first)
        df = df.sort_values(by='Timestamp', ascending=False)

        # Apply limit if specified
        if limit:
            df = df.head(limit)

        return df.to_dict('records')

    def get_pass_rate_by_date(self) -> Dict:
        """
        Calculate pass rate grouped by date

        Returns:
            dict: Date -> pass rate mapping
        """
        df = self.sheets_manager.get_all_results()

        if df.empty:
            return {}

        all_results = df.to_dict('records')

        date_stats = {}

        for result in all_results:
            timestamp = result.get('Timestamp', '')
            try:
                # Extract date from timestamp (YYYY-MM-DD HH:MM:SS)
                date = timestamp.split(' ')[0]

                if date not in date_stats:
                    date_stats[date] = {
                        'total': 0,
                        'passed': 0
                    }

                date_stats[date]['total'] += 1
                if result.get('Zdany', False):
                    date_stats[date]['passed'] += 1

            except Exception:
                continue

        # Calculate pass rates
        pass_rates = {}
        for date, stats in date_stats.items():
            if stats['total'] > 0:
                pass_rates[date] = round((stats['passed'] / stats['total'] * 100), 2)

        return pass_rates

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
