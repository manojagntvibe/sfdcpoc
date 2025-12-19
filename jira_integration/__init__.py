"""
Jira Integration Module for SFDC POC
Provides functionality to connect to Jira and capture epics, features, user stories, and test cases.
"""

from .jira_client import JiraClient
from .epic_manager import EpicManager
from .feature_manager import FeatureManager
from .story_manager import StoryManager
from .test_case_manager import TestCaseManager

__version__ = "1.0.0"

__all__ = [
    'JiraClient',
    'EpicManager',
    'FeatureManager',
    'StoryManager',
    'TestCaseManager'
]
