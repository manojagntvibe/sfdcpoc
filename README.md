# SFDC POC - Jira Integration

A Python-based integration tool for connecting with Jira to capture and manage Epics, Features, User Stories, and Test Cases for Salesforce POC projects.

## Features

- **Jira Integration**: Connect to Jira Cloud or Server instances
- **Epic Management**: Create, retrieve, update, and export epics
- **Feature Management**: Manage features (stories tagged as features)
- **User Story Management**: Handle user stories with full CRUD operations
- **Test Case Management**: Create and manage test cases linked to stories
- **Data Export**: Export all items to JSON format for analysis and reporting

## Prerequisites

- Python 3.7 or higher
- Jira Cloud account or Jira Server access
- Jira API token (for Cloud) or credentials (for Server)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/manojagntvibe/sfdcpoc.git
cd sfdcpoc
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your Jira connection:
```bash
cp .env.example .env
# Edit .env with your Jira credentials
```

## Configuration

Edit the `.env` file with your Jira details:

```env
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token-here
JIRA_PROJECT_KEY=YOUR_PROJECT_KEY
```

### Getting Your Jira API Token

1. Log in to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label and copy the token
4. Use this token in your `.env` file

## Usage

### Basic Usage

Run the basic usage example to create sample items:

```bash
python examples/basic_usage.py
```

This will:
- Connect to Jira
- Create an Epic
- Create a Feature under the Epic
- Create a User Story under the Epic
- Create a Test Case linked to the Story
- Export all items to JSON files

### Capture Existing Items

To retrieve and export existing items from Jira:

```bash
python examples/capture_existing.py
```

This will fetch all epics, features, user stories, and test cases from your Jira project and export them to JSON files in the `output/` directory.

### Programmatic Usage

```python
from jira_integration import (
    JiraClient,
    EpicManager,
    FeatureManager,
    StoryManager,
    TestCaseManager
)

# Initialize client
client = JiraClient()

# Test connection
if client.test_connection():
    print("Connected to Jira!")

# Create managers
epic_mgr = EpicManager(client)
story_mgr = StoryManager(client)
test_mgr = TestCaseManager(client)

# Create an epic
epic = epic_mgr.create_epic(
    summary="My Epic",
    description="Epic description"
)

# Create a user story under the epic
story = story_mgr.create_story(
    summary="As a user, I want to...",
    description="Story description",
    epic_key=epic.key
)

# Create a test case for the story
test_case = test_mgr.create_test_case(
    summary="Test login functionality",
    description="Verify user can login",
    story_key=story.key,
    test_steps=[
        "Open login page",
        "Enter credentials",
        "Click login",
        "Verify dashboard loads"
    ]
)

# Export all epics to JSON
epic_mgr.export_epics_to_json('my_epics.json')
```

## Module Documentation

### JiraClient

Main client for connecting to Jira.

**Methods:**
- `connect()`: Establish connection to Jira
- `test_connection()`: Test if connection is working
- `get_project()`: Get the configured project

### EpicManager

Manager for Epic operations.

**Methods:**
- `create_epic(summary, description, **kwargs)`: Create a new epic
- `get_epic(epic_key)`: Get an epic by key
- `get_all_epics()`: Get all epics in the project
- `update_epic(epic_key, **fields)`: Update an epic
- `get_epic_details(epic_key)`: Get detailed epic information
- `export_epics_to_json(filename)`: Export all epics to JSON

### FeatureManager

Manager for Feature operations (Stories tagged as features).

**Methods:**
- `create_feature(summary, description, epic_key, **kwargs)`: Create a new feature
- `get_feature(feature_key)`: Get a feature by key
- `get_all_features()`: Get all features in the project
- `get_features_by_epic(epic_key)`: Get features under an epic
- `update_feature(feature_key, **fields)`: Update a feature
- `export_features_to_json(filename)`: Export all features to JSON

### StoryManager

Manager for User Story operations.

**Methods:**
- `create_story(summary, description, epic_key, story_points, **kwargs)`: Create a new story
- `get_story(story_key)`: Get a story by key
- `get_all_stories()`: Get all stories in the project
- `get_stories_by_epic(epic_key)`: Get stories under an epic
- `update_story(story_key, **fields)`: Update a story
- `add_comment(story_key, comment_text)`: Add a comment to a story
- `export_stories_to_json(filename)`: Export all stories to JSON

### TestCaseManager

Manager for Test Case operations.

**Methods:**
- `create_test_case(summary, description, story_key, test_steps, **kwargs)`: Create a new test case
- `get_test_case(test_case_key)`: Get a test case by key
- `get_all_test_cases()`: Get all test cases in the project
- `get_test_cases_by_story(story_key)`: Get test cases for a story
- `update_test_case(test_case_key, **fields)`: Update a test case
- `add_test_execution_comment(test_case_key, result, notes)`: Add test execution result
- `export_test_cases_to_json(filename)`: Export all test cases to JSON

## Project Structure

```
sfdcpoc/
├── jira_integration/          # Main integration module
│   ├── __init__.py           # Module initialization
│   ├── config.py             # Configuration management
│   ├── jira_client.py        # Jira client
│   ├── epic_manager.py       # Epic management
│   ├── feature_manager.py    # Feature management
│   ├── story_manager.py      # User story management
│   └── test_case_manager.py  # Test case management
├── examples/                  # Example scripts
│   ├── basic_usage.py        # Basic usage example
│   └── capture_existing.py   # Capture existing items
├── .env.example              # Environment configuration template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue in the GitHub repository.