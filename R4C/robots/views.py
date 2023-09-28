from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services import valid_request
from .models import Robot


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

