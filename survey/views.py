from django.http import JsonResponse, HttpResponse
import requests
import json
import base64
import pandas as pd
import io
from decouple import config
import urllib3
urllib3.disable_warnings()

url = "https://limesurvey.tce.mt.gov.br/index.php/admin/remotecontrol"
USER=config('USER')
PASSWORD=config('PASSWORD')


def get_session_key(user, password):
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

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    data = response.json()['result']

    return data


def export_responses(key, sid):
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
    
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    data = response.json()['result']

    return base64.b64decode(data).decode('UTF-8')


def list_participants(key, sid):
    payload = json.dumps({
        "method": "list_participants",
        "params": [
            key,
            sid,
            1,
            20
            ],
        "id": 1
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    data = response.json()['result']

    return data


def sessao(request):
    se = get_session_key(USER, PASSWORD)

    return HttpResponse(se)
    

def lime_respostas(request, sid):
    key = get_session_key(USER, PASSWORD)
    respostas = export_responses(key, sid=sid)
    df = pd.read_csv(io.StringIO(respostas), sep=';')
    data = df.to_dict(orient='list')

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii':False}, status=200)


def lista_participantes(request, sid):
    key = get_session_key(USER, PASSWORD)
    participantes = list_participants(key, sid=sid)

    return JsonResponse(participantes, safe=False, json_dumps_params={'ensure_ascii':False}, status=200)
