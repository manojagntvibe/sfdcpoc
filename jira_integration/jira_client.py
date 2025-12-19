"""
Jira Client module for managing connection to Jira
"""
from jira import JIRA
from .config import JiraConfig


class JiraClient:
    """Client for connecting to Jira and managing the connection"""
    
    def __init__(self, config=None):
        """
        Initialize Jira client
        
        Args:
            config: JiraConfig object, if None will create one from environment
        """
        self.config = config or JiraConfig()
        self.config.validate()
        self._jira = None
    
    def connect(self):
        """
        Establish connection to Jira
        
        Returns:
            JIRA: Connected Jira instance
        """
        if self._jira is None:
            self._jira = JIRA(
                server=self.config.server,
                basic_auth=(self.config.email, self.config.api_token)
            )
        return self._jira
    
    @property
    def jira(self):
        """
        Get the Jira connection instance
        
        Returns:
            JIRA: Connected Jira instance
        """
        if self._jira is None:
            self.connect()
        return self._jira
    
    def test_connection(self):
        """
        Test the Jira connection
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            self.jira.myself()
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False
    
    def get_project(self):
        """
        Get the configured project
        
        Returns:
            Project: Jira project object
        """
        return self.jira.project(self.config.project_key)
