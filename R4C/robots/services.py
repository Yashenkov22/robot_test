import json

from django.http import HttpRequest


KEYS_MODEL = {'model', 'version', 'created'}


def valid_request(request: HttpRequest) -> dict | str:
    if request.content_type == 'application/json':
        data: dict = json.loads(request.body)

        if len(data) == 3 and all(key in KEYS_MODEL for key in data):
            data['serial'] = data['model'] + '-' + data['version']
            return data
        else:
            return 'incorrect json data'
    
    return 'incorrect content-type'