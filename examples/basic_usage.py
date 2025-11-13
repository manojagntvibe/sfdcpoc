#!/usr/bin/env python3
"""
Basic usage example for Jira Integration
This script demonstrates how to use the Jira integration to create and manage
epics, features, user stories, and test cases.
"""

import sys
import os

# Add parent directory to path to import jira_integration module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jira_integration import (
    JiraClient,
    EpicManager,
    FeatureManager,
    StoryManager,
    TestCaseManager
)


def main():
    """Main function demonstrating basic Jira integration usage"""
    
    print("=== Jira Integration - Basic Usage Example ===\n")
    
    # Step 1: Initialize Jira Client
    print("1. Initializing Jira Client...")
    try:
        client = JiraClient()
        print("   ✓ Client initialized")
    except ValueError as e:
        print(f"   ✗ Configuration error: {e}")
        print("\n   Please ensure your .env file is configured with:")
        print("   - JIRA_SERVER")
        print("   - JIRA_EMAIL")
        print("   - JIRA_API_TOKEN")
        print("   - JIRA_PROJECT_KEY")
        return
    
    # Step 2: Test Connection
    print("\n2. Testing Jira connection...")
    if client.test_connection():
        print("   ✓ Connection successful")
    else:
        print("   ✗ Connection failed")
        return
    
    # Step 3: Create Managers
    print("\n3. Initializing managers...")
    epic_mgr = EpicManager(client)
    feature_mgr = FeatureManager(client)
    story_mgr = StoryManager(client)
    test_mgr = TestCaseManager(client)
    print("   ✓ All managers initialized")
    
    # Step 4: Create an Epic
    print("\n4. Creating an Epic...")
    try:
        epic = epic_mgr.create_epic(
            summary="SFDC Integration Epic",
            description="This epic covers all work related to Salesforce integration"
        )
        print(f"   ✓ Epic created: {epic.key}")
    except Exception as e:
        print(f"   Note: {str(e)}")
        print("   You may need to adjust issue types or permissions in your Jira project")
        return
    
    # Step 5: Create a Feature
    print("\n5. Creating a Feature...")
    try:
        feature = feature_mgr.create_feature(
            summary="User Authentication Feature",
            description="Implement user authentication with Salesforce SSO",
            epic_key=epic.key
        )
        print(f"   ✓ Feature created: {feature.key}")
    except Exception as e:
        print(f"   Note: {str(e)}")
    
    # Step 6: Create a User Story
    print("\n6. Creating a User Story...")
    try:
        story = story_mgr.create_story(
            summary="As a user, I want to login with Salesforce credentials",
            description="User story for implementing SSO login",
            epic_key=epic.key
        )
        print(f"   ✓ User Story created: {story.key}")
    except Exception as e:
        print(f"   Note: {str(e)}")
    
    # Step 7: Create a Test Case
    print("\n7. Creating a Test Case...")
    try:
        test_case = test_mgr.create_test_case(
            summary="Test SSO Login Flow",
            description="Verify that users can login using Salesforce SSO",
            story_key=story.key if 'story' in locals() else None,
            test_steps=[
                "Navigate to login page",
                "Click on 'Login with Salesforce' button",
                "Enter valid Salesforce credentials",
                "Verify successful login and redirect to dashboard"
            ]
        )
        print(f"   ✓ Test Case created: {test_case.key}")
    except Exception as e:
        print(f"   Note: {str(e)}")
    
    # Step 8: Export data
    print("\n8. Exporting data to JSON...")
    try:
        epic_mgr.export_epics_to_json('output/epics.json')
        story_mgr.export_stories_to_json('output/stories.json')
        test_mgr.export_test_cases_to_json('output/test_cases.json')
        print("   ✓ Data exported successfully")
    except Exception as e:
        print(f"   Note: {str(e)}")
    
    print("\n=== Example completed successfully! ===")
    print(f"\nYou can view the created items in Jira:")
    print(f"  {client.config.server}/browse/{epic.key if 'epic' in locals() else 'PROJECT'}")


if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    main()
