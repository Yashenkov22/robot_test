import json

from django.http import HttpRequest
from .forms import RobotForm


def valid_request(request: HttpRequest) -> dict | str:
    if request.content_type == 'application/json':
        data: dict = json.loads(request.body)
        form = RobotForm(data)
        
        try:
            if form.is_valid():
                data = form.cleaned_data
                data['serial'] = data['model'] + '-' + data['version']
                return data
            else:
                return form.errors.as_text()
                
        except AttributeError:
            return 'incorrect "created" field value'
    
    return 'incorrect content-type'