import os
import signal
import urllib3
import requests
from jira import JIRA
from dotenv import load_dotenv


signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)    # KeyboardInterrupt: Ctrl-C

load_dotenv()

session = requests.Session()
session.verify = False
urllib3.disable_warnings()

server = os.getenv('JIRA_URL')
apikey = os.getenv('JIRA_API')
options = {'server': server, 'verify': False, 'session': session}
jira = JIRA(options, token_auth=apikey)

myJQL = ''  # <- add your JQL here

filename = ''  # <- define the output file name

batch_size = 1000
start_at = 0
with open(filename, 'a+', buffering=1) as csvfile:
	while True:
		issues = jira.search_issues(jql_str=myJQL, startAt=start_at, maxResults=batch_size, fields='key,customfield_16120')
		print(issues.total)
		try:
			for issue in issues:
				csvfile.write(issue.fields.customfield_16120 + '\n')
		except:
			pass
		total_issues = issues.total
		start_at += batch_size
		if start_at >= total_issues:
			break

jira.close()
