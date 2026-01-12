"""
Data Validation Tests for questions.json and test_config.json
"""

import json
import sys

def test_questions_json():
    """Validate questions.json structure and content"""
    print("\n" + "="*60)
    print("TESTING: data/questions.json")
    print("="*60)

    issues = []

    try:
        with open('data/questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ File exists and is valid JSON")
    except FileNotFoundError:
        print("❌ File not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False

    # Test test_info section
    if 'test_info' not in data:
        issues.append("Missing 'test_info' section")
    else:
        test_info = data['test_info']
        required_fields = ['title', 'duration_minutes', 'total_questions', 'pass_threshold', 'pass_count']
        for field in required_fields:
            if field not in test_info:
                issues.append(f"Missing test_info.{field}")

        if test_info.get('total_questions') == 27:
            print("✅ test_info.total_questions = 27")
        else:
            issues.append(f"test_info.total_questions = {test_info.get('total_questions')}, expected 27")

        if test_info.get('duration_minutes') == 30:
            print("✅ test_info.duration_minutes = 30")
        else:
            issues.append(f"test_info.duration_minutes = {test_info.get('duration_minutes')}, expected 30")

        if test_info.get('pass_threshold') == 0.48:
            print("✅ test_info.pass_threshold = 0.48")
        else:
            issues.append(f"test_info.pass_threshold = {test_info.get('pass_threshold')}, expected 0.48")

    # Test categories
    if 'categories' not in data:
        issues.append("Missing 'categories' section")
    else:
        categories = data['categories']
        if len(categories) == 5:
            print(f"✅ 5 categories defined: {', '.join(categories)}")
        else:
            issues.append(f"Expected 5 categories, found {len(categories)}")

    # Test questions
    if 'questions' not in data:
        issues.append("Missing 'questions' section")
        print(f"\n❌ FAILED: {len(issues)} issues found")
        for issue in issues:
            print(f"  - {issue}")
        return False

    questions = data['questions']

    if len(questions) == 27:
        print(f"✅ 27 questions present")
    else:
        issues.append(f"Expected 27 questions, found {len(questions)}")

    # Validate each question
    question_ids = set()
    category_counts = {}

    for q in questions:
        q_id = q.get('id')

        # Check ID
        if q_id is None:
            issues.append(f"Question missing 'id' field")
            continue

        if q_id in question_ids:
            issues.append(f"Duplicate question ID: {q_id}")
        question_ids.add(q_id)

        # Check required fields
        if 'category' not in q:
            issues.append(f"Question {q_id} missing 'category'")
        else:
            cat = q['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        if 'question' not in q:
            issues.append(f"Question {q_id} missing 'question' text")

        if 'options' not in q:
            issues.append(f"Question {q_id} missing 'options'")
        else:
            options = q['options']
            if not all(key in options for key in ['a', 'b', 'c', 'd']):
                issues.append(f"Question {q_id} missing one or more options (a, b, c, d)")

        if 'correct_answer' not in q:
            issues.append(f"Question {q_id} missing 'correct_answer'")
        elif q['correct_answer'] not in ['a', 'b', 'c', 'd']:
            issues.append(f"Question {q_id} has invalid correct_answer: {q['correct_answer']}")

        if 'explanation' not in q:
            issues.append(f"Question {q_id} missing 'explanation'")

    # Check ID range
    if question_ids == set(range(1, 28)):
        print("✅ All question IDs 1-27 present and unique")
    else:
        missing = set(range(1, 28)) - question_ids
        if missing:
            issues.append(f"Missing question IDs: {sorted(missing)}")

    # Category distribution
    print(f"\n📊 Category distribution:")
    for cat, count in sorted(category_counts.items()):
        print(f"  - {cat}: {count} questions")

    if issues:
        print(f"\n❌ FAILED: {len(issues)} issues found")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✅ PASSED: All validations successful")
        return True


def test_config_json():
    """Validate test_config.json structure and content"""
    print("\n" + "="*60)
    print("TESTING: data/test_config.json")
    print("="*60)

    issues = []

    try:
        with open('data/test_config.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ File exists and is valid JSON")
    except FileNotFoundError:
        print("❌ File not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False

    # Test test_settings section
    if 'test_settings' not in data:
        issues.append("Missing 'test_settings' section")
    else:
        settings = data['test_settings']
        required = ['test_version', 'duration_minutes', 'total_questions',
                   'pass_threshold_percentage', 'auto_save_interval']
        for field in required:
            if field not in settings:
                issues.append(f"Missing test_settings.{field}")

        if settings.get('duration_minutes') == 30:
            print("✅ test_settings.duration_minutes = 30")

        if settings.get('total_questions') == 27:
            print("✅ test_settings.total_questions = 27")

        if settings.get('pass_threshold_percentage') == 48:
            print("✅ test_settings.pass_threshold_percentage = 48")

        if settings.get('auto_save_interval') == 5:
            print("✅ test_settings.auto_save_interval = 5")

    # Test grading_scale section
    if 'grading_scale' not in data:
        issues.append("Missing 'grading_scale' section")
    else:
        grading = data['grading_scale']
        expected_grades = ['5.0', '4.5', '4.0', '3.5', '3.0', '2.0']

        if set(grading.keys()) == set(expected_grades):
            print(f"✅ All 6 grades defined: {', '.join(expected_grades)}")
        else:
            issues.append(f"Expected grades {expected_grades}, found {list(grading.keys())}")

        for grade, criteria in grading.items():
            if 'min_percentage' not in criteria:
                issues.append(f"Grade {grade} missing 'min_percentage'")
            if 'description' not in criteria:
                issues.append(f"Grade {grade} missing 'description'")

    # Test ui_settings section
    if 'ui_settings' not in data:
        issues.append("Missing 'ui_settings' section")
    else:
        ui = data['ui_settings']
        required = ['show_timer', 'show_progress', 'allow_navigation']
        for field in required:
            if field not in ui:
                issues.append(f"Missing ui_settings.{field}")
        print("✅ ui_settings section complete")

    # Test notifications section
    if 'notifications' not in data:
        issues.append("Missing 'notifications' section")
    else:
        notif = data['notifications']
        required = ['send_email_to_student', 'send_email_to_teacher']
        for field in required:
            if field not in notif:
                issues.append(f"Missing notifications.{field}")
        print("✅ notifications section complete")

    if issues:
        print(f"\n❌ FAILED: {len(issues)} issues found")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✅ PASSED: All validations successful")
        return True


if __name__ == '__main__':
    print("\n" + "#"*60)
    print("# DATA VALIDATION TEST SUITE")
    print("#"*60)

    results = []

    # Test questions.json
    results.append(('questions.json', test_questions_json()))

    # Test test_config.json
    results.append(('test_config.json', test_config_json()))

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
        print("\n🎉 All data validation tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")
        sys.exit(1)
