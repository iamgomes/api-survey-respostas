from django.http import JsonResponse, HttpResponse
import http.client
import json
import base64
import pandas as pd
import io
from decouple import config

url = "limesurvey.tce.mt.gov.br"
url_remotecontrol = "/index.php/admin/remotecontrol"
USER=config('USER')
PASSWORD=config('PASSWORD')


def get_session_key(user, password):
    conn = http.client.HTTPSConnection(url)
    payload = json.dumps({
        "method": "get_session_key",
        "params": [
            user,
            password
    ],
    "id": 1
    })
    
    headers = {
    'Content-Type': 'application/json'
    }

    conn.request("POST", url_remotecontrol, payload, headers)
    res = conn.getresponse()
    data = res.read()
    key = json.loads(data)['result']

    return key


def export_responses(key, sid):
    conn = http.client.HTTPSConnection(url)
    payload = json.dumps({
        "method": "export_responses",
        "params": [
            key,
            sid,
            "csv",
            None,
            "complete",
            "code",
            "long"
            ],
    "id": 1
    })

    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", url_remotecontrol, payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)['result']

    decodeRespostas = base64.b64decode(result).decode('UTF-8')

    return decodeRespostas


def lime_respostas(request, sid):
    key = get_session_key(USER, PASSWORD)
    respostas = export_responses(key, sid=sid)
    df = pd.read_csv(io.StringIO(respostas), sep=';')
    data = df.to_dict(orient='list')

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii':False}, status=200)
