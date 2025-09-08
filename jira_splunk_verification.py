import os
import urllib3
import requests
from jira import JIRA
from getpass import getpass
from dotenv import load_dotenv
import splunklib.client as client
import splunklib.results as results

load_dotenv()

session = requests.Session()
session.verify = False

apikey = os.getenv('JIRA_API_KEY')
server = os.getenv('JIRA_SERVER')
options = {'server': server, 'verify': False, 'session': session}
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

jira = JIRA(options, token_auth=apikey)

myJQL = 'project = Security AND resolution = unresolved AND "Asset Ownership" in ("Network DevOps", "Network Engineering", "Networking Systems", "Networking Tools and Automation", "Network Operations") AND status not in (Resolved, Closed, Cancelled, "False Positive", "SOC Request", "SOC Verification", "Sec Eng Review", PCE, "PCE Mgmt Review", "PCE SOC REVIEW") AND issuetype in (SecCompliance) AND component = NLR AND "IP Address" is not EMPTY '

issues = jira.search_issues(jql_str=myJQL, maxResults=False)

splunk_host = os.getenv('SPLUNK_SERVER')
splunk_port = 8089  # Default management port
splunk_username = input('Splunk Username: ')
splunk_password = getpass()

service = client.connect(
	host=splunk_host,
	port=splunk_port,
	username=splunk_username,
	password=splunk_password,
	scheme='https',
	verify=False
)

for i in issues:
	issue = jira.issue(i.key)
	hostname = i.fields.customfield_16120

	# query Splunk for device logs
	search_query = f'search sourcetype=cisco_syslog earliest=@d {hostname}'
	job = service.jobs.create(search_query, exec_mode='blocking')
	log_entries = ''
	for result in results.JSONResultsReader(job.results(output_mode='json')):
		if isinstance(result, dict):
			if result["DeviceName"] == hostname:
				log_entries += f'{result["_raw"]}\n'
	if len(log_entries) != 0:
		lines = log_entries.splitlines()
		log_text = "\n".join(lines[:10])
		print(f'Updating {i.key} for {hostname}')
		jira.transition_issue(issue, '11')	# In Progress
		comment_text = f'This device is sending, please check your QRadar server:\n{{code}}\n{log_text}\n{{code}}'
		jira.add_comment(i.key, comment_text)
		jira.transition_issue(issue, '421')	# Resolved
		print('Done')
