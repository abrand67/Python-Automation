from jira import JIRA
from alive_progress import alive_bar
from dotenv import load_dotenv
import urllib3
import os

urllib3.disable_warnings()

load_dotenv()

apikey = os.getenv('JIRA_API')
server = os.getenv('JIRA_URL')
options = {'server': server, 'verify': False}

jira = JIRA(options, token_auth=apikey)

myJQL = ''  # <- JQL of tickets needing to be linked
issues = jira.search_issues(jql_str=myJQL, fields='key', maxResults=0)

parent_issue=''  # <- list the main Jira issue key

with alive_bar(len(issues)) as bar:
        for issue in issues:
                bar.title = f'Linking {issue.key}'
                issue = jira.issue(issue)
                data = {
                        "type": {"name": "is addressed by"},
                        "inwardIssue": {"key": str(issue.key)},
                        "outwardIssue": {"key": parent_issue}
                }
                jira.create_issue_link(type="is addressed by", inwardIssue=str(issue.key), outwardIssue=parent_issue)
                bar()

jira.close()
