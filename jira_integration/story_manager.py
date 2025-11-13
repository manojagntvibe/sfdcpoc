"""
Story Manager for capturing and managing Jira User Stories
"""
import json


class StoryManager:
    """Manager for Jira User Story operations"""
    
    def __init__(self, jira_client):
        """
        Initialize Story Manager
        
        Args:
            jira_client: JiraClient instance
        """
        self.client = jira_client
        self.jira = jira_client.jira
    
    def create_story(self, summary, description=None, epic_key=None, story_points=None, **kwargs):
        """
        Create a new User Story in Jira
        
        Args:
            summary: Story summary/title
            description: Story description
            epic_key: Parent epic key (optional)
            story_points: Story points estimation (optional)
            **kwargs: Additional fields for the story
        
        Returns:
            Issue: Created story issue
        """
        issue_dict = {
            'project': {'key': self.client.config.project_key},
            'summary': summary,
            'issuetype': {'name': 'Story'},
        }
        
        if description:
            issue_dict['description'] = description
        
        # Link to epic if provided
        if epic_key:
            issue_dict['parent'] = {'key': epic_key}
        
        # Add story points if provided
        if story_points:
            # Note: Field name may vary by Jira configuration
            issue_dict['customfield_10016'] = story_points
        
        # Add any additional fields
        issue_dict.update(kwargs)
        
        story = self.jira.create_issue(fields=issue_dict)
        print(f"User Story created: {story.key} - {summary}")
        return story
    
    def get_story(self, story_key):
        """
        Get a user story by key
        
        Args:
            story_key: The story key (e.g., 'PROJ-123')
        
        Returns:
            Issue: Story issue object
        """
        return self.jira.issue(story_key)
    
    def get_all_stories(self):
        """
        Get all user stories in the project
        
        Returns:
            list: List of story issues
        """
        jql = f'project = {self.client.config.project_key} AND issuetype = Story AND labels != feature ORDER BY created DESC'
        stories = self.jira.search_issues(jql, maxResults=1000)
        return stories
    
    def get_stories_by_epic(self, epic_key):
        """
        Get all user stories under a specific epic
        
        Args:
            epic_key: The epic key
        
        Returns:
            list: List of story issues
        """
        jql = f'project = {self.client.config.project_key} AND "Epic Link" = {epic_key} AND issuetype = Story ORDER BY created DESC'
        stories = self.jira.search_issues(jql, maxResults=1000)
        return stories
    
    def update_story(self, story_key, **fields):
        """
        Update a user story
        
        Args:
            story_key: The story key
            **fields: Fields to update
        
        Returns:
            Issue: Updated story issue
        """
        story = self.jira.issue(story_key)
        story.update(fields=fields)
        print(f"User Story updated: {story_key}")
        return story
    
    def add_comment(self, story_key, comment_text):
        """
        Add a comment to a user story
        
        Args:
            story_key: The story key
            comment_text: Comment text
        
        Returns:
            Comment: Created comment object
        """
        comment = self.jira.add_comment(story_key, comment_text)
        print(f"Comment added to {story_key}")
        return comment
    
    def get_story_details(self, story_key):
        """
        Get detailed information about a user story
        
        Args:
            story_key: The story key
        
        Returns:
            dict: Story details
        """
        story = self.get_story(story_key)
        return {
            'key': story.key,
            'summary': story.fields.summary,
            'description': story.fields.description,
            'status': story.fields.status.name,
            'created': str(story.fields.created),
            'updated': str(story.fields.updated),
            'reporter': story.fields.reporter.displayName if story.fields.reporter else None,
            'assignee': story.fields.assignee.displayName if story.fields.assignee else None,
            'labels': story.fields.labels,
            'priority': story.fields.priority.name if story.fields.priority else None,
        }
    
    def export_stories_to_json(self, filename='stories.json'):
        """
        Export all user stories to JSON file
        
        Args:
            filename: Output filename
        """
        stories = self.get_all_stories()
        stories_data = []
        
        for story in stories:
            stories_data.append(self.get_story_details(story.key))
        
        with open(filename, 'w') as f:
            json.dump(stories_data, f, indent=2)
        
        print(f"Exported {len(stories_data)} user stories to {filename}")
        return stories_data
