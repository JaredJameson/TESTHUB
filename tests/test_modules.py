"""
Module Unit Tests for test_engine.py, email_service.py, and analytics.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_test_engine():
    """Test TestEngine module"""
    print("\n" + "="*60)
    print("TESTING: modules/test_engine.py")
    print("="*60)

    issues = []

    try:
        from modules.test_engine import TestEngine
        print("✅ Module imports successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

    try:
        # Initialize engine
        engine = TestEngine()
        print("✅ TestEngine initialization successful")

        # Test data loading
        if hasattr(engine, 'questions') and engine.questions:
            print("✅ Questions loaded")
        else:
            issues.append("Questions not loaded")

        if hasattr(engine, 'config') and engine.config:
            print("✅ Config loaded")
        else:
            issues.append("Config not loaded")

        # Test question access
        total = engine.get_total_questions()
        if total == 27:
            print(f"✅ get_total_questions() returns 27")
        else:
            issues.append(f"get_total_questions() returns {total}, expected 27")

        # Test format_time
        time_str = engine.format_time(1800)
        if time_str == "30:00":
            print(f"✅ format_time(1800) = '30:00'")
        else:
            issues.append(f"format_time(1800) = '{time_str}', expected '30:00'")

        time_str = engine.format_time(299)
        if time_str == "04:59":
            print(f"✅ format_time(299) = '04:59'")
        else:
            issues.append(f"format_time(299) = '{time_str}', expected '04:59'")

        # Test grade calculation
        grade, grade_text = engine._calculate_grade(26, 96.3)
        if grade == '5.0' and grade_text == 'Bardzo dobry':
            print(f"✅ Grade calculation for 96.3% = 5.0 (Bardzo dobry)")
        else:
            issues.append(f"Grade calculation failed: {grade} - {grade_text}")

        grade, grade_text = engine._calculate_grade(13, 48.1)
        if grade == '3.0' and grade_text == 'Dostateczny (zaliczony)':
            print(f"✅ Grade calculation for 48.1% = 3.0 (Dostateczny)")
        else:
            issues.append(f"Grade calculation failed: {grade} - {grade_text}")

        grade, grade_text = engine._calculate_grade(12, 44.4)
        if grade == '2.0' and grade_text == 'Niedostateczny (niezaliczony)':
            print(f"✅ Grade calculation for 44.4% = 2.0 (Niedostateczny)")
        else:
            issues.append(f"Grade calculation failed: {grade} - {grade_text}")

    except Exception as e:
        issues.append(f"Exception during testing: {e}")
        import traceback
        traceback.print_exc()

    if issues:
        print(f"\n❌ FAILED: {len(issues)} issues found")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✅ PASSED: All test_engine tests successful")
        return True


def test_email_service():
    """Test EmailService module"""
    print("\n" + "="*60)
    print("TESTING: modules/email_service.py")
    print("="*60)

    issues = []

    try:
        from modules.email_service import EmailService
        print("✅ Module imports successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

    try:
        # Initialize service (will show warning if not configured, which is OK)
        service = EmailService()
        print("✅ EmailService initialization successful")

        # Check methods exist
        methods = [
            'send_student_result_email',
            'send_teacher_notification_email',
            '_send_email',
            '_generate_student_email_html',
            '_generate_teacher_email_html'
        ]

        for method in methods:
            if hasattr(service, method):
                print(f"✅ Method {method}() exists")
            else:
                issues.append(f"Method {method}() missing")

        # Test HTML generation (without sending)
        mock_results = {
            'passed': True,
            'percentage': 85.2,
            'correct_count': 23,
            'total_questions': 27,
            'grade': '4.5',
            'grade_text': 'Dobry plus',
            'time_spent_seconds': 1500,
            'category_stats': {
                'Test Category': {
                    'correct': 5,
                    'total': 5,
                    'percentage': 100.0
                }
            }
        }

        student_html = service._generate_student_email_html("Jan Kowalski", mock_results)
        if 'ZALICZONY' in student_html and '85.2%' in student_html:
            print("✅ Student email HTML generated correctly")
        else:
            issues.append("Student email HTML generation failed")

        teacher_html = service._generate_teacher_email_html("Jan Kowalski", "jan@example.com", mock_results)
        if 'Nowy wynik testu' in teacher_html and 'Jan Kowalski' in teacher_html:
            print("✅ Teacher email HTML generated correctly")
        else:
            issues.append("Teacher email HTML generation failed")

    except Exception as e:
        issues.append(f"Exception during testing: {e}")
        import traceback
        traceback.print_exc()

    if issues:
        print(f"\n❌ FAILED: {len(issues)} issues found")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✅ PASSED: All email_service tests successful")
        return True


def test_analytics():
    """Test Analytics module"""
    print("\n" + "="*60)
    print("TESTING: modules/analytics.py")
    print("="*60)

    issues = []

    try:
        from modules.analytics import Analytics
        print("✅ Module imports successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

    try:
        # Check methods exist (can't fully test without SheetsManager)
        methods = [
            'get_global_statistics',
            'get_category_analysis',
            'get_hardest_questions',
            'get_easiest_questions',
            'get_time_analysis',
            'get_student_performance_summary',
            'get_pass_rate_by_date',
            'format_time'
        ]

        # Create mock sheets_manager
        class MockSheetsManager:
            def get_all_results(self):
                import pandas as pd
                return pd.DataFrame()  # Empty DataFrame for testing

        analytics = Analytics(MockSheetsManager())
        print("✅ Analytics initialization successful")

        for method in methods:
            if hasattr(analytics, method):
                print(f"✅ Method {method}() exists")
            else:
                issues.append(f"Method {method}() missing")

        # Test format_time
        time_str = analytics.format_time(1800)
        if time_str == "30:00":
            print(f"✅ format_time(1800) = '30:00'")
        else:
            issues.append(f"format_time(1800) = '{time_str}', expected '30:00'")

        # Test with empty data
        stats = analytics.get_global_statistics()
        if stats['total_tests'] == 0:
            print("✅ get_global_statistics() handles empty data")
        else:
            issues.append("get_global_statistics() doesn't handle empty data correctly")

        category_analysis = analytics.get_category_analysis()
        if category_analysis == {}:
            print("✅ get_category_analysis() handles empty data")
        else:
            issues.append("get_category_analysis() doesn't handle empty data correctly")

        hardest = analytics.get_hardest_questions()
        if hardest == []:
            print("✅ get_hardest_questions() handles empty data")
        else:
            issues.append("get_hardest_questions() doesn't handle empty data correctly")

    except Exception as e:
        issues.append(f"Exception during testing: {e}")
        import traceback
        traceback.print_exc()

    if issues:
        print(f"\n❌ FAILED: {len(issues)} issues found")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✅ PASSED: All analytics tests successful")
        return True


if __name__ == '__main__':
    print("\n" + "#"*60)
    print("# MODULE UNIT TEST SUITE")
    print("#"*60)

    results = []

    # Test test_engine
    results.append(('test_engine.py', test_test_engine()))

    # Test email_service
    results.append(('email_service.py', test_email_service()))

    # Test analytics
    results.append(('analytics.py', test_analytics()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")

    print(f"\nResults: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 All module tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")
        sys.exit(1)
