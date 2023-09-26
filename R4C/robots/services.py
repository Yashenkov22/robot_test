import json
import sqlite3
import os

import pandas

from django.http import HttpRequest
from .forms import RobotForm


query_to_excel = '''
SELECT model, version, count(version)
FROM robots_robot
WHERE model = "{}" AND created >= datetime("now", "-7 day")
GROUP by version
'''


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


def make_excel_file(models: list):
    conn = sqlite3.connect('db.sqlite3')
    models = map(lambda x: x[0], models)

    with pandas.ExcelWriter('output.xlsx') as writer:
        
        for model in models:  
            df = pandas.read_sql(query_to_excel.format(model),
                                 conn)
            
            df.to_excel(writer,
                        sheet_name=f'model {model}',
                        index=False,
                        header=['Модель', 'Версия', 'Количество за неделю'])
