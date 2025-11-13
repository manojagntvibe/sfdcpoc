#!/usr/bin/env python3
"""
Simple integration test script
Tests basic functionality without creating any issues in Jira
"""

import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from jira_integration import (
            JiraClient,
            EpicManager,
            FeatureManager,
            StoryManager,
            TestCaseManager
        )
        print("  ✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    try:
        from jira_integration.config import JiraConfig
        config = JiraConfig()
        
        # Check if config values are loaded (even if not valid)
        has_server = config.server is not None
        has_email = config.email is not None
        has_token = config.api_token is not None
        has_project = config.project_key is not None
        
        if has_server and has_email and has_token and has_project:
            print("  ✅ Configuration loaded")
            print(f"     Server: {config.server}")
            print(f"     Project: {config.project_key}")
            return True
        else:
            print("  ⚠️  Configuration incomplete")
            print("     Run 'python check_config.py' for details")
            return False
            
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def test_connection():
    """Test connection to Jira (read-only)"""
    print("\nTesting Jira connection...")
    try:
        from jira_integration import JiraClient
        
        client = JiraClient()
        if client.test_connection():
            print("  ✅ Connected to Jira successfully")
            
            # Try to get project info
            try:
                project = client.get_project()
                print(f"     Project: {project.name} ({project.key})")
            except Exception as e:
                print(f"     ⚠️  Could not access project: {str(e)}")
            
            return True
        else:
            print("  ❌ Connection failed")
            print("     Run 'python check_config.py' for details")
            return False
            
    except Exception as e:
        print(f"  ❌ Connection error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Jira Integration Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test configuration
    results.append(("Configuration", test_config()))
    
    # Test connection (only if config passed)
    if results[-1][1]:
        results.append(("Connection", test_connection()))
    else:
        print("\nSkipping connection test due to configuration issues")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20s}: {status}")
    
    print()
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! Your integration is ready to use.")
        print("\n📚 Next steps:")
        print("   - Run 'python examples/basic_usage.py' to create sample items")
        print("   - Run 'python examples/capture_existing.py' to export existing items")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please fix the issues and try again.")
        print("   - Run 'python check_config.py' for detailed configuration check")
        sys.exit(1)


if __name__ == "__main__":
    main()
