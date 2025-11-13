"""
Configuration module for Jira integration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class JiraConfig:
    """Configuration class for Jira connection"""
    
    def __init__(self):
        self.server = os.getenv('JIRA_SERVER')
        self.email = os.getenv('JIRA_EMAIL')
        self.api_token = os.getenv('JIRA_API_TOKEN')
        self.project_key = os.getenv('JIRA_PROJECT_KEY')
    
    def validate(self):
        """Validate that all required configuration is present"""
        missing = []
        if not self.server:
            missing.append('JIRA_SERVER')
        if not self.email:
            missing.append('JIRA_EMAIL')
        if not self.api_token:
            missing.append('JIRA_API_TOKEN')
        if not self.project_key:
            missing.append('JIRA_PROJECT_KEY')
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True
