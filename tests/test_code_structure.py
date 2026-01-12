"""
Code Structure Validation Tests
Tests module structure, imports, and class/function definitions without executing
"""

import os
import re
import ast

def test_file_structure():
    """Test that all required files exist"""
    print("\n" + "="*60)
    print("TESTING: File Structure")
    print("="*60)

    required_files = [
        'app.py',
        'data/questions.json',
        'data/test_config.json',
        'modules/__init__.py',
        'modules/auth.py',
        'modules/sheets_manager.py',
        'modules/test_engine.py',
        'modules/email_service.py',
        'modules/analytics.py',
        'modules/ui_components.py',
        'pages/1_Logowanie_Studenta.py',
        'pages/2_Test_Studenta.py',
        'pages/3_Wyniki_Studenta.py',
        'pages/4_Panel_Nauczyciela.py',
        'pages/5_Dashboard_Nauczyciela.py',
        'pages/6_Szczegoly_Studenta.py',
    ]

    missing = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing.append(file_path)

    if missing:
        print(f"\n❌ FAILED: {len(missing)} files missing")
        return False
    else:
        print(f"\n✅ PASSED: All required files present")
        return True


def test_module_structure(module_path, expected_classes=None, expected_functions=None):
    """Test a Python module's structure"""
    print(f"\n📄 Testing: {module_path}")

    if not os.path.exists(module_path):
        print(f"❌ File not found")
        return False

    issues = []

    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the AST
        tree = ast.parse(content)

        # Find classes
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        # Find functions (top-level only)
        functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]

        # Check expected classes
        if expected_classes:
            for cls in expected_classes:
                if cls in classes:
                    print(f"  ✅ Class {cls} found")
                else:
                    issues.append(f"Class {cls} missing")

        # Check expected functions
        if expected_functions:
            for func in expected_functions:
                if func in functions:
                    print(f"  ✅ Function {func} found")
                else:
                    issues.append(f"Function {func} missing")

        # Check for docstrings
        if ast.get_docstring(tree):
            print(f"  ✅ Module docstring present")
        else:
            issues.append("Module docstring missing")

        # Check imports
        imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
        if imports:
            print(f"  ✅ {len(imports)} import statements")
        else:
            issues.append("No imports found")

    except SyntaxError as e:
        issues.append(f"Syntax error: {e}")

    except Exception as e:
        issues.append(f"Error parsing: {e}")

    if issues:
        print(f"  ❌ {len(issues)} issues:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print(f"  ✅ Structure valid")
        return True


def test_test_engine_structure():
    """Test test_engine.py structure"""
    print("\n" + "="*60)
    print("TESTING: modules/test_engine.py Structure")
    print("="*60)

    expected_classes = ['TestEngine']
    expected_methods = [
        '__init__',
        '_load_questions',
        '_load_config',
        'initialize_test',
        'get_question',
        'get_total_questions',
        'save_answer',
        'get_answer',
        'get_time_remaining',
        'is_time_up',
        'format_time',
        'get_answered_count',
        'should_auto_save',
        'mark_auto_saved',
        'calculate_results',
        '_calculate_grade',
        'format_results_for_sheets',
        'get_progress_percentage'
    ]

    result = test_module_structure('modules/test_engine.py', expected_classes=expected_classes)

    # Check for specific methods in TestEngine class
    try:
        with open('modules/test_engine.py', 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'TestEngine':
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                missing_methods = []
                for method in expected_methods:
                    if method in methods:
                        print(f"  ✅ Method {method}() found")
                    else:
                        missing_methods.append(method)

                if missing_methods:
                    print(f"  ❌ Missing methods: {', '.join(missing_methods)}")
                    return False

    except Exception as e:
        print(f"  ❌ Error checking methods: {e}")
        return False

    return result


def test_email_service_structure():
    """Test email_service.py structure"""
    print("\n" + "="*60)
    print("TESTING: modules/email_service.py Structure")
    print("="*60)

    expected_classes = ['EmailService']
    return test_module_structure('modules/email_service.py', expected_classes=expected_classes)


def test_analytics_structure():
    """Test analytics.py structure"""
    print("\n" + "="*60)
    print("TESTING: modules/analytics.py Structure")
    print("="*60)

    expected_classes = ['Analytics']
    return test_module_structure('modules/analytics.py', expected_classes=expected_classes)


def test_sheets_manager_structure():
    """Test sheets_manager.py structure"""
    print("\n" + "="*60)
    print("TESTING: modules/sheets_manager.py Structure")
    print("="*60)

    expected_classes = ['SheetsManager']
    expected_functions = ['retry_on_failure']
    return test_module_structure('modules/sheets_manager.py',
                                 expected_classes=expected_classes,
                                 expected_functions=expected_functions)


def test_auth_structure():
    """Test auth.py structure"""
    print("\n" + "="*60)
    print("TESTING: modules/auth.py Structure")
    print("="*60)

    expected_classes = ['AuthManager']
    return test_module_structure('modules/auth.py', expected_classes=expected_classes)


def test_pages_structure():
    """Test that all pages have proper structure"""
    print("\n" + "="*60)
    print("TESTING: Pages Structure")
    print("="*60)

    pages = [
        'app.py',
        'pages/1_Logowanie_Studenta.py',
        'pages/2_Test_Studenta.py',
        'pages/3_Wyniki_Studenta.py',
        'pages/4_Panel_Nauczyciela.py',
        'pages/5_Dashboard_Nauczyciela.py',
        'pages/6_Szczegoly_Studenta.py',
    ]

    results = []

    for page in pages:
        if os.path.exists(page):
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for st.set_page_config (except app.py)
            has_config = 'st.set_page_config' in content
            # Check for streamlit import
            has_import = 'import streamlit' in content

            if has_import:
                print(f"✅ {page}: Streamlit imported")
                results.append(True)
            else:
                print(f"❌ {page}: Streamlit import missing")
                results.append(False)

            if page != 'app.py' and not has_config:
                print(f"⚠️  {page}: st.set_page_config missing (optional)")

        else:
            print(f"❌ {page}: File not found")
            results.append(False)

    return all(results)


if __name__ == '__main__':
    print("\n" + "#"*60)
    print("# CODE STRUCTURE VALIDATION SUITE")
    print("#"*60)

    results = []

    # Test file structure
    results.append(('File Structure', test_file_structure()))

    # Test module structures
    results.append(('test_engine.py', test_test_engine_structure()))
    results.append(('email_service.py', test_email_service_structure()))
    results.append(('analytics.py', test_analytics_structure()))
    results.append(('sheets_manager.py', test_sheets_manager_structure()))
    results.append(('auth.py', test_auth_structure()))

    # Test pages
    results.append(('Pages', test_pages_structure()))

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
        print("\n🎉 All code structure tests passed!")
        exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")
        exit(1)
