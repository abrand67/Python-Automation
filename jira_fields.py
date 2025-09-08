import os
import signal
import requests
from jira import JIRA
from dotenv import load_dotenv

signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)    # KeyboardInterrupt: Ctrl-C
requests.packages.urllib3.disable_warnings()

load_dotenv()

apikey = os.getenv('JIRA_API_KEY')
jiraurl = os.getenv('JIRA_SERVER')
jira_options={'verify': False, 'server': jiraurl}
jira = JIRA(jira_options, token_auth=apikey)

ticket = 'ABC-1234567'
issue = jira.issue(ticket)

for field_name in issue.raw['fields']:
    print("Field:", field_name, "Value:", issue.raw['fields'][field_name])
