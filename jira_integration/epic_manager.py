"""
Epic Manager for capturing and managing Jira Epics
"""
import json


class EpicManager:
    """Manager for Jira Epic operations"""
    
    def __init__(self, jira_client):
        """
        Initialize Epic Manager
        
        Args:
            jira_client: JiraClient instance
        """
        self.client = jira_client
        self.jira = jira_client.jira
    
    def create_epic(self, summary, description=None, **kwargs):
        """
        Create a new Epic in Jira
        
        Args:
            summary: Epic summary/title
            description: Epic description
            **kwargs: Additional fields for the epic
        
        Returns:
            Issue: Created epic issue
        """
        issue_dict = {
            'project': {'key': self.client.config.project_key},
            'summary': summary,
            'issuetype': {'name': 'Epic'},
        }
        
        if description:
            issue_dict['description'] = description
        
        # Add any additional fields
        issue_dict.update(kwargs)
        
        epic = self.jira.create_issue(fields=issue_dict)
        print(f"Epic created: {epic.key} - {summary}")
        return epic
    
    def get_epic(self, epic_key):
        """
        Get an epic by key
        
        Args:
            epic_key: The epic key (e.g., 'PROJ-123')
        
        Returns:
            Issue: Epic issue object
        """
        return self.jira.issue(epic_key)
    
    def get_all_epics(self):
        """
        Get all epics in the project
        
        Returns:
            list: List of epic issues
        """
        jql = f'project = {self.client.config.project_key} AND issuetype = Epic ORDER BY created DESC'
        epics = self.jira.search_issues(jql, maxResults=1000)
        return epics
    
    def update_epic(self, epic_key, **fields):
        """
        Update an epic
        
        Args:
            epic_key: The epic key
            **fields: Fields to update
        
        Returns:
            Issue: Updated epic issue
        """
        epic = self.jira.issue(epic_key)
        epic.update(fields=fields)
        print(f"Epic updated: {epic_key}")
        return epic
    
    def get_epic_details(self, epic_key):
        """
        Get detailed information about an epic
        
        Args:
            epic_key: The epic key
        
        Returns:
            dict: Epic details
        """
        epic = self.get_epic(epic_key)
        return {
            'key': epic.key,
            'summary': epic.fields.summary,
            'description': epic.fields.description,
            'status': epic.fields.status.name,
            'created': str(epic.fields.created),
            'updated': str(epic.fields.updated),
            'reporter': epic.fields.reporter.displayName if epic.fields.reporter else None,
            'assignee': epic.fields.assignee.displayName if epic.fields.assignee else None,
        }
    
    def export_epics_to_json(self, filename='epics.json'):
        """
        Export all epics to JSON file
        
        Args:
            filename: Output filename
        """
        epics = self.get_all_epics()
        epics_data = []
        
        for epic in epics:
            epics_data.append(self.get_epic_details(epic.key))
        
        with open(filename, 'w') as f:
            json.dump(epics_data, f, indent=2)
        
        print(f"Exported {len(epics_data)} epics to {filename}")
        return epics_data
