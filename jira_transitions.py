import os
import urllib3
import requests
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

session = requests.Session()
session.verify = False

apikey = os.getenv('JIRA_API_KEY')
server = os.getenv('JIRA_SERVER')
options = {'server': server, 'verify': False, 'session': session}
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

jira = JIRA(options, token_auth=apikey)

issue_key = 'ABCD-01234567'
transitions = jira.transitions(issue_key)
for t in transitions:
	print(f'{t['id']} - {t['name']}')
