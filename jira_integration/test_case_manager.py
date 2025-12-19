"""
Test Case Manager for capturing and managing Jira Test Cases
Test cases can be created as Task issues with 'test-case' label or using Xray/Zephyr if available
"""
import json


class TestCaseManager:
    """Manager for Jira Test Case operations"""
    
    def __init__(self, jira_client):
        """
        Initialize Test Case Manager
        
        Args:
            jira_client: JiraClient instance
        """
        self.client = jira_client
        self.jira = jira_client.jira
    
    def create_test_case(self, summary, description=None, story_key=None, test_steps=None, **kwargs):
        """
        Create a new Test Case in Jira
        
        Args:
            summary: Test case summary/title
            description: Test case description
            story_key: Parent story key (optional)
            test_steps: Test steps as a list or string (optional)
            **kwargs: Additional fields for the test case
        
        Returns:
            Issue: Created test case issue
        """
        issue_dict = {
            'project': {'key': self.client.config.project_key},
            'summary': summary,
            'issuetype': {'name': 'Task'},
            'labels': ['test-case']
        }
        
        # Build description with test steps
        full_description = description or ''
        if test_steps:
            if isinstance(test_steps, list):
                steps_text = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(test_steps)])
            else:
                steps_text = test_steps
            full_description += f"\n\n*Test Steps:*\n{steps_text}"
        
        if full_description:
            issue_dict['description'] = full_description
        
        # Link to story if provided
        if story_key:
            issue_dict['parent'] = {'key': story_key}
        
        # Add any additional fields
        issue_dict.update(kwargs)
        
        test_case = self.jira.create_issue(fields=issue_dict)
        print(f"Test Case created: {test_case.key} - {summary}")
        
        # Link to story as 'tests' if story_key provided
        if story_key:
            try:
                self.jira.create_issue_link(
                    type="Tests",
                    inwardIssue=test_case.key,
                    outwardIssue=story_key
                )
            except Exception as e:
                print(f"Note: Could not create 'Tests' link: {str(e)}")
        
        return test_case
    
    def get_test_case(self, test_case_key):
        """
        Get a test case by key
        
        Args:
            test_case_key: The test case key (e.g., 'PROJ-123')
        
        Returns:
            Issue: Test case issue object
        """
        return self.jira.issue(test_case_key)
    
    def get_all_test_cases(self):
        """
        Get all test cases in the project
        
        Returns:
            list: List of test case issues
        """
        jql = f'project = {self.client.config.project_key} AND labels = test-case ORDER BY created DESC'
        test_cases = self.jira.search_issues(jql, maxResults=1000)
        return test_cases
    
    def get_test_cases_by_story(self, story_key):
        """
        Get all test cases linked to a specific story
        
        Args:
            story_key: The story key
        
        Returns:
            list: List of test case issues
        """
        jql = f'project = {self.client.config.project_key} AND labels = test-case AND "Epic Link" = {story_key} ORDER BY created DESC'
        test_cases = self.jira.search_issues(jql, maxResults=1000)
        return test_cases
    
    def update_test_case(self, test_case_key, **fields):
        """
        Update a test case
        
        Args:
            test_case_key: The test case key
            **fields: Fields to update
        
        Returns:
            Issue: Updated test case issue
        """
        test_case = self.jira.issue(test_case_key)
        test_case.update(fields=fields)
        print(f"Test Case updated: {test_case_key}")
        return test_case
    
    def add_test_execution_comment(self, test_case_key, result, notes=None):
        """
        Add a test execution result as a comment
        
        Args:
            test_case_key: The test case key
            result: Test result (e.g., 'Passed', 'Failed', 'Blocked')
            notes: Additional notes (optional)
        
        Returns:
            Comment: Created comment object
        """
        comment_text = f"*Test Execution Result:* {result}"
        if notes:
            comment_text += f"\n\n*Notes:* {notes}"
        
        comment = self.jira.add_comment(test_case_key, comment_text)
        print(f"Test execution result added to {test_case_key}: {result}")
        return comment
    
    def get_test_case_details(self, test_case_key):
        """
        Get detailed information about a test case
        
        Args:
            test_case_key: The test case key
        
        Returns:
            dict: Test case details
        """
        test_case = self.get_test_case(test_case_key)
        return {
            'key': test_case.key,
            'summary': test_case.fields.summary,
            'description': test_case.fields.description,
            'status': test_case.fields.status.name,
            'created': str(test_case.fields.created),
            'updated': str(test_case.fields.updated),
            'reporter': test_case.fields.reporter.displayName if test_case.fields.reporter else None,
            'assignee': test_case.fields.assignee.displayName if test_case.fields.assignee else None,
            'labels': test_case.fields.labels,
            'priority': test_case.fields.priority.name if test_case.fields.priority else None,
        }
    
    def export_test_cases_to_json(self, filename='test_cases.json'):
        """
        Export all test cases to JSON file
        
        Args:
            filename: Output filename
        """
        test_cases = self.get_all_test_cases()
        test_cases_data = []
        
        for test_case in test_cases:
            test_cases_data.append(self.get_test_case_details(test_case.key))
        
        with open(filename, 'w') as f:
            json.dump(test_cases_data, f, indent=2)
        
        print(f"Exported {len(test_cases_data)} test cases to {filename}")
        return test_cases_data
