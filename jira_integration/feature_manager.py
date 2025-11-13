"""
Feature Manager for capturing and managing Jira Features
Features are typically Stories with a specific label or custom issue type
"""
import json


class FeatureManager:
    """Manager for Jira Feature operations"""
    
    def __init__(self, jira_client):
        """
        Initialize Feature Manager
        
        Args:
            jira_client: JiraClient instance
        """
        self.client = jira_client
        self.jira = jira_client.jira
    
    def create_feature(self, summary, description=None, epic_key=None, **kwargs):
        """
        Create a new Feature in Jira
        
        Args:
            summary: Feature summary/title
            description: Feature description
            epic_key: Parent epic key (optional)
            **kwargs: Additional fields for the feature
        
        Returns:
            Issue: Created feature issue
        """
        issue_dict = {
            'project': {'key': self.client.config.project_key},
            'summary': summary,
            'issuetype': {'name': 'Story'},
            'labels': ['feature']  # Tag as feature
        }
        
        if description:
            issue_dict['description'] = description
        
        # Link to epic if provided
        if epic_key:
            issue_dict['parent'] = {'key': epic_key}
        
        # Add any additional fields
        issue_dict.update(kwargs)
        
        feature = self.jira.create_issue(fields=issue_dict)
        print(f"Feature created: {feature.key} - {summary}")
        return feature
    
    def get_feature(self, feature_key):
        """
        Get a feature by key
        
        Args:
            feature_key: The feature key (e.g., 'PROJ-123')
        
        Returns:
            Issue: Feature issue object
        """
        return self.jira.issue(feature_key)
    
    def get_all_features(self):
        """
        Get all features in the project
        
        Returns:
            list: List of feature issues
        """
        jql = f'project = {self.client.config.project_key} AND labels = feature ORDER BY created DESC'
        features = self.jira.search_issues(jql, maxResults=1000)
        return features
    
    def get_features_by_epic(self, epic_key):
        """
        Get all features under a specific epic
        
        Args:
            epic_key: The epic key
        
        Returns:
            list: List of feature issues
        """
        jql = f'project = {self.client.config.project_key} AND "Epic Link" = {epic_key} AND labels = feature ORDER BY created DESC'
        features = self.jira.search_issues(jql, maxResults=1000)
        return features
    
    def update_feature(self, feature_key, **fields):
        """
        Update a feature
        
        Args:
            feature_key: The feature key
            **fields: Fields to update
        
        Returns:
            Issue: Updated feature issue
        """
        feature = self.jira.issue(feature_key)
        feature.update(fields=fields)
        print(f"Feature updated: {feature_key}")
        return feature
    
    def get_feature_details(self, feature_key):
        """
        Get detailed information about a feature
        
        Args:
            feature_key: The feature key
        
        Returns:
            dict: Feature details
        """
        feature = self.get_feature(feature_key)
        return {
            'key': feature.key,
            'summary': feature.fields.summary,
            'description': feature.fields.description,
            'status': feature.fields.status.name,
            'created': str(feature.fields.created),
            'updated': str(feature.fields.updated),
            'reporter': feature.fields.reporter.displayName if feature.fields.reporter else None,
            'assignee': feature.fields.assignee.displayName if feature.fields.assignee else None,
            'labels': feature.fields.labels,
        }
    
    def export_features_to_json(self, filename='features.json'):
        """
        Export all features to JSON file
        
        Args:
            filename: Output filename
        """
        features = self.get_all_features()
        features_data = []
        
        for feature in features:
            features_data.append(self.get_feature_details(feature.key))
        
        with open(filename, 'w') as f:
            json.dump(features_data, f, indent=2)
        
        print(f"Exported {len(features_data)} features to {filename}")
        return features_data
