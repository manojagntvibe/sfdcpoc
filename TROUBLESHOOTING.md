# Troubleshooting Guide

This guide covers common issues and their solutions when using the Jira integration.

## Connection Issues

### Error: "Missing required configuration"

**Problem:** Your `.env` file is missing or incomplete.

**Solution:**
1. Make sure you have a `.env` file in the project root
2. Verify it contains all required variables:
   ```env
   JIRA_SERVER=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token-here
   JIRA_PROJECT_KEY=YOUR_PROJECT_KEY
   ```
3. Check that there are no extra spaces or quotes around the values

### Error: "401 Unauthorized" or "Authentication failed"

**Problem:** Your API token or email is incorrect.

**Solution:**
1. Verify your email address is correct
2. Generate a new API token:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Create a new token
   - Update your `.env` file with the new token
3. Make sure there are no spaces in your API token

### Error: "404 Not Found" when accessing project

**Problem:** The project key is incorrect or you don't have access.

**Solution:**
1. Verify the project key in Jira
2. Make sure you have access to the project
3. Check that the project key is in uppercase (e.g., `PROJ`, not `proj`)

## Issue Creation Problems

### Error: "Field 'issuetype' does not exist or you do not have permission"

**Problem:** The issue type (Epic, Story, Task) doesn't exist in your project.

**Solution:**
1. Go to your Jira project settings
2. Check available issue types
3. Modify the code to use available issue types
4. For Epics, some Jira projects require the "Epic" issue type to be enabled

### Error: "Epic link field not found"

**Problem:** Your Jira project doesn't have the Epic Link field configured.

**Solution:**
1. Use parent-child relationships instead:
   ```python
   issue_dict['parent'] = {'key': epic_key}
   ```
2. Or use custom epic link fields if your Jira configuration requires it

### Error: "customfield_10016 does not exist"

**Problem:** The story points field ID is different in your Jira instance.

**Solution:**
1. Find the correct field ID:
   ```python
   from jira_integration import JiraClient
   
   client = JiraClient()
   fields = client.jira.fields()
   for field in fields:
       if 'story' in field['name'].lower() or 'point' in field['name'].lower():
           print(f"{field['name']}: {field['id']}")
   ```
2. Update the field ID in `story_manager.py`

## Import Errors

### Error: "ModuleNotFoundError: No module named 'jira'"

**Problem:** Dependencies not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Problem:** python-dotenv not installed.

**Solution:**
```bash
pip install python-dotenv
```

## Export Issues

### Error: "FileNotFoundError: [Errno 2] No such file or directory: 'output/epics.json'"

**Problem:** The output directory doesn't exist.

**Solution:**
```python
import os
os.makedirs('output', exist_ok=True)
```

Or run from the project root:
```bash
cd /path/to/sfdcpoc
python examples/basic_usage.py
```

## Performance Issues

### Slow queries when fetching many issues

**Problem:** Default max results might be too high or Jira is slow.

**Solution:**
1. Use pagination:
   ```python
   jql = "project = PROJ AND issuetype = Epic"
   start = 0
   max_results = 50
   
   while True:
       issues = jira.search_issues(jql, startAt=start, maxResults=max_results)
       if not issues:
           break
       # Process issues
       start += max_results
   ```

2. Add filters to your JQL queries:
   ```python
   jql = "project = PROJ AND issuetype = Epic AND created >= -30d"
   ```

## API Rate Limiting

### Error: "429 Too Many Requests"

**Problem:** You've exceeded Jira's rate limits.

**Solution:**
1. Add delays between requests:
   ```python
   import time
   time.sleep(1)  # Wait 1 second between requests
   ```

2. Reduce the number of concurrent requests
3. Cache results when possible

## SSL/Certificate Issues

### Error: "SSLError" or certificate verification failed

**Problem:** SSL certificate verification issues.

**Solution:**
1. For development/testing only (NOT recommended for production):
   ```python
   import os
   os.environ['REQUESTS_CA_BUNDLE'] = ''
   ```

2. Better solution - update certificates:
   ```bash
   pip install --upgrade certifi
   ```

## Debugging Tips

### Enable debug logging

Add this to your script to see detailed API calls:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('jira')
logger.setLevel(logging.DEBUG)
```

### Test JQL queries in Jira

Before using JQL in your code:
1. Go to Jira → Filters → Advanced search
2. Test your JQL query
3. Verify it returns expected results
4. Then use it in your code

### Inspect issue fields

To see all available fields for an issue:

```python
from jira_integration import JiraClient

client = JiraClient()
issue = client.jira.issue('PROJ-123')

print("Available fields:")
for field, value in issue.raw['fields'].items():
    print(f"  {field}: {value}")
```

## Common JQL Mistakes

### Wrong project key

```python
# ✗ Wrong
jql = "project = proj AND issuetype = Epic"

# ✓ Correct
jql = "project = PROJ AND issuetype = Epic"
```

### Incorrect field names

```python
# ✗ Wrong
jql = "project = PROJ AND epiclink = PROJ-123"

# ✓ Correct
jql = 'project = PROJ AND "Epic Link" = PROJ-123'
```

### Missing quotes for multi-word fields

```python
# ✗ Wrong
jql = "project = PROJ AND Epic Link = PROJ-123"

# ✓ Correct
jql = 'project = PROJ AND "Epic Link" = PROJ-123'
```

## Still Having Issues?

If you're still experiencing problems:

1. Check the [Jira REST API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
2. Review the [jira-python library docs](https://jira.readthedocs.io/)
3. Enable debug logging (see above)
4. Open an issue on GitHub with:
   - Error message
   - Python version
   - Jira version (Cloud/Server)
   - Minimal code to reproduce the issue
