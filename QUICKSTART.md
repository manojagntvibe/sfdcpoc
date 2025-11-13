# Quick Start Guide

This guide will help you get up and running with the Jira integration in just a few minutes.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Jira Connection

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Jira credentials:

```env
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token-here
JIRA_PROJECT_KEY=YOUR_PROJECT_KEY
```

### How to Get Your API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**
3. Give it a name (e.g., "SFDC POC Integration")
4. Copy the token and paste it into your `.env` file

### Finding Your Project Key

1. Go to your Jira project
2. Look at the URL: `https://your-domain.atlassian.net/browse/PROJ-123`
3. The project key is the part before the dash (e.g., `PROJ`)

## Step 3: Test the Connection

Create a simple test script:

```python
from jira_integration import JiraClient

client = JiraClient()
if client.test_connection():
    print("✓ Connected to Jira successfully!")
    print(f"Project: {client.get_project().name}")
else:
    print("✗ Connection failed. Check your credentials.")
```

## Step 4: Try the Examples

### Create Sample Items

```bash
python examples/basic_usage.py
```

This will create:
- 1 Epic
- 1 Feature under the Epic
- 1 User Story under the Epic
- 1 Test Case linked to the Story

### Capture Existing Items

```bash
python examples/capture_existing.py
```

This will export all existing epics, features, stories, and test cases to JSON files in the `output/` directory.

## Step 5: Use in Your Own Code

```python
from jira_integration import (
    JiraClient,
    EpicManager,
    StoryManager,
    TestCaseManager
)

# Initialize
client = JiraClient()
epic_mgr = EpicManager(client)
story_mgr = StoryManager(client)

# Create an epic
epic = epic_mgr.create_epic(
    summary="Customer Portal",
    description="Build a customer-facing portal"
)

# Create a story under the epic
story = story_mgr.create_story(
    summary="As a customer, I want to view my orders",
    epic_key=epic.key
)

# Export to JSON
epic_mgr.export_epics_to_json('my_epics.json')
```

## Common Tasks

### Create an Epic

```python
from jira_integration import JiraClient, EpicManager

client = JiraClient()
epic_mgr = EpicManager(client)

epic = epic_mgr.create_epic(
    summary="My Epic Title",
    description="Detailed description of the epic"
)
print(f"Created: {epic.key}")
```

### Create a User Story

```python
from jira_integration import JiraClient, StoryManager

client = JiraClient()
story_mgr = StoryManager(client)

story = story_mgr.create_story(
    summary="As a user, I want to...",
    description="Acceptance criteria:\n- Criterion 1\n- Criterion 2",
    epic_key="PROJ-123"  # Optional: link to an epic
)
```

### Create a Test Case

```python
from jira_integration import JiraClient, TestCaseManager

client = JiraClient()
test_mgr = TestCaseManager(client)

test_case = test_mgr.create_test_case(
    summary="Test Login Functionality",
    description="Verify users can login with valid credentials",
    story_key="PROJ-124",  # Optional: link to a story
    test_steps=[
        "Navigate to login page",
        "Enter valid username and password",
        "Click Login button",
        "Verify dashboard is displayed"
    ]
)
```

### Export All Items

```python
from jira_integration import JiraClient, EpicManager, StoryManager, TestCaseManager

client = JiraClient()

# Export epics
epic_mgr = EpicManager(client)
epic_mgr.export_epics_to_json('epics.json')

# Export stories
story_mgr = StoryManager(client)
story_mgr.export_stories_to_json('stories.json')

# Export test cases
test_mgr = TestCaseManager(client)
test_mgr.export_test_cases_to_json('test_cases.json')
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check the [examples/](examples/) directory for more examples
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if you encounter issues

## Need Help?

- Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide
- Open an issue on GitHub
- Review the Jira Python library documentation: https://jira.readthedocs.io/
