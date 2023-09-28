import json
import sqlite3

import pandas

from django.http import HttpRequest

from .forms import RobotForm


query_to_excel = '''
SELECT model, version, count(version) as cnt
FROM robots_robot
WHERE created >= datetime("now", "-7 day")
GROUP by version
ORDER BY cnt
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


def make_excel_file():
    conn = sqlite3.connect('db.sqlite3')

    df = pandas.read_sql(query_to_excel, conn)

    model = df['model'].drop_duplicates()

    with pandas.ExcelWriter('output.xlsx') as writer:
        for m in model:
            sub_df = df[df['model'] == m]
            
            sub_df.to_excel(writer,
                            sheet_name=f'model {m}',
                            index=False,
                            header=['Модель', 'Версия', 'Количество за неделю'])
