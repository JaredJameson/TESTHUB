"""
Email Service - Gmail SMTP Integration for Test Results
Handles sending email notifications to students and teachers
"""

import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Optional
import streamlit as st


class EmailService:
    """
    Manages email notifications using Gmail SMTP
    """

    def __init__(self):
        """Initialize email service with SMTP configuration from secrets"""
        try:
            self.smtp_server = "smtp.gmail.com"
            self.smtp_port = 587
            self.sender_email = st.secrets["email"]["sender_email"]
            self.sender_password = st.secrets["email"]["sender_password"]
            self.teacher_email = st.secrets["email"]["teacher_email"]
            self.enabled = True
        except Exception as e:
            st.warning(f"Email service not configured: {e}")
            self.enabled = False

    def send_student_result_email(
        self,
        student_email: str,
        student_name: str,
        results: dict,
        async_send: bool = True
    ) -> bool:
        """
        Send test results email to student

        Args:
            student_email: Student's email address
            student_name: Student's full name
            results: Test results dictionary from test_engine.calculate_results()
            async_send: Whether to send asynchronously (default True)

        Returns:
            bool: True if email sent successfully (or queued for async)
        """
        if not self.enabled:
            return False

        try:
            subject = f"Wyniki Testu - AI w Marketingu"
            html_content = self._generate_student_email_html(student_name, results)

            if async_send:
                # Send email in background thread
                thread = threading.Thread(
                    target=self._send_email,
                    args=(student_email, subject, html_content)
                )
                thread.daemon = True
                thread.start()
                return True
            else:
                # Send email synchronously
                return self._send_email(student_email, subject, html_content)

        except Exception as e:
            st.error(f"Błąd wysyłania emaila do studenta: {e}")
            return False

    def send_teacher_notification_email(
        self,
        student_name: str,
        student_email: str,
        results: dict,
        async_send: bool = True
    ) -> bool:
        """
        Send notification email to teacher about new test result

        Args:
            student_name: Student's full name
            student_email: Student's email address
            results: Test results dictionary
            async_send: Whether to send asynchronously (default True)

        Returns:
            bool: True if email sent successfully (or queued for async)
        """
        if not self.enabled:
            return False

        try:
            subject = f"Nowy wynik testu - {student_name}"
            html_content = self._generate_teacher_email_html(
                student_name,
                student_email,
                results
            )

            if async_send:
                # Send email in background thread
                thread = threading.Thread(
                    target=self._send_email,
                    args=(self.teacher_email, subject, html_content)
                )
                thread.daemon = True
                thread.start()
                return True
            else:
                # Send email synchronously
                return self._send_email(self.teacher_email, subject, html_content)

        except Exception as e:
            st.error(f"Błąd wysyłania emaila do nauczyciela: {e}")
            return False

    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """
        Internal method to send email via Gmail SMTP

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of email

        Returns:
            bool: True if sent successfully
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject

            # Attach HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            return True

        except Exception as e:
            print(f"Email send error: {e}")
            return False

    def _generate_student_email_html(self, student_name: str, results: dict) -> str:
        """
        Generate HTML email template for student results

        Args:
            student_name: Student's full name
            results: Test results dictionary

        Returns:
            str: HTML content for email
        """
        passed = results['passed']
        status_color = "#2D5016" if passed else "#8B0000"
        status_text = "ZALICZONY" if passed else "NIEZALICZONY"
        status_emoji = "✅" if passed else "❌"

        # Calculate time spent
        time_minutes = int(results['time_spent_seconds'] / 60)
        time_seconds = results['time_spent_seconds'] % 60

        # Category breakdown
        category_rows = ""
        for category, stats in results.get('category_stats', {}).items():
            category_rows += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #000000;">{category}</td>
                <td style="padding: 8px; border: 1px solid #000000; text-align: center;">{stats['correct']}/{stats['total']}</td>
                <td style="padding: 8px; border: 1px solid #000000; text-align: center;">{stats['percentage']}%</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #F5F5F5;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #FFFFFF;
                    border: 2px solid #000000;
                    padding: 32px;
                }}
                .status-card {{
                    background: #FFFFFF;
                    border: 3px solid {status_color};
                    padding: 32px;
                    text-align: center;
                    margin-bottom: 24px;
                }}
                .status-title {{
                    font-size: 36px;
                    font-weight: 700;
                    color: {status_color};
                    margin-bottom: 16px;
                }}
                .percentage {{
                    font-size: 48px;
                    font-weight: 700;
                    color: #000000;
                    margin-bottom: 8px;
                }}
                .grade-box {{
                    font-size: 20px;
                    color: #000000;
                    padding: 12px 24px;
                    background: #F5F5F5;
                    border: 1px solid #000000;
                    display: inline-block;
                    margin-top: 16px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 16px 0;
                }}
                th {{
                    background: #000000;
                    color: #FFFFFF;
                    padding: 12px;
                    text-align: left;
                }}
                td {{
                    padding: 8px;
                    border: 1px solid #000000;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="color: #000000; margin-bottom: 8px;">Wyniki Testu</h1>
                <h2 style="color: #000000; margin-bottom: 24px;">AI w Marketingu</h2>

                <p>Cześć {student_name},</p>
                <p>Twój test został oceniony. Poniżej znajdziesz szczegółowe wyniki:</p>

                <div class="status-card">
                    <div class="status-title">{status_emoji} {status_text}</div>
                    <div class="percentage">{results['percentage']}%</div>
                    <div style="font-size: 20px; margin-bottom: 16px;">
                        {results['correct_count']}/{results['total_questions']} poprawnych odpowiedzi
                    </div>
                    <div class="grade-box">
                        Ocena: {results['grade']} - {results['grade_text']}
                    </div>
                </div>

                <p><strong>Czas rozwiązywania:</strong> {time_minutes} min {time_seconds} sek</p>

                <h3 style="margin-top: 32px;">Wyniki według kategorii</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Kategoria</th>
                            <th style="text-align: center;">Poprawne</th>
                            <th style="text-align: center;">Procent</th>
                        </tr>
                    </thead>
                    <tbody>
                        {category_rows}
                    </tbody>
                </table>

                <div style="margin-top: 32px; padding: 16px; background: #F5F5F5; border: 1px solid #000000;">
                    <p style="margin: 0;"><strong>Przypomnienie:</strong></p>
                    <p style="margin: 8px 0 0 0;">
                        Próg zaliczenia to 48% (13 poprawnych odpowiedzi).
                        Szczegółowe wyniki oraz wyjaśnienia do pytań są dostępne w systemie testowym.
                    </p>
                </div>

                <p style="margin-top: 24px;">Pozdrawienia,<br>System Testowy UKEN</p>
            </div>
        </body>
        </html>
        """
        return html

    def _generate_teacher_email_html(
        self,
        student_name: str,
        student_email: str,
        results: dict
    ) -> str:
        """
        Generate HTML email template for teacher notification

        Args:
            student_name: Student's full name
            student_email: Student's email address
            results: Test results dictionary

        Returns:
            str: HTML content for email
        """
        passed = results['passed']
        status_color = "#2D5016" if passed else "#8B0000"
        status_text = "ZALICZONY" if passed else "NIEZALICZONY"
        status_emoji = "✅" if passed else "❌"

        # Calculate time spent
        time_minutes = int(results['time_spent_seconds'] / 60)
        time_seconds = results['time_spent_seconds'] % 60

        # Auto-submitted info
        auto_submitted = results.get('auto_submitted', False)
        auto_submit_text = "<p><em>⏰ Test został automatycznie wysłany po upływie czasu</em></p>" if auto_submitted else ""

        # Category breakdown
        category_rows = ""
        for category, stats in results.get('category_stats', {}).items():
            percentage = stats['percentage']
            if percentage >= 80:
                color = "#2D5016"
            elif percentage >= 60:
                color = "#FFD700"
            else:
                color = "#8B0000"

            category_rows += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #000000;">{category}</td>
                <td style="padding: 8px; border: 1px solid #000000; text-align: center;">{stats['correct']}/{stats['total']}</td>
                <td style="padding: 8px; border: 1px solid #000000; text-align: center; color: {color}; font-weight: 600;">{stats['percentage']}%</td>
            </tr>
            """

        # Current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #F5F5F5;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #FFFFFF;
                    border: 2px solid #000000;
                    padding: 32px;
                }}
                .header {{
                    background: #000000;
                    color: #FFFFFF;
                    padding: 16px;
                    margin: -32px -32px 24px -32px;
                }}
                .status-badge {{
                    display: inline-block;
                    padding: 8px 16px;
                    background: {status_color};
                    color: #FFFFFF;
                    font-weight: 700;
                    font-size: 18px;
                }}
                .info-box {{
                    background: #F5F5F5;
                    border: 1px solid #000000;
                    padding: 16px;
                    margin: 16px 0;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 16px 0;
                }}
                th {{
                    background: #000000;
                    color: #FFFFFF;
                    padding: 12px;
                    text-align: left;
                }}
                td {{
                    padding: 8px;
                    border: 1px solid #000000;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Nowy wynik testu</h2>
                    <p style="margin: 8px 0 0 0;">Test Zaliczeniowy - AI w Marketingu</p>
                </div>

                <p><strong>Student:</strong> {student_name}</p>
                <p><strong>Email:</strong> {student_email}</p>
                <p><strong>Data i czas:</strong> {timestamp}</p>

                <div class="info-box">
                    <p style="margin: 0 0 8px 0;"><strong>Wynik:</strong></p>
                    <div class="status-badge">{status_emoji} {status_text}</div>
                    <p style="margin: 16px 0 0 0; font-size: 24px; font-weight: 700;">
                        {results['percentage']}% ({results['correct_count']}/{results['total_questions']})
                    </p>
                    <p style="margin: 8px 0 0 0;">
                        <strong>Ocena:</strong> {results['grade']} - {results['grade_text']}
                    </p>
                    <p style="margin: 8px 0 0 0;">
                        <strong>Czas:</strong> {time_minutes} min {time_seconds} sek
                    </p>
                </div>

                {auto_submit_text}

                <h3 style="margin-top: 24px;">Wyniki według kategorii</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Kategoria</th>
                            <th style="text-align: center;">Poprawne</th>
                            <th style="text-align: center;">Procent</th>
                        </tr>
                    </thead>
                    <tbody>
                        {category_rows}
                    </tbody>
                </table>

                <div style="margin-top: 32px; padding: 16px; background: #FFFFCC; border: 1px solid #FFD700;">
                    <p style="margin: 0 0 8px 0;"><strong>ℹ️ Informacja</strong></p>
                    <p style="margin: 0;">
                        Szczegółowe wyniki wraz z odpowiedziami studenta są dostępne w panelu nauczyciela
                        oraz zostały zapisane w arkuszu Google Sheets.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
