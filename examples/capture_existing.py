#!/usr/bin/env python3
"""
Capture existing Jira items
This script demonstrates how to retrieve and export existing epics, features,
user stories, and test cases from Jira.
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
    """Main function to capture existing Jira items"""
    
    print("=== Capturing Existing Jira Items ===\n")
    
    # Initialize client
    print("Initializing Jira Client...")
    try:
        client = JiraClient()
        if not client.test_connection():
            print("Failed to connect to Jira. Please check your configuration.")
            return
        print("✓ Connected to Jira\n")
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Initialize managers
    epic_mgr = EpicManager(client)
    feature_mgr = FeatureManager(client)
    story_mgr = StoryManager(client)
    test_mgr = TestCaseManager(client)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Capture Epics
    print("Capturing Epics...")
    try:
        epics = epic_mgr.get_all_epics()
        print(f"  Found {len(epics)} epic(s)")
        if epics:
            epic_mgr.export_epics_to_json('output/epics_export.json')
            print("  ✓ Epics exported to output/epics_export.json")
            
            # Show summary
            for epic in epics[:5]:  # Show first 5
                print(f"    - {epic.key}: {epic.fields.summary}")
            if len(epics) > 5:
                print(f"    ... and {len(epics) - 5} more")
    except Exception as e:
        print(f"  Error capturing epics: {e}")
    
    print()
    
    # Capture Features
    print("Capturing Features...")
    try:
        features = feature_mgr.get_all_features()
        print(f"  Found {len(features)} feature(s)")
        if features:
            feature_mgr.export_features_to_json('output/features_export.json')
            print("  ✓ Features exported to output/features_export.json")
            
            # Show summary
            for feature in features[:5]:  # Show first 5
                print(f"    - {feature.key}: {feature.fields.summary}")
            if len(features) > 5:
                print(f"    ... and {len(features) - 5} more")
    except Exception as e:
        print(f"  Error capturing features: {e}")
    
    print()
    
    # Capture User Stories
    print("Capturing User Stories...")
    try:
        stories = story_mgr.get_all_stories()
        print(f"  Found {len(stories)} user stor(ies)")
        if stories:
            story_mgr.export_stories_to_json('output/stories_export.json')
            print("  ✓ Stories exported to output/stories_export.json")
            
            # Show summary
            for story in stories[:5]:  # Show first 5
                print(f"    - {story.key}: {story.fields.summary}")
            if len(stories) > 5:
                print(f"    ... and {len(stories) - 5} more")
    except Exception as e:
        print(f"  Error capturing stories: {e}")
    
    print()
    
    # Capture Test Cases
    print("Capturing Test Cases...")
    try:
        test_cases = test_mgr.get_all_test_cases()
        print(f"  Found {len(test_cases)} test case(s)")
        if test_cases:
            test_mgr.export_test_cases_to_json('output/test_cases_export.json')
            print("  ✓ Test cases exported to output/test_cases_export.json")
            
            # Show summary
            for test_case in test_cases[:5]:  # Show first 5
                print(f"    - {test_case.key}: {test_case.fields.summary}")
            if len(test_cases) > 5:
                print(f"    ... and {len(test_cases) - 5} more")
    except Exception as e:
        print(f"  Error capturing test cases: {e}")
    
    print("\n=== Capture completed! ===")
    print("Check the 'output' directory for exported JSON files.")


if __name__ == "__main__":
    main()
