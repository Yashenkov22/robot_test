import os

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services import valid_request, make_excel_file
from .models import Robot


#Page with link to download excel file
def index(request):
    return render(request, 'robots/download.html')


#Add new record to database
@require_POST
@csrf_exempt
def new_robot_record(request: HttpRequest):
    data = valid_request(request)

    if isinstance(data, dict):

        Robot.objects.create(**data)
        return JsonResponse({'status': 'success',
                             'detail': 'object has been created'})
        
    else:
        return JsonResponse({'status': 'error',
                             'detail': data})


def download_excel(request):

    make_excel_file()

    with open('output.xlsx', 'rb') as f:
        response = HttpResponse(f, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="File.xlsx"'

    if os.path.exists('output.xlsx'):
        os.remove('output.xlsx')
    
    return response