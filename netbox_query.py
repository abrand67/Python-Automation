import os
import signal
import urllib3
import requests
import pynetbox
from dotenv import load_dotenv

signal.signal(signal.SIGPIPE, signal.SIG_DFL)
signal.signal(signal.SIGINT, signal.SIG_DFL)

load_dotenv()

urllib3.disable_warnings()
session = requests.Session()
session.verify = False

nb_url = os.getenv('NETBOX_URL')
nb_api = os.getenv('NETBOX_API')
nb = pynetbox.api(url=nb_url, token=nb_api, threading=True)
nb.http_session = session
nb.http_session.verify = False

nb_devs = nb.dcim.devices.filter(status=1, manufacturer_id=3, has_primary_ip=True, platform=['ios', 'iosxr'])
for i in nb_devs:
        print(i.name)
