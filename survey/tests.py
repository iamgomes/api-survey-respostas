from django.test import TestCase
import requests
import json


url = "https://limesurvey.tce.mt.gov.br/index.php/admin/remotecontrol/"

payload = json.dumps({
    "method": "get_session_key",
    "params": [
        "wgomes",
        "tcemt@2022"
        ],
"id": 1
})

headers = {
'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)