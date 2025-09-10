import os
import requests
from dotenv import load_dotenv

requests.packages.urllib3.disable_warnings()

load_dotenv()

ipam_appid = os.getenv('IPAM_APPID')
ipam_user = os.getenv('IPAM_USER')
ipam_pass = os.getenv('IPAM_PASS')

def get_ipam_token():
    url = 'https://ipam.{DOMAIN}.local/api/{}/user/token'.format(ipam_appid)
    response = requests.post(url, auth=(ipam_user, ipam_pass), verify=False)
    response = response.json()
    token = response.get('data', {}).get('token', '')
    if token:
        return str(token)
    response.update({'ERROR': 'Unable to retrieve IPAM token'})
    msg = json.dumps(response, indent=4, sort_keys=True)
    raise SystemExit(msg)

def get_ipam_dict(ip):
    ipam_token = get_ipam_token()
    ret = {}
    try:
        url = 'https://ipam.{DOMAIN}.local/api/{}/addresses/search/{}'.format(ipam_appid, ip)
        response = requests.get(url, headers={'token': ipam_token}, verify=False)
        res = response.json()
        if res.get('success') == True:
            ret = res.get('data')[0]
    except Exception as e:
        ret['error'] = 'ERROR:','IPAM stuff broke.. ERROR:{}'.format(str(e))
    return ret

if __name__ == "__main__":
	ip = input('Enter IP address: ')
	obj = get_ipam_dict(ip)
	print(f'{obj.get('ip')}\n{obj.get('hostname')}\n{obj.get('owner')}')
