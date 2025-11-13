#!/usr/bin/env python3
"""
Configuration checker for Jira Integration
Run this script to verify your configuration is correct before using the integration.
"""

import os
import sys
from dotenv import load_dotenv


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("\n📝 To fix this:")
        print("   1. Copy .env.example to .env:")
        print("      cp .env.example .env")
        print("   2. Edit .env and add your Jira credentials")
        return False
    print("✅ .env file exists")
    return True


def check_configuration():
    """Check if all required configuration is present"""
    load_dotenv()
    
    required_vars = {
        'JIRA_SERVER': 'Jira server URL (e.g., https://your-domain.atlassian.net)',
        'JIRA_EMAIL': 'Your Jira email address',
        'JIRA_API_TOKEN': 'Your Jira API token',
        'JIRA_PROJECT_KEY': 'Your Jira project key (e.g., PROJ)'
    }
    
    all_present = True
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            print(f"❌ {var} is missing")
            print(f"   Description: {description}")
            missing_vars.append(var)
            all_present = False
        else:
            # Show partial value for security
            if var == 'JIRA_API_TOKEN':
                display_value = value[:8] + '...' if len(value) > 8 else '***'
            else:
                display_value = value
            print(f"✅ {var} = {display_value}")
    
    if missing_vars:
        print(f"\n❌ Missing configuration: {', '.join(missing_vars)}")
        print("\n📝 To fix this, edit your .env file and add the missing values.")
        return False
    
    return all_present


def test_connection():
    """Test connection to Jira"""
    try:
        from jira_integration import JiraClient
        
        print("\n🔗 Testing connection to Jira...")
        client = JiraClient()
        
        if client.test_connection():
            print("✅ Successfully connected to Jira!")
            
            # Get user info
            user = client.jira.myself()
            print(f"   Logged in as: {user.get('displayName', 'Unknown')} ({user.get('emailAddress', 'Unknown')})")
            
            # Get project info
            try:
                project = client.get_project()
                print(f"   Project: {project.name} ({project.key})")
                print(f"   Project URL: {client.config.server}/browse/{project.key}")
            except Exception as e:
                print(f"   ⚠️  Could not access project: {str(e)}")
            
            return True
        else:
            print("❌ Connection failed!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("\n📝 To fix this:")
        print("   Install dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        print("\n📝 Possible issues:")
        print("   - Check your JIRA_SERVER URL")
        print("   - Verify your JIRA_EMAIL is correct")
        print("   - Make sure your API token is valid")
        print("   - Ensure you have access to the project")
        return False


def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = {
        'jira': 'Jira Python library',
        'dotenv': 'python-dotenv library',
        'requests': 'Requests library'
    }
    
    all_installed = True
    
    for package, description in required_packages.items():
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed ({description})")
            all_installed = False
    
    if not all_installed:
        print("\n📝 To install dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    return all_installed


def main():
    """Main function"""
    print("=" * 60)
    print("Jira Integration Configuration Checker")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install dependencies before continuing.")
        sys.exit(1)
    
    print()
    
    # Check .env file
    if not check_env_file():
        sys.exit(1)
    
    print()
    
    # Check configuration
    if not check_configuration():
        sys.exit(1)
    
    # Test connection
    if not test_connection():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! You're ready to use the integration.")
    print("=" * 60)
    print("\n📚 Next steps:")
    print("   - Run examples/basic_usage.py to create sample items")
    print("   - Run examples/capture_existing.py to export existing items")
    print("   - See README.md for full documentation")


if __name__ == "__main__":
    main()
